# CloudWatchMetrics

Description:

This script, awsmetric2csv.py, helps to collect CPUUtilization and MemoryUtilization metrics.
CPU utilization can be obtained by default from ClouWatch console, but to retrieve MemoryUtilization, CloudWatch Agent has to be installed on the each instance from where the metrics are to be collected.

Installation:

On the VirtualMachines to get metrics of:

1. Install ClouWatch Agent 

Can be found <a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-on-first-instance.html"> here</a>


The ClouWatch Monitoring Scripts for Amazon EC2 Linux-based instances, follow the instructions below that are provided by AWS. The Perl scripts comprise a fully functional example that reports memroy, swap, and disk space utilization metrics for a linux instance.
All the instructions (Step 1 through 8) can also be found <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html"> here </a>


2. Install prerequisite: 
   For some versions of Linux, you must install additional modules before the monitoring scripts will work.
   Log onto to the instance and install the following packages: 
  

  
  Amazon Linux and Amazon Linux AMI.
    
      sudo yum install -y perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https perl-Digest-SHA.x86_64

  SUSE Linux Enterprise Server.
  
      sudo zypper install perl-Switch perl-DateTime
      sudo zypper install –y "perl(LWP::Protocol::https)"

  Red Hat Enterprise Linux 6.9.
      
      sudo yum install perl-DateTime perl-CPAN perl-Net-SSLeay perl-IO-Socket-SSL perl-Digest-SHA gcc -y
      sudo yum install zip unzip
    
  Run CPAN as an elevated user.
	 
      sudo cpan
	
  Press Enter through the Prompts until you see the following prompt:
	 
      cpan[1]>
	
At CPAN prompt, run each of the below commands: run once command and it installs, and when you return to the CPAN prompt, run the next command. Press Enter like beofre when prompted to continue through the process:
	
      cpan[1]> install YAML 
      cpan[2]> install LWP::Protocol::https 
      cpan[3]> install Sys::Syslog 
      cpan[4]> install Switch 

	
  Red Hat Enterprise Linux 7.4
  
      sudo yum install perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https perl-Digest-SHA --enablerepo="rhui-REGION-rhel-server-optional" -y 
      sudo yum install zip unzip
	 

  Ubuntu Server.
  
      sudo apt-get update
      sudo apt-get install unzip
      sudo apt-get install libwww-perl libdatetime-perl
 	

3. To Download, Install and Configure monitoring scripts
   At the folder where you want to store the monitoring scritps run
	  
       curl https://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.2.zip -O

4. Run the following commands to install the monitoring scripts you downloaded

       unzip CloudWatchMonitoringScripts-1.2.2.zip && \
       rm CloudWatchMonitoringScripts-1.2.2.zip && \
       cd aws-scripts-mon

5. Ensure the script has required permission to perform CloudWatch operation.
  
   If an IAM role has been associated, verify it grants to perform following operations:
  
      cloudwatch:PutMetricData
      
      cloudwatch:GetMetricStatistics
      
      cloudwatch:ListMetrics
      
      ec2:DescribeTags
      
   Else,
   
6. Specify AWS credentials in a credentials file. Copy awscreds.template file included with monitoring scripts to awscreds.conf as follows.
     
       cp awscreds.template awscreds.conf
  
   Add credentials to the awscreds.conf file
	 
       AWSAccessKeyId = my-access-key-id
       AWSSecretKey = my-secret-access-key
   
7. To perform a simple test run without posting data to CloudWatch

       ./mon-put-instance-data.pl --mem-util --verify --verbose 
       
   
   Perfom a test run to collect available metrics and send them to CloudWatch, counting cache and buffer memory as used.
   
       ./mon-put-instance-data.pl --mem-used-incl-cache-buff --mem-util --mem-used --mem-avail
   
8. Start a cron schedule for metrics reported to CloudWatch
      
       crontab -e 
       
       */5 * * * * /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-used-incl-cache-buff --mem-util --mem-used --mem-avail


 A Custom Namespace of "Linux System" will be created on CloudWatch console providing graphical representation of MemoryUtilization.
  
  ![alt text](https://github.com/ccrshishir1/CloudWatchMetrics/blob/master/Custom%20Namespace.PNG)
 
 
This script runs only against the target instances that are on the same region as the machine where script is running is on. 


From your terminal:

9. Clone Project from github.
   
   https://github.com/ccrshishir1/CloudWatchMetrics.git
   
   Go to the project folder:
   
       cd awsmetric2csv

  Install requirements before running scripts.
  
  Pip (If not installed already)
  
  Boto3 (If not installed already)
  
  Numpy (If not installed already)
 
 or use 
  
      pip install -r requirements.txt
      
  Install AWS CLI (If not installed already)
     
     pip install awscli
  
  Configure AWS CLI (If not configured already)
     
     aws configure

Usage:
      
      python awsmetric2csv.py ec2 
       
 By default, number of days the metrics collected off is 7. You can change the number of days to retrieve metrics off by using --days option.
      
 --days: specifies number of days.
      
 Example:
  
       python awsmetric2csv.py ec2 --days 30

Output: output.csv
