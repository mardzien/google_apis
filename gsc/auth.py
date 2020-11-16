import argparse
import httplib2

from googleapiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools


CLIENT_SECRETS_PATH = "../key/secret_key.json"


def authorize_creds():
    print('Authorizing Creds')
    # Variable parameter that controls the set of resources that the access token permits.
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

    # Path to client_secrets.json file

    # Create a parser to be able to open browser for Authorization
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])

    # Creates an authorization flow from a clientsecrets file.
    # Will raise InvalidClientSecretsError for unknown types of Flows.
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS_PATH, scope=SCOPES,
        message=tools.message_if_missing(CLIENT_SECRETS_PATH))

    # Prepare credentials and authorize HTTP
    # If they exist, get them from the storage object
    # credentials will get written back to the 'authorizedcreds.dat' file.
    storage = file.Storage('../key/authorizedcreds.dat')
    credentials = storage.get()

    # If authenticated credentials don't exist, open Browser to authenticate
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)  # Add the valid creds to a variable

    # Take the credentials and authorize them using httplib2
    http = httplib2.Http()  # Creates an HTTP client object to make the http request
    http = credentials.authorize(http=http)  # Sign each request from the HTTP client with the OAuth 2.0 access token
    webmasters_service = build('webmasters', 'v3',
                               http=http)  # Construct a Resource to interact with the API using the Authorized HTTP Client.

    print('Auth Successful')
    return webmasters_service


def initialize_analyticsreporting():
    """Initializes the analyticsreporting service object.

    Returns:
    analytics an authorized analyticsreporting service object.
    """
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS_PATH, scope=SCOPES,
        message=tools.message_if_missing(CLIENT_SECRETS_PATH))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage('analyticsreporting.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', http=http)

    return analytics


# Create Function to execute your API Request
def execute_request(service, property_uri, request):
    return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()
