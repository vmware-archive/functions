import json
import yaml

from kubernetes import client, config

config.load_incluster_config()

d1=client.ExtensionsV1beta1Api()

nginx= """
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
"""

deployment = yaml.load(nginx)

def handler(event):
    try:
        if event['type'] == "ADDED" and event['object']['kind'] == "Namespace":
            print "Event: %s %s %s" % (event['type'], event['object']['kind'], event['object']['metadata']['name'])
            res = d1.create_namespaced_deployment(body=deployment, namespace=event['object']['metadata']['name'])
    except:
        print event.keys()
        print type(event)
        print str(event)
    return True
