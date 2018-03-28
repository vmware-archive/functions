import json
import base64
from kubernetes import client, config

config.load_incluster_config()
v1=client.CoreV1Api()

#Get slack secret
for secrets in v1.list_secret_for_all_namespaces().items:
    if secrets.metadata.name == 'slack':
        token = base64.b64decode(secrets.data['token'])

print "==> Function ready to listen events..."

def handler(event, context):
    util_data = False
    try:
        if 'op' in event['data']['payload']:
            util_data = True;
    except:
        util_data = False

    if util_data == True:
        # CREATE operation
        if event['data']['payload']['op'] == "c":
            first_name = event['data']['payload']['after']['first_name'];
            last_name = event['data']['payload']['after']['last_name'];
            email = event['data']['payload']['after']['email'];
            msg = "Create operation: Added user %s %s with email %s" % (first_name, last_name, email)
            print msg;
        # DELETE operation
        elif event['data']['payload']['op'] == "d":
            first_name = event['data']['payload']['before']['first_name'];
            last_name = event['data']['payload']['before']['last_name'];
            email = event['data']['payload']['before']['email'];
            msg = "Delete operation: Deleted user %s %s with email %s" % (first_name, last_name, email)
            print msg;
        # UPDATE operation
        elif event['data']['payload']['op'] == "u":
            row_id = event['data']['payload']['before']['id'];
            first_name_before = event['data']['payload']['before']['first_name'];
            last_name_before = event['data']['payload']['before']['last_name'];
            email_before = event['data']['payload']['before']['email'];
            first_name_after = event['data']['payload']['after']['first_name'];
            last_name_after = event['data']['payload']['after']['last_name'];
            email_after = event['data']['payload']['after']['email'];
            msg = "Update operation in row with id %s: \n Old value: Name: %s %s and Email: %s \n New value: Name: %s %s and Email %s" % (row_id, first_name_before, last_name_before, email_before, first_name_after, last_name_after, email_after)
            print msg;
        else:
            msg = "Unrecognized operation"
            print msg;

    else:
        print "Payload is empty. Useless event..."

    return "Function executed"
