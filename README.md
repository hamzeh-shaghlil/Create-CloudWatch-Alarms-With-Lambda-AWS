# AWS-CloudWatch-Alarms-With-Lambda-Function
This Lambda Function Will filiter AWS-EC2 Instances by tag ((cloudwatch)) then will Create the below Alarms for each instance.
*  StatusCheckFailed_System >= 1 for 15 minutes
*  StatusCheckFailed >= 1 for 15 minutes
*  NetworkOut >= 50,000,000 for 5 minutes
*  CPUUtilization >= 80 for 5 minutes
*  DiskWriteOps >= 2,500 for 15 minutes
*  DiskReadOps >= 2,500 for 15 minutes
*  MemoryUtil >=80 for 5 minutes (Linux)
*  SwapUtil >=5 for 5 minutes(Linux)
*  DiskUsage >= 90 for 15 minuets(Linux)
