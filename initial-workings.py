import requests
from dotenv import load_dotenv
import os
import datetime
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json
load_dotenv()

api_key=os.getenv('MAILCHIMP_API_KEY')

#set date fields: this is what we will use to filter the data which is brought in
start_date = '2025-01-01'
end_date = datetime.datetime.now()
start_date_time = start_date +'T00:00:00'
end_date_time = end_date.strftime('%Y-%m-%d') + 'T23:59:59'

#sets a file name and checks the file exists, if it does it opens the file in read mode otherwise sets existing campaigns to an empty list
json_filename = 'mailchimp_campaigns.json'
if os.path.isfile(json_filename):
    with open(json_filename, 'r') as f:
        existing_campaigns = json.load(f)
else:
    existing_campaigns = []

# Build a set of existing campaign ids which already exist in your json file
existing_ids = {c['id'] for c in existing_campaigns}


try:
    client = MailchimpMarketing.Client()
    client.set_config({
    "api_key": api_key,
    # "start" : start_date,
    # "end" : end_date
  })
    
#filter to limit the data extracted to for this year
    response = client.campaigns.list(  
        since_create_time = start_date_time,
        before_create_time = end_date_time
      )

    campaigns = response.get('campaigns', [])

#remove any duplicate data, loops throughthe 
    new_campaigns = [c for c in campaigns if c['id'] not in existing_ids]

#Append only new campaigns, adds the list of new campaigns and adds it to the list of existing campaigns
    if new_campaigns:
        existing_campaigns.extend(new_campaigns)
        print(f"Appended {len(new_campaigns)} new campaigns.")
    else:
        print("No new campaigns to append.")

# Save the campaigns data to a JSON file
    with open('mailchimp_campaigns.json', 'w') as f:
        json.dump(campaigns, f, indent=4)

    print(f"Exported {len(campaigns)} campaigns to mailchimp_campaigns.json")

except ApiClientError as error:
    print("Error: {}".format(error.text))
