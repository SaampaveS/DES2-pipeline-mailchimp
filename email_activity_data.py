import requests
from dotenv import load_dotenv
import os
import datetime
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

api_key=os.getenv('MAILCHIMP_API_KEY')
start_date = '2025-01-01'
start_date_time= start_date +'T00:00:00'
try:
  client = MailchimpMarketing.Client()
  client.set_config({
    "api_key": api_key,
    "since" : start_date_time
  })

  response = client.reports.get_email_activity_for_campaign("campaign_id")
  print(response)
except ApiClientError as error:
  print("Error: {}".format(error.text))