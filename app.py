import os
import requests

# Configuration
TENANT_ID = os.environ.get('TENANT_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')  # This is the Microsoft Entra Identity Application ID
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
RESOURCE = 'https://cloudapi.deployment.marketplace.azure.com/'
GRANT_TYPE = 'client_credentials'
METER_ID = os.environ.get('UserCount')  # This is the ID you've set for your metering dimension
CUSTOMER_SUBSCRIPTION_GUID = os.environ.get('CUSTOMER_SUBSCRIPTION_GUID')  # Provided when a customer subscribes
RESOURCE_GUID = os.environ.get('RESOURCE_GUID')  # Your marketplace resource ID

# Function to get access token
def get_access_token():
    token_url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
    token_data = {
        'grant_type': GRANT_TYPE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': f'{RESOURCE}/.default'
    }
    response = requests.post(token_url, data=token_data)
    return response.json().get("access_token")

# Report usage to Azure Marketplace Metering Service
def report_usage(user_count):
    token = get_access_token()
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    report_url = f'https://cloudapi.deployment.marketplace.azure.com/api/usageEvent?api-version=2018-08-31'
    
    usage_data = {
        'resourceId': f'/subscriptions/{CUSTOMER_SUBSCRIPTION_GUID}/resourceGroups/default/providers/Marketplace/offerTypes/default/offers/default/plans/default/resources/{RESOURCE_GUID}',
        'quantity': user_count,
        'dimension': METER_ID,
        'effectiveStartTime': 'UTC_START_TIME',  # e.g., '2021-09-01T00:00:00Z'
        'planId': 'default',
        'armRegionName': 'global'
    }
    
    response = requests.post(report_url, headers=headers, json=usage_data)
    return response.json()

# Example of reporting 10 users
response = report_usage(10)
print(response)