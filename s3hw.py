import boto3
import csv
import io

s3=boto3.resource('s3',
         aws_access_key_id='',
         aws_secret_access_key= '')
#s3.create_bucket(Bucket='s3hellested', CreateBucketConfiguration={'LocationConstraint':'us-west-2'})

dyndb=boto3.resource('dynamodb',
        aws_access_key_id='',
        aws_secret_access_key= '',
        region_name='us-west-2')


table=dyndb.Table('DataTable')
urlbase='https://s3-us-west-2.amazonaws.com/datacont/'
with open('.\datafiles\experiments.csv', 'rt' ) as csvfile:
    csvf=csv.reader(csvfile, delimiter=',', quotechar='|')
    linecount=0
    for item in csvf:
        if linecount==0:
            linecount+=1
        else:
            body=open('./datafiles//'+item[4],'rb')
            s3.Object('s3hellested', item[3]).put(Body=body)
            md=s3.Object('s3hellested',item[3]).Acl().put(ACL='public-read')
            url=urlbase+item[3]
            metadata_item={'PartitionKey':item[0],'RowKey':item[1],'description':item[4],'date':item[2],'url':url}
            try:
                table.put_item(Item=metadata_item)
            except:
                print ("item may already be there or another failure")


response = table.get_item(
 Key={
 'PartitionKey': 'experiment2',
 'RowKey': 'data2'
 }
)
item = response['Item']
print(item)
print(response)