import requests
from dotenv import load_dotenv
import os
import datetime
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json
load_dotenv()

api_key=os.getenv('MAILCHIMP_API_KEY')



all_campaigns = []
offset = 0
count = 100 

try:
    client = MailchimpMarketing.Client()
    client.set_config({
    "api_key": api_key,
    # "start" : start_date,
    # "end" : end_date
  })
except ApiClientError as error:
    print("Error: {}".format(error.text))
    
while True:   
#filter to limit the data extracted to for this year
    response = client.campaigns.list(  
        offset=offset, 
        count=count
      )

    campaigns = response.get('campaigns', [])
    if not campaigns:
        break
    all_campaigns.extend(campaigns)
    offset += count

#Save the campaigns data to a JSON file
with open('mailchimp_campaigns.json', 'w') as f:
    json.dump(campaigns, f, indent=4)

    print(f"Exported {len(campaigns)} campaigns to mailchimp_campaigns.json")

