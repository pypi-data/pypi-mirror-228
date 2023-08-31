import sys
import os
import json
import time

import boto3

r"""
This script simplifies the process to spawn instances on EC2 built from scratch
on top of Amazon's original AMI.

There are two parts to this task. The first is to create the instance, and the
second is to apply patches to it.


Part 1: Create the instance

A few things are needed:
* authentication (profile or keys)
* region (e.g. us-east-1)
* image name (amzn-2015.09...)
* virtualization type (hvm, pv)
* instance type (e.g. m1.small)
* destination (availability zone or subnet id)
* role
* security groups

Ideally, a few tweaks are:
* automatically attach block devices
* (optionally) use spot pricing
* add to load balancer
* set tags
* set root volume size
* set key

cfg = foolaunch.Configuration()
cfg.apply("name")
...
foolaunch.launch(cfg)
"""

# https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RunInstances.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html


def _load_configurations(*args):
    filenames = ['./.foolaunch', '~/.foolaunch', '/etc/foolaunch']
    if args:
        filenames = list(args) + filenames
    result = {}
    for filename in reversed(filenames):
        try:
            body = None
            with open(os.path.expanduser(filename), 'rb') as f:
                body = f.read()
            try:
                body = json.loads(body)
            except:
                print("error parsing {}".format(filename), file=sys.stderr)
                continue
            for k, v in body.items():
                result[k] = v
        except:
            pass
    return result


# TODO couldn't figure out how to add prices.txt file to pyproject.toml, so removing for now
# # Create a Boto3 client for AWS Pricing
# pricing_client = boto3.client('pricing')

# # Define filters to narrow down the product search
# filters = [
#     {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Compute Instance'}
# ]

# # Get pricing data
# response = pricing_client.get_products(
#     ServiceCode='AmazonEC2',
#     Filters=filters
# )

# # Extract instance types and pricing information
# for product in response['PriceList']:
#     product = json.loads(product)  # Convert JSON string to dictionary
#     instance_type = product['product']['attributes']['instanceType']
#     on_demand = product['terms']['OnDemand']
#     for term_key, term_value in on_demand.items():
#         stuff = list(term_value['priceDimensions'].values())[0]
#         print(f"{instance_type}\t{stuff['pricePerUnit']}")


_EC2_INSTANCE_PRICE = {}
# with open(os.path.join(os.path.dirname(__file__), 'prices.txt')) as f:
#     for line in f:
#         if line[-1] == '\n':
#             line = line[:-1]
#         (instance_type, region, price) = line.split('\t')
#         _EC2_INSTANCE_PRICE[(instance_type, region)] = float(price)


_EC2_INSTANCE_VOLUME_COUNT = {
    'x1.16xlarge': 1,
    'x1e.4xlarge': 1,
    'x1e.16xlarge': 1,
    'x1.32xlarge': 2,
    'x1e.2xlarge': 1,
    'd2.8xlarge': 24,
    'd2.2xlarge': 6,
    'd2.xlarge': 3,
    'x1e.32xlarge': 2,
    'd2.4xlarge': 12,
    'x1e.8xlarge': 1,
    'x1e.xlarge': 1,
    'f1.4xlarge': 1,
    'h1.8xlarge': 4,
    'h1.16xlarge': 8,
    'h1.4xlarge': 2,
    'h1.2xlarge': 1,
}


_DEVICE_LETTER = []
for i in range(1, 26):
    _DEVICE_LETTER.append(chr(ord('a')+i))
for i in range(0, 26):
    for j in range(0, 26):
        _DEVICE_LETTER.append(chr(ord('a')+i) + chr(ord('a')+j))


def _make_block_device_mappings(image, root_volume_size=None):
    if root_volume_size is None:
        return None

    block_device_mappings = image['BlockDeviceMappings']

    if len(block_device_mappings) != 1:
        raise RuntimeError('unexpected number of block devices in image')

    if block_device_mappings[0]['Ebs']['VolumeSize'] == root_volume_size:
        return None
    
    # TODO: add emphemeral stores?
    # for i in range(_EC2_INSTANCE_VOLUME_COUNT.get(instance_type, 0)):
    #     block_device_mapping['/dev/sd' + _DEVICE_LETTER[i]] = \
    #         boto.ec2.blockdevicemapping.BlockDeviceType(ephemeral_name="ephemeral{}".format(i))

    return [
        {
            'DeviceName': block_device_mappings[0]['DeviceName'],
            'Ebs': {
                'DeleteOnTermination': block_device_mappings[0]['Ebs']['DeleteOnTermination'],
                'VolumeSize': root_volume_size,
                'VolumeType': block_device_mappings[0]['Ebs']['VolumeType']
            }
        }
    ]


def convert_dict_to_filters(input_dict):
    filters_list = []
    
    for key, value in input_dict.items():
        filter_dict = {'Name': key, 'Values': [value]}
        filters_list.append(filter_dict)
    
    return filters_list


def _lookup_ami(ec2, image_filters):
    """Returns AMI id that matches `image_filters`"""

    images = ec2.describe_images(Filters=convert_dict_to_filters(image_filters))['Images']
    if len(images) == 0:
        raise RuntimeError('cannot find image')
    if len(images) != 1:
        raise RuntimeError('found multiple images: {}'.format(', '.join([image.id for image in images])))
    return images[0]


def _lookup_security_group_ids(ec2, names):
    if not names:
        return None
    security_groups = ec2.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': names}])
    return [i['GroupId'] for i in security_groups['SecurityGroups']]


class _Connections(object):
    def __init__(self):
        self.session = None
        self.ec2 = None


class _Context(object):
    def __init__(self):
        self.image = None
        self.image_id = None
        self.block_device_mappings = None
        self.subnet_id = None


# TODO make this more robust
_VALID_KEYS = {
        "profile",
        "region",
        "image_filters",
        "instance_type",
        "placement",
        "subnet",
        "key",
        "instance_profile",
        "security_groups",
        "tags",
        "root_volume_size",
        "load_balancers",
        "user_data",
        "spot",
        "name",
        "count",
        "price",
        "*"
    }


class Session(object):
    def __init__(self, *args):
        self._configurations = _load_configurations(*args)
        # aws profile name
        self.profile = None
        # aws region name
        self.region = None
        # ami filters
        self.image_filters = None
        # ec2 instance type
        self.instance_type = None
        # ec2 availability zone
        self.placement = None
        # subnet id
        self.subnet = None
        # key pair name
        self.key = None
        # iam instance profile name
        self.instance_profile = None
        # security group names (list)
        self.security_groups = None
        # instance tags to set (dict (str->str))
        self.tags = None
        # root volume size (number, in ??)
        self.root_volume_size = None
        # elastic load balancers (list (str))
        self.load_balancers = None
        # instance user data (str)
        self.user_data = None
        # use spot pricing
        self.spot = False
        # dry run
        self.dry_run = False
        # instance name
        self.name = None
        # number of instances to launch
        self.count = None
        # max price
        self.price = None

        if "default" in self._configurations:
            self.apply("default")

    def apply(self, label):
        if label not in self._configurations:
            raise ValueError("configuration {} not found".format(label))

        total = {}
        self._apply(label, total)
        for k, v in total.items():
            setattr(self, k, v)

    def _apply(self, label, total):
        assert isinstance(total, dict)
        if label not in self._configurations:
            raise ValueError("configuration {} not found".format(label))
        configuration = self._configurations[label]
        if not isinstance(configuration, dict):
            raise ValueError("configuration {} not a dict".format(label))

        if "*" in configuration:
            includes = configuration["*"]
            if not isinstance(includes, list):
                raise ValueError("configuration {} default (*) not a list".format(label))
            for i in includes:
                self._apply(i, total)

        for k, v in configuration.items():
            if k != "*":
                if k not in _VALID_KEYS:
                    raise ValueError("invalid key {} in configuration {}".format(k, label))
                total[k] = v

    def launch(self):
        conn = _Connections()

        conn.session = boto3.Session(region_name=self.region, profile_name=self.profile)
        conn.ec2 = conn.session.client('ec2')

        ctx = _Context()

        print("connected")

        # -- find ami image id --

        ctx.image = _lookup_ami(conn.ec2, self.image_filters)
        ctx.image_id = ctx.image['ImageId']

        print("ami image '{}' found as '{}'".format(self.image_filters, ctx.image_id))

        # -- find placement or subnet id --

        if self.subnet:
            subnets = conn.ec2.describe_subnets(Filters=[{'Name': 'tag:Name', 'Values': [self.subnet]}])
            if len(subnets) == 0:
                raise ValueError("no matching subnets")
            if len(subnets) != 1:
                raise ValueError("too many matching subnets")
            ctx.subnet_id = subnets[0]['SubnetId']
            print("subnet '{}' found as '{}'".format(self.subnet, ctx.subnet_id))

        # -- create block device mapping --

        # ctx.block_device_mappings = _make_block_device_map(ctx.image, self.instance_type, self.root_volume_size)
        ctx.block_device_mappings = _make_block_device_mappings(ctx.image, self.root_volume_size)

        # -- find security group ids --

        create_kwargs = {
            'InstanceType': self.instance_type,
            'DryRun': self.dry_run
        }

        if ctx.subnet_id:
            create_kwargs['SubnetId'] = ctx.subnet_id
        elif self.placement:
            create_kwargs['Placement'] = self.placement

        if self.key:
            create_kwargs['KeyName'] = self.key

        if self.instance_profile:
            create_kwargs['IamInstanceProfile'] = {'Name': self.instance_profile}

        if self.security_groups:
            create_kwargs['SecurityGroups'] = self.security_groups

        if ctx.block_device_mappings:
            create_kwargs['BlockDeviceMappings'] = ctx.block_device_mappings

        if self.user_data:
            create_kwargs['UserData'] = self.user_data

        instance_ids = []
        if self.spot:
            # TODO: make spot work
            if self.count:
                create_kwargs['count'] = self.count

            price = _EC2_INSTANCE_PRICE[(self.instance_type, conn.old_ec2.region.name)]
            if self.price:
                price = self.price

            result = conn.old_ec2.request_spot_instances(price, ctx.image_id, **create_kwargs)
            spot_request_ids = [x.id for x in result]
            for spot_request_id in spot_request_ids:
                state = 'open'
                while state == 'open':
                    print("Waiting on spot request...")
                    time.sleep(5)
                    spot = conn.old_ec2.get_all_spot_instance_requests(spot_request_id)[0]
                    state = spot.state
                if state != 'active':
                    print("Failed to create instance.")
                    continue
                instance_ids.append(spot.instance_id)
        else:
            if self.count:
                create_kwargs['MinCount'] = self.count
                create_kwargs['MaxCount'] = self.count
            else:
                create_kwargs['MinCount'] = 1
                create_kwargs['MaxCount'] = 1

            create_kwargs['ImageId'] = ctx.image_id
            create_kwargs['MetadataOptions'] = {
                'HttpTokens': 'required',
                'HttpPutResponseHopLimit': 2
            }

            result = conn.ec2.run_instances(**create_kwargs)
            for i in result['Instances']:
                instance_ids.append(i['InstanceId'])

        if instance_ids:
            print("Instances '{}' created.".format(', '.join(instance_ids)))

            if self.name:
                conn.ec2.create_tags(Resources=instance_ids, Tags=[{'Key': 'Name', 'Value': self.name}], DryRun=self.dry_run)

            if self.tags:
                tags = [{'Key': k, 'Value': v} for (k, v) in self.tags.items()]
                conn.ec2.create_tags(Resources=instance_ids, Tags=tags, DryRun=self.dry_run)

            if not self.dry_run and self.load_balancers:
                # TODO: make load balancers work
                # # Initialize the ELBV2 client
                # elbv2_client = boto3.client('elbv2')

                # # Specify the target group ARN and instance IDs
                # target_group_arn = 'arn:aws:elasticloadbalancing:REGION:ACCOUNT_ID:targetgroup/TARGET_GROUP_NAME/GENERATED_ID'
                # instance_ids = ['INSTANCE_ID_1', 'INSTANCE_ID_2']

                # # Register instances with the target group
                # response = elbv2_client.register_targets(
                #     TargetGroupArn=target_group_arn,
                #     Targets=[{'Id': instance_id} for instance_id in instance_ids]
                # )
                for load_balancer in self.load_balancers:
                    conn.old_elb.register_instances(load_balancer, [i for i in instance_ids])

            response = conn.ec2.describe_instances(InstanceIds=instance_ids)
            instances = [r['Instances'][0] for r in response['Reservations']]
            for instance in instances:
                print("{}: {}".format(instance['InstanceId'], instance['PublicIpAddress']))

            return conn, instances

        return conn, []
