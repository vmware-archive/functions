import json
import base64

from slackclient import SlackClient
from kubernetes import client, config

config.load_incluster_config()

v1=client.CoreV1Api()

for secrets in v1.list_secret_for_all_namespaces().items:
    if secrets.metadata.name == 'slack':
        token = base64.b64decode(secrets.data['token'])

sc = SlackClient(token)

def remind():
    return sc.api_call(
                       "chat.postMessage",
                       channel="#kubeless",
                       text="""<!here> please jump into the weekly call for discussing things going on Kubeless.
Link to access: https://meet.google.com/rbr-gcjp-xxz
Meeting notes: https://docs.google.com/document/d/1-OsikjjQVHVFoXBHUbkRogrzzZijQ9MumFpLfWCCjwk/edit?usp=sharing
                       """,
                       as_user=True
                      )
