import time
import json
import base64
import tempfile
import urllib

# pip install slackclient
from slackclient import SlackClient

# pip install kubernetes
from kubernetes import client, config
from kubernetes.client import configuration
from kubernetes.client.apis import core_v1_api
from kubernetes.client.rest import ApiException

# pip install minio
from minio import Minio
from minio.error import ResponseError

# load incluster_config
config.load_incluster_config()
v1=client.CoreV1Api()

# In order to avoid issue with kubernetes hostnames when using python 2
configuration.assert_hostname = False

# Get minio and slack secrets
for secrets in v1.list_secret_for_all_namespaces().items:
    if secrets.metadata.name == 'minio-minio-user':
        access_key = base64.b64decode(secrets.data['accesskey'])
        secret_key = base64.b64decode(secrets.data['secretkey'])
    if secrets.metadata.name == 'slack-token':
        slack_token = base64.b64decode(secrets.data['token'])


# Replace the DNS below with the minio service name (helm release name -svc)
client = Minio('minio-minio-svc:9000',
                  access_key=access_key,
                  secret_key=secret_key,
                  secure=False)

# Slack token
sc = SlackClient(slack_token)

pod_name = 'tensorflow-inception'

# Check if pod already exists
resp = None
try:
    resp = v1.read_namespaced_pod(name=pod_name,
                                   namespace='default')
except ApiException as e:
    if e.status != 404:
        print("Unknown error: %s" % e)
        exit(1)

# Create pod if not exists
if not resp:
    print("Pod %s does not exits. Creating it..." % pod_name)
    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': pod_name
        },
        'spec': {
            'containers': [{
                'image': 'bitnami/tensorflow-inception',
                'name': 'tf-inception'
            }]
        }
    }
    resp = v1.create_namespaced_pod(body=pod_manifest, namespace='default')
    while True:
        resp = v1.read_namespaced_pod(name=pod_name, namespace='default')
        print("resp.status.phase is %s" % resp.status.phase)
        if resp.status.phase != 'Pending':
            print("resp.status.phase is not Pending...exiting")
            break
        time.sleep(1)
    print("Pod %s successfully created" % pod_name)

    # Install minio client in tensorflow-inception pod to retrieve the image
    exec_command = ['/bin/sh',
                    '-c',
                    'curl -JLO https://dl.minio.io/client/mc/release/linux-amd64/mc && \
                    chmod a+x mc && \
                    ./mc config host add remoteminio http://minio-minio-svc:9000 %s %s' % (access_key, secret_key)]

    # Exec command in container and retrieve response
    resp = v1.connect_get_namespaced_pod_exec(pod_name, 'default', command=exec_command, stderr=True, stdin=False, stdout=True, tty=False)
    print("Minio client installed in %s pod. Output: %s" % pod_name, resp)

print("Pod ready to accept commands")


def handler(context):

    if context['EventType'] == "s3:ObjectCreated:Put":

        tf = tempfile.NamedTemporaryFile(delete=False)
        bucket = context['Key'].split('/')[0]
        filename = context['Key'].split('/')[1]

        # Fetching source file from Minio to send it to slack
        try:
            print 'Fetching file'
            client.fget_object(bucket, filename, tf.name)
        except ResponseError as err:
            print 'Error fetching file'
            print err

        # Retrieve image from minio and send to tensorflow-serving
        exec_command = ['/bin/sh',
                        '-c',
                        './mc cp remoteminio/images/' + filename + ' . > /dev/null 2>&1 && \
                        inception_client --server=tensorflow-inception-tensorflow-serving:9000 --image=' + filename]

        # Exec command in container and retrieve response
        resp = v1.connect_get_namespaced_pod_exec(pod_name, 'default', command=exec_command, stderr=True, stdin=False, stdout=True, tty=False)

        print("Response: " + resp)


        msg = "New image uploaded to Minio and categorized by TensorFlow Inception"
        attachments = """[{"fallback": "New image upload to Minio and categorized by TensorFlow Inception",
                         "pretext": "The above image called %s was uploaded to bucket %s",
                         "title": '%s',
                         "text": '%s',
                         "color": "#7CD197"}]""" % (filename, bucket, filename, resp)

        # Send image and tensorflow-inception output to slack
        sc.api_call("files.upload", filename=filename, channels='#bots-tests', file=open(tf.name, 'rb'))
        sc.api_call("chat.postMessage", channel="#bots-tests", text=msg, attachments=attachments)



    return "Image and tensorflow-inception output sent to SLACK"
