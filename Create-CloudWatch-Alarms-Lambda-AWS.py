from collections import defaultdict

import boto3

ec2_sns = 'SNS-Topic:'
ec2_rec ="arn:aws:automate:eu-west-1:ec2:recover"


"""
A tool for retrieving  the  EC2 instances with specific tag.
"""
def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    cw = boto3.client('cloudwatch')
    ec2info = defaultdict()
    running_instances = ec2.instances.filter(Filters=[{'Name': 'tag-key','Values': ['cloudwatch'],}])
    for instance in running_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key']:
                name = tag['Value']
                 ###############################################
                # Add instance info to a dictionary         
                ec2info[instance.id] = {'Name': name,'InstanceId':instance.instance_id,}
                
                attributes = ['Name','InstanceId']
                for instance_id, instance in ec2info.items():
                        instanceid =instance["InstanceId"]
                        nameinsta = instance["Name"]
                        print(instanceid,nameinsta )
                         ###############################################
                        #Create CPU Alarms                
                        cw.put_metric_alarm(
                         AlarmName = (nameinsta) + "_CPU_Load_(Lambda)",
                         AlarmDescription='CPU Utilization ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_sns,],
                         MetricName='CPUUtilization',
                         Namespace='AWS/EC2',
                         Statistic='Average',
                         Dimensions=[ {'Name': "InstanceId",'Value': instanceid},],
                         Period=300,
                         EvaluationPeriods=1,
                         Threshold=70.0,
                         ComparisonOperator='GreaterThanOrEqualToThreshold')
                         ###############################################
                        #Create NetworkOut Alarms
                        cw.put_metric_alarm(
                         AlarmName = (nameinsta) + "_Network_Bandwidth_(Lambda)" ,
                         AlarmDescription='NetworkOut ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_sns,],
                         MetricName='NetworkOut',
                         Namespace='AWS/EC2',
                         Statistic='Average',
                         Dimensions=[ {'Name': "InstanceId",'Value': instanceid},],
                         Period=300,
                         EvaluationPeriods=1,
                         Threshold=50000000,
                         ComparisonOperator='GreaterThanOrEqualToThreshold')
                            ###############################################
                         #Create StatusCheckFailed Alamrs
                        cw.put_metric_alarm(
                         AlarmName = (nameinsta) + "_StatusCheckFailed_(Lambda)",
                         AlarmDescription='StatusCheckFailed ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_sns,],
                         MetricName='StatusCheckFailed',
                         Namespace='AWS/EC2',
                         Statistic='Average',
                         Dimensions=[ {'Name': "InstanceId",'Value': instanceid},],
                         Period=900,
                         EvaluationPeriods=1,
                         Threshold=1,
                         ComparisonOperator='GreaterThanOrEqualToThreshold')
                          ###############################################
                           #Create StatusCheckFailed_System Alamrs
                        cw.put_metric_alarm(
                         AlarmName= (nameinsta) + "_StatusCheckFailed_System_(Lambda)",
                         AlarmDescription='StatusCheckFailed_System ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_rec,ec2_sns],
                         MetricName='StatusCheckFailed_System',
                         Namespace='AWS/EC2',
                         Statistic='Average',
                         Dimensions=[ {'Name': "InstanceId",'Value': instanceid},],
                         Period=900,
                         EvaluationPeriods=1,
                         Threshold=1,
                         ComparisonOperator='GreaterThanOrEqualToThreshold')
                          ###############################################
                           #Create DiskWriteOps Alarms
                        cw.put_metric_alarm(
                         AlarmName = (nameinsta) +"_DiskWriteOps_(Lambda)",
                         AlarmDescription='DiskWriteOps ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_sns,],
                         MetricName='DiskWriteOps',
                         Namespace='AWS/EC2',
                         Statistic='Average',
                         Dimensions=[ {'Name': "InstanceId",'Value': instanceid},],
                         Period=900,
                         EvaluationPeriods=1,
                         Threshold=2500,
                         ComparisonOperator='GreaterThanOrEqualToThreshold')
                         ###############################################
                         #Create DiskReadOps Alarms
                        cw.put_metric_alarm(
                         AlarmName= (nameinsta) +"_DiskReadOps_(Lambda)",
                         AlarmDescription='DiskReadOps ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_sns,],
                         MetricName='DiskReadOps',
                         Namespace='AWS/EC2',
                         Statistic='Average',
                         Dimensions=[ {'Name': "InstanceId",'Value': instanceid},],
                         Period=900,
                         EvaluationPeriods=1,
                         Threshold=2500,
                         ComparisonOperator='GreaterThanOrEqualToThreshold')
                         #Create MemoryUtilization Alarms
                        cw.put_metric_alarm(
                         AlarmName= (nameinsta) +"MemoryUtilization(Lambda)",
                         AlarmDescription='MemoryUtilization ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_sns,],
                         MetricName='MemoryUtilization',
                         Namespace='System/Linux',
                         Statistic='Average',
                         Dimensions=[ {'Name': "InstanceId",'Value': instanceid},],
                         Period=300,
                         EvaluationPeriods=1,
                         Threshold=80,
                         ComparisonOperator='GreaterThanOrEqualToThreshold')
                         #Create SwapUtilization Alarms
                        cw.put_metric_alarm(
                         AlarmName= (nameinsta) +"SwapUtilization(Lambda)",
                         AlarmDescription='SwapUtilization ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_sns,],
                         MetricName='SwapUtilization',
                         Namespace='System/Linux',
                         Statistic='Average',
                         Dimensions=[ {'Name': "InstanceId",'Value': instanceid},],
                         Period=300,
                         EvaluationPeriods=1,
                         Threshold=5,
                         ComparisonOperator='GreaterThanOrEqualToThreshold')
                         #Create DiskSpaceUtilization Alarms
                        cw.put_metric_alarm(
                         AlarmName= (nameinsta) +"DiskSpaceUtilization(Lambda)",
                         AlarmDescription='DiskSpaceUtilization ',
                         ActionsEnabled=True,
                         AlarmActions=[ec2_sns,],
                         MetricName='DiskSpaceUtilization',
                         Namespace='System/Linux',
                         Statistic='Average',
                         Period=900,
                         EvaluationPeriods=1,
                         Threshold=90,
                         ComparisonOperator='GreaterThanOrEqualToThreshold',
                         Dimensions =[{'Name': 'MountPath', 'Value': '/'},
                         {'Name': 'InstanceId', 'Value': instanceid},
                         {'Name': 'Filesystem', 'Value': '/dev/xvda1'}],)
                         
                         
                         
                          
                  