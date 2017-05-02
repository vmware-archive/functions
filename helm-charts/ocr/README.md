Introduction
============

This demo needs at least Helm 2.3.0  and Kubeless 0.0.11

This demo shows how to interconnect services with kubeless functions. All the architecture is packaged with Helm, 
a Kubernetes package manager which provide us a easy way to manage applications and his dependencies. 

We're assuming you already have Minikube and Kubectl installed locally 

This demo implements a OCR pipeline.
PDF files are uploaded to a object store (Minio) which notifies to our function via webhook. The function will
fetch the recently uploaded file and send it to Apache Tika in order to get the text from the PDF. The result
json document is stored finally in a MongoDB document. 


Install Kubeless
================
Install latest Kubeless version from https://github.com/bitnami/kubeless/releases

Install Helm
============
Install latest Helm version from  https://github.com/kubernetes/helm#install

Install Minio client
====================
Install latest minio client from https://minio.io/downloads/#minio-client

Install curl 
============
Install curl from https://curl.haxx.se/download.html or from  your OS package manager


Setup the demo environment
==========================
We have coded a Makefile to make you live easier. Feel free to examine it.

Execute `make setup` to install kubeless and Helm Tiller into your minikube cluster

  $ make setup

Wait a couple of minutes while the pods starts

Install the ocr-pipeline helm chart 
===================================

Execute `make install` to install the `ocr-pipeline` helm chart and associated dependencies

  $ make install

Wait a couple of minutes while the pods starts. Minio pod tends to crash until our function is ready
so it can crash 5 o 6 times. This happens because Minio tries to check the function before launching 
his own the service, and if the function is not listening, the check fails and makes the pod restart. 

Execute the test
=================

Execute `make test` to install the `ocr=pipeline` helm chart and associated dependencies
  $ make test 

It fetchs a sample PDF to feed up OCR system powered by Apache Tika. 

This sample file includes most common tags used in PDF files.

   http://www.tra.org.bh/media/document/sample10.pdf


Wait a few seconds while Tika parses the document (OCR is a time consuming task) and execute:

POD=`kubectl get pods -l app=ocr-mongodb  | awk '/ocr-mongo/{print $1}'`
kubectl exec -it $POD --  mongo --eval "printjson(db.processed.findOne())" localhost/ocr

You gonna see the JSON document stored on MongoDB.

Finally, you can run `make clean` in order to clean up the installed resources
