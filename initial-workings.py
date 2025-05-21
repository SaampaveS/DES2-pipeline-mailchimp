import requests
from dotenv import load_dotenv
import os
import datetime
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json
from os import listdir
from os.path import isfile, join
from functions.Upload import upload_to_s3

load_dotenv()

api_key=os.getenv('MAILCHIMP_API_KEY')

#set date fields: this is what we will use to filter the data which is brought in
start_date = '2025-01-01'
end_date = datetime.datetime.now()
start_date_time = start_date +'T00:00:00'
end_date_time = end_date.strftime('%Y-%m-%d') + 'T23:59:59'

try:
    client = MailchimpMarketing.Client()
    client.set_config({
    "api_key": api_key,
  })
    
#filter to limit the data extracted to for this year
    response = client.campaigns.list(  
        since_create_time = start_date_time,
        before_create_time = end_date_time
      )

    campaigns = response.get('campaigns', [])
    # Define the folder where you want to save the JSON files
    save_folder = 'exported_campaigns'

    # Create the folder if it doesn't exist
    os.makedirs(save_folder, exist_ok=True)

    for campaign in [c for c in campaigns]:
        campaign_id = campaign['id']
        filename = campaign_id+'.json'
        file_list = [f for f in os.listdir('.') if f.endswith('.json')]
        file_path = os.path.join(save_folder, filename)

        if os.path.exists(file_path):
            print('Up to date')
        else:
        #save to a file
            with open(file_path, 'w') as file:
                json.dump(campaign, file)
            print(f"Exported campaign {campaign_id} to {filename}")


except ApiClientError as error:
    print("Error: {}".format(error.text))

my_path = save_folder
onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path,f))]

bucket_file_path = os.getenv('aws_bucket_filepath')
aws_access_key=os.getenv('aws_access_key')
aws_secret_key=os.getenv('aws_secret_key')
bucket_name=os.getenv('aws_bucket')

for file in onlyfiles:

    local_file = my_path+'/'+file
    bucket_filename = bucket_file_path+'/campaign/'+ file
    upload_to_s3(aws_access_key,aws_secret_key, local_file, bucket_name, bucket_filename)



    
