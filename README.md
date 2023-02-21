# ah-my-api
![image](https://user-images.githubusercontent.com/1037523/220186671-7dc5e7e0-4202-4373-ba05-25a826e11e73.png)

The REST API gateways created in AWS have a default endpoint and If not explicely secured, they are publically accessible from internet by default. Wrote a script which would find such APIs across in all regions under all the accounts in the AWS organizations and screenshot their webpage for evidence. It will also generated a CSV file which may be ingested by a SIEM such as Splunk for alerting and remediation.

The script when executed will produce a CSV file in the below format showing all the API URLs and which one could be publically accessible and which security setting are applied on the API if API is not accessible.

# Important 
Please set up appropriate role and permissions as noted in below blog post
https://guptaashish.com/2023/02/21/ahh-my-api-discover-publically-exposed-apis-in-aws/

# Setup the AWS credentials
aws configure

# Clone the git repo
https://github.com/ashishmgupta/ah-my-api.git 

# Install all the requirements
pip install -r requirements

# Run the script
python ./ah-my-api.py
