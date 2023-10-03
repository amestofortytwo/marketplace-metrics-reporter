import os
import requests
from datetime import datetime

# Configuration
TENANT_ID = os.environ.get('TENANT_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')  # Microsoft Entra Identity Application ID
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
RESOURCE = 'https://cloudapi.deployment.marketplace.azure.com/'
GRANT_TYPE = 'client_credentials'
METER_ID = os.environ.get('UserCount')  # ID for metering dimension
CUSTOMER_SUBSCRIPTION_GUID = os.environ.get('CUSTOMER_SUBSCRIPTION_GUID')  # When a customer subscribes
RESOURCE_GUID = os.environ.get('RESOURCE_GUID')  # Marketplace resource ID
GROUP_ID = os.environ.get('GROUP_ID')  # AD group ID
GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0/"

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

def get_ad_group_user_count():
    token = get_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{GRAPH_ENDPOINT}groups/{GROUP_ID}/members/$count", headers=headers)
    if response.status_code == 200:
        return response.json()['@odata.count']
    else:
        print(response.json())
        return 0

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
        'effectiveStartTime': datetime.utcnow().isoformat() + 'Z',  # Current UTC time in ISO 8601 format
        'planId': 'default',
        'armRegionName': 'global'
    }
    
    response = requests.post(report_url, headers=headers, json=usage_data)
    return response.json()

# Report actual user count from AD group to Azure Marketplace
user_count = get_ad_group_user_count()
response = report_usage(user_count)
print(response)
