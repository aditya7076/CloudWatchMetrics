import boto3
import datetime
import numpy as np

csv_headers = {
    'ec2': [
        'name',
        'instance',
        'type',
        'hypervisor',
        'virtualization_type',
        'architecture',
        'ebs_optimized',
        'image_id',
        'key_name',
        'metric',
        'low',
        'high',
        'ave',
        'median',
        'launch_time',
        'subnet_id',
        'vpc_id'
    ]
    }

# create boto clients
cw = boto3.client('cloudwatch')
ec2 = boto3.resource('ec2')


def get_all_instances(resource):
    if resource == 'ec2':
        return ec2.instances.filter(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']}])
    else:
        return None


def get_metric(resource, id, period, days, metric, namespace):
    # get current time
    now = datetime.datetime.now()

    # identify dimension name
    if resource == 'ec2':
        dimension_name = 'InstanceId'
    else:
        return None

    # get metric statistics
    return cw.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric,
        Dimensions=[{
            'Name': dimension_name,
            'Value': id
        }],
        StartTime=now - datetime.timedelta(days=days),
        EndTime=now,
        Period=period,
        Statistics=['Maximum'],
        Unit='Percent'
    )


def process_metric(result):
    # get all datapoints and add to list
    item_list = []
    for datapoint in result['Datapoints']:
        item_list.append(float(datapoint['Maximum']))

    # on empty datapoints, append zero to avoid zero-size array error
    if len(item_list) == 0:
        item_list.append(0)

    # return a numpy array
    return np.array(item_list)


def write_to_csv(resource, csvwriter, instance, item_list_arr, metric):
    if resource == 'ec2':
        # get instance name
        if instance.tags:
            name_dict = next(
                (i for i in instance.tags if i['Key'] == 'Name'),
                None)
        else:
            name_dict = None

        # write data rows
        csvwriter.writerow([
            '' if name_dict is None else name_dict.get('Value'),
            instance.id,
            instance.instance_type,
            instance.hypervisor,
            instance.virtualization_type,
            instance.architecture,
            instance.ebs_optimized,
            instance.image_id,
            instance.key_name,
            metric,
            np.min(item_list_arr),
            np.max(item_list_arr),
            np.round(np.average(item_list_arr), 2),
            np.median(item_list_arr),
            instance.launch_time,
            instance.subnet_id,
            instance.vpc_id
        ])
