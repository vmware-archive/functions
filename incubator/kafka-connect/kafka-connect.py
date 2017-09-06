import json
import base64
from slackclient import SlackClient
from kubernetes import client, config

config.load_incluster_config()
v1=client.CoreV1Api()

#Get slack secret
for secrets in v1.list_secret_for_all_namespaces().items:
    if secrets.metadata.name == 'slack':
        token = base64.b64decode(secrets.data['token'])
sc = SlackClient(token)

print "==> Function ready to listen events..."

def handler(context):
    util_data = False
    try:
        if 'op' in context['payload']:
            util_data = True;
    except:
        util_data = False

    if util_data == True:
        # CREATE operation
        if context['payload']['op'] == "c":
            first_name = context['payload']['after']['first_name'];
            last_name = context['payload']['after']['last_name'];
            email = context['payload']['after']['email'];
            msg = "Create operation: Added user %s %s with email %s" % (first_name, last_name, email)
            print msg;
        # DELETE operation
        elif context['payload']['op'] == "d":
            first_name = context['payload']['before']['first_name'];
            last_name = context['payload']['before']['last_name'];
            email = context['payload']['before']['email'];
            msg = "Delete operation: Deleted user %s %s with email %s" % (first_name, last_name, email)
            print msg;
        # UPDATE operation
        elif context['payload']['op'] == "u":
            row_id = context['payload']['before']['id'];
            first_name_before = context['payload']['before']['first_name'];
            last_name_before = context['payload']['before']['last_name'];
            email_before = context['payload']['before']['email'];
            first_name_after = context['payload']['after']['first_name'];
            last_name_after = context['payload']['after']['last_name'];
            email_after = context['payload']['after']['email'];
            msg = "Update operation in row with id %s: \n Old value: Name: %s %s and Email: %s \n New value: Name: %s %s and Email %s" % (row_id, first_name_before, last_name_before, email_before, first_name_after, last_name_after, email_after)
            print msg;
        else:
            msg = "Unrecognized operation"
            print msg;

        sc.api_call("chat.postMessage", channel="#bot", text=msg)

    else:
        print "Payload is empty. Useless event..."

    return "Function executed\n"
