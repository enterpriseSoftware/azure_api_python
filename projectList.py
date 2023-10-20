import os 
from dotenv import load_dotenv

load_dotenv()

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint

# Fill in with your personal access token and org URL
personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
organization_url =  os.getenv('ORGANIZATION_URL')

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
try:
   core_client = connection.clients.get_core_client()
except:
    print('Auth failed connection.clients.get_core_client()')
      
# Get the first page of projects
try:
    get_projects_response = core_client.get_projects()
except: 
    print('Auth failed, core_client.get_projects()')

index = 0
while get_projects_response is not None:
    for project in get_projects_response.value:
        pprint.pprint("[" + str(index) + "] " + project.name)
        index += 1
    if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
        # Get the next page of projects
        get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
    else:
        # All projects have been retrieved
        get_projects_response = None