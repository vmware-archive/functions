import base64
import tempfile
import os.path

#pip install kubernetes
from kubernetes import client, config

# pip install minio
from minio import Minio
from minio.error import ResponseError

# Use Pillow for thumbnail
from PIL import Image

config.load_incluster_config()

v1=client.CoreV1Api()

for secrets in v1.list_secret_for_all_namespaces().items:
    if secrets.metadata.name == 'minio-minio-user':
        access_key = base64.b64decode(secrets.data['accesskey'])
        secret_key = base64.b64decode(secrets.data['secretkey'])

# Replace the DNS below with the minio service name (helm release name -svc)
client = Minio('minio-minio-svc:9000',
                  access_key=access_key,
                  secret_key=secret_key,
                  secure=False)

def thumbnail(event, context):
    bucket = os.path.dirname(event['data']['Key'])
    _, file_extension = os.path.splitext(event['data']['Key'])
    filename = os.path.basename(event['data']['Key'])

    print file_extension.upper()

    if file_extension.upper() != ".JPEG":
        return "Not a picture"

    if event['data']['EventType'] == "s3:ObjectCreated:Put" and bucket == 'foobar':

        tf = tempfile.NamedTemporaryFile(delete=False)
        tf_thumb = tempfile.NamedTemporaryFile(delete=False)

        try:
            client.fget_object(bucket, filename, tf.name)
        except ResponseError as err:
            print err

        size=(120,120)
        img = Image.open(tf.name)
        img.thumbnail(size)
        img.save(tf_thumb.name, "JPEG")

        # puts the thumbnail in a thumbnail bucket
        thumb_name = filename + '.thumb'
        try:
            client.fput_object('thumb',thumb_name,tf_thumb.name)
        except ResponseError as err:
            print err

    else:
        print "Minio file deletion event"

    return "Thumbnail creation triggered"
