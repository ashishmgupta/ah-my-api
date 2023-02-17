import boto3
import traceback
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_fullpage_screenshot(url,fileName):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)
    
    #the element with longest height on page
    #ele=driver.find_element("xpath", '//div[@class="react-grid-layout layout"]')
    #total_height = ele.size["height"]+1000
    
    driver.set_window_size(1920, 1000)      #the trick
    time.sleep(2)
    driver.save_screenshot(fileName)
    driver.quit()

with open('banner.txt', 'r') as file:
    data = file.read()
    print(data)

# Create a client to access the STS service
sts_client = boto3.client('sts')

# Iterate through all the AWS accounts
session = boto3.session.Session()
org = session.client('organizations')
paginator = org.get_paginator('list_accounts')
page_iterator = paginator.paginate()
for page in page_iterator:        
    for acct in page['Accounts']:
        #print(acct) # print the account

        if  acct["Id"] != "655210302908":
            print(" Account Id :" +acct["Id"])
            print(" Account Email :" +acct["Email"])
            #response = sts_client.assume_role(RoleArn='arn:aws:iam::771025898509:role/ScanAWSAPIRole', RoleSessionName='MySession')
            response = sts_client.assume_role(RoleArn='arn:aws:iam::'+acct["Id"]+':role/ScanAWSAPIRole', RoleSessionName='MySession')
            aws_access_key_id=response['Credentials']['AccessKeyId']
            aws_secret_access_key=response['Credentials']['SecretAccessKey']
            aws_session_token=response['Credentials']['SessionToken']
            #print(aws_access_key_id)
            #print(aws_secret_access_key)
            #print(aws_session_token)

            regions = ['ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

                #print(client)
            urls_to_test = []    
            rest_api_ids = []
            stage_names = []
            resource_paths = []
            #print(client.get_account())
            client = boto3.client('apigateway',aws_access_key_id=response['Credentials']['AccessKeyId'], aws_secret_access_key=response['Credentials']['SecretAccessKey'], aws_session_token=response['Credentials']['SessionToken'])
            # Get all the REST APIs, the stages and resources
            all_rest_apis=client.get_rest_apis()

            if len(all_rest_apis["items"]) > 0:
                print("Number of API gateways in the region "+str(len(all_rest_apis["items"])))

                for rest_api in all_rest_apis["items"]:
                        rest_api_ids.append(rest_api["id"])

                        stages = client.get_stages(restApiId=rest_api["id"])
                        for stage in stages["item"]:
                            stage_names.append(stage["stageName"])
                            resources=client.get_resources(restApiId=rest_api["id"])
                            resources = resources['items']
                            for resource in resources:
                                resource_paths.append(resource["path"])
                                if resource["path"] !="/" and resource["path"] !="/{proxy+}":
                                    url = 'https://'+rest_api["id"] +".execute-api.us-east-1.amazonaws.com"
                                    url += "/"+stage["stageName"]
                                    url += resource["path"]
                                    if url not in urls_to_test:
                                        urls_to_test.append(url)


            for url_to_test in urls_to_test:
                print(url_to_test)
                try:
                    get = requests.get(url_to_test)
                    # if the request succeeds 
                    if get.status_code == 200 :
                        print("URL is reachable...")
                        fileName = url_to_test.replace("https://","").replace("/","_")+ ".png"
                        print("taking screenshot")
                        test_fullpage_screenshot(url_to_test, fileName)
                        print("screenshot saved as " + fileName)
                    else:
                        print("URL {0} is NOT reachable...", url_to_test)
                except:
                        print("URL {0} is NOT reachable with exception.", url_to_test)
                        continue
