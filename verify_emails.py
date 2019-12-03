# https://account.cloudmersive.com/keys

from __future__ import print_function
import time
import cloudmersive_validate_api_client
from cloudmersive_validate_api_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Apikey
configuration = cloudmersive_validate_api_client.Configuration()
configuration.api_key['Apikey'] = 'a7fa4e04-df08-4b69-a5f1-fcd1dbc34b88'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Apikey'] = 'Bearer'

# create an instance of the API class
api_instance = cloudmersive_validate_api_client.EmailApi(cloudmersive_validate_api_client.ApiClient(configuration))
email = 'lhough@arizonatile.com' # str | Email address to validate, e.g. \"support@cloudmersive.com\".    The input is a string so be sure to enclose it in double-quotes.

try:
    # Fully validate an email address
    api_response = api_instance.email_full_validation(email)
    # api_response = api_instance.email_address_get_servers(email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailApi->email_full_validation: %s\n" % e)