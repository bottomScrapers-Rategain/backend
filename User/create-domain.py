import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def createOpenSearchDomain(client, domainName):

    response = client.create_domain(
        DomainName=domainName,
        EngineVersion='Elasticsearch_7.10',
        ClusterConfig={
            'InstanceType': 't2.small.search',
            'InstanceCount': 1,
            'DedicatedMasterEnabled': False,
            'ZoneAwarenessEnabled': False
        },
        EBSOptions={
            'EBSEnabled': True,
            'VolumeType': 'standard',
            'VolumeSize' : 10
        },
        AdvancedOptions={
            'rest.action.multi.allow_explicit_index': 'true'  # Optional: Modify advanced options if needed
        }
    )

    return response

# AWS credentials (replace with your actual credentials)
awsAccessKey = os.getenv("awsAccessKey")
awsSecretKey = os.getenv("awsSecretKey")
regionName = os.getenv("regionName")  

client = boto3.client('opensearch', region_name=regionName,
                     aws_access_key_id=awsAccessKey,
                     aws_secret_access_key=awsSecretKey)


domainName = "rategain2023"

# Create the Amazon OpenSearch index
createIndexResponse = createOpenSearchDomain(client, domainName)
print("Create index response:", createIndexResponse)