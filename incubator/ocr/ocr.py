import base64
import tempfile
import json
import tika
import pymongo
tika.TikaClientOnly = True
from tika import parser
from pymongo import MongoClient
from kubernetes import client, config
from minio import Minio
from minio.error import ResponseError
      
config.load_incluster_config()
      
v1=client.CoreV1Api()
      
for secrets in v1.list_secret_for_all_namespaces().items:
    if secrets.metadata.name == 'minio-minio-user':
        access_key =  base64.b64decode(secrets.data['accesskey'])
        secret_key =  base64.b64decode(secrets.data['secretkey'])

mongo = MongoClient('mongodb-mongodb', 27017)

client = Minio('minio-minio-svc:9000', 
                  access_key=access_key,
                  secret_key=secret_key, 
                  secure=False)

print('Loading function...')
      
def handler(context):
  if context['EventType'] == "s3:ObjectCreated:Put" : 
        tf = tempfile.NamedTemporaryFile(delete=False)
        bucket = context['Key'].split('/')[0]
        filename = context['Key'].split('/')[1]
      
        # Fetching source file from Minio
        try:
            print('Fetching file')
            client.fget_object(bucket, filename, tf.name)
        except ResponseError as err:
            print('Error fetching file')
            print err

        # OCR text extraction performed by Tika
        print 'Sending file to Tika'
        parsed = parser.from_file(tf.name, 'http://tika-tika-server:80/tika')
        ocrdata = json.dumps(parsed, ensure_ascii=True)

        # MongoDB document insertion 
        db = mongo['ocr']
        result = db.processed.insert_one(parsed)
        print 'Document Saved!'
        print('Document proccessed: {0}'.format(result.inserted_id))

        # move OCRd file to done bucket 
        try:
            # Copy from input bucket to done bucket
            fullpath = 'input/' + filename 
            client.copy_object('done', filename, fullpath)
            # Remove from input bucket
            client.remove_object('input', filename)
        except ResponseError as err:
            print err
  else:
       print "Minio file deletion event"
      
  return "OCR Finished"
