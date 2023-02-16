import json
import boto3
from operator import itemgetter
from botocore.exceptions import ClientError
ec2_client = boto3.client('ec2')
client = boto3.client('rds') 
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')
def lambda_handler(event, context):
    regionsss = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    NonComplainceList = []  
    message = "The following instances were not Tag Complaince. These intances have been stopped.The Following Tags should be present for each instance: 'BU' 'Owner' 'Dept' 'Project' 'Company'."
    #print(message)
    for i in regionsss:             
            #print(i)
            var = boto3.client('rds', region_name=i)
            j = var.describe_db_instances()   
            for db in j['DBInstances']:
                #print(db['DBInstanceIdentifier'],db['DBInstanceStatus']) 
                con=db['TagList']
                #print(con)
                rdp = list(map(itemgetter('Key'), con))
                #print("keys : " + str(rdp))
                table=dynamodb.Table(<Table name Configurable>)  
                response=table.get_item(Key={'name':'RDS'}) 
                rds_check=response['Item']['Tags']
                #print(rds_check)
                if len(rdp)==0:
                    NonComplainceList.append(db['DBInstanceIdentifier'])
                    #print(NonComplainceList)
                else:
                    for tag in con: 
                        if not tag['Value']:
                            NonComplainceList.append(db['DBInstanceIdentifier'])
                            #print(db['DBInstanceIdentifier'])
                            message = message + "\n" + "Region Name           : " + i 
                            message = message + "\n" + "DBInstance Name    : " + db['DBInstanceIdentifier'] + "\t" "\t" + "Status :  " + db['DBInstanceStatus']
                            break
                check = all(item in rds_check for item in rdp)    
                if check == True:  
                    print(' ') 
                else:
                    message = message + "\n" + "Region Name           : " + i 
                    message = message + "\n" + "DBInstance Name    : " + db['DBInstanceIdentifier'] + "\t" "\t" + "Status :  " + db['DBInstanceStatus']
                    #print(message)
                    print("Region Name      : " + i )
                    print("Instance Name    : " + db['DBInstanceIdentifier'] + '\t' +"DBInstanceStatus : " + db['DBInstanceStatus']) 
                    NonComplainceList.append(db['DBInstanceIdentifier'])
                    #break
    print(NonComplainceList)     
    response = sns_client.publish(
    TargetArn = <Arn Configurable>,
    Message = message,
    Subject = "RDS Non Complaince"  
    )
    
    