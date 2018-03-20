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

def remind(event, context):
    return sc.api_call(
                       "chat.postMessage",
                       channel="#kubeless",
                       text="""<!here> please jump into the weekly call for discussing things going on Kubeless.
                       
Join from PC, Mac, Linux, iOS or Android: https://zoom.us/j/536180327

Or iPhone one-tap :
    US: +16699006833,,536180327#  or +16465588656,,536180327#
Or Telephone:
    Dial(for higher quality, dial a number based on your current location)：
        US: +1 669 900 6833  or +1 646 558 8656
    Meeting ID: 536 180 327
    International numbers available: https://zoom.us/zoomconference?m=H8zcNnFc19vCkVdoEHBkxK61gwDvyawC

Meeting notes: https://docs.google.com/document/d/1-OsikjjQVHVFoXBHUbkRogrzzZijQ9MumFpLfWCCjwk/edit?usp=sharing
                       """,
                       as_user=True
                      )
