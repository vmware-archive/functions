Introduction
============

This demo shows how to interconnect services with kubeless functions.

We're assuming you already have `minikube` and `kubectl` installed locally 

This demo implements an OCR (Optical Character Recognition) pipeline.

PDF files are uploaded to an object store (Minio) which notifies our function via webhook. The function will
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


# Second README (TODO: Cleanup)

# OCR Pipeline
As a application developer, I want to create an OCR pipelline so when I drop a file in Minio object store, it gets automatically parsed by Apache Tika  and the text gets stored in an MongoDB collection, using serverless functions provided by Kubeless.

## TL;DR;

```console
$ helm install ./ocr-pipeline
```

## Introduction

This chart bootstraps an [OCR](https://en.wikipedia.org/wiki/Optical_character_recognition) deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

It makes use of [Minio](https://github.com/kubernetes/charts/tree/master/stable/minio), [Apache Tika](https://github.com/bitnami/charts/tree/tika-server/incubator/tika-server) and [MongoDB](https://github.com/kubernetes/charts/tree/master/stable/mongodb) as Object Store, Translator and Document Store.

## Prerequisites

- Kubernetes 1.4+ with Beta APIs enabled
- PV provisioner support in the underlying infrastructure

## Installing the Chart

To install the chart with the release name `my-release`:

```console
$ helm install --name my-release ./ocr-pipeline
```


## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```console
$ helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

The function itself doesn't require any kind of configuration, so the values stored in `values.yaml`
are chart's defaults from Minio, MongoDB and Apache Tika charts. 

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example,

```console
$ helm install --name my-release \
  --set minio.minioConfig.webhook.endpoint=someURL \ 
    ./ocr-pipeline
```

The above command sets Minio's webhook URL to be fired when a file is uploaded.

Alternatively, a YAML file that specifies the values for the above parameters can be provided while installing the chart. For example,

```console
$ helm install --name my-release -f values.yaml i./ocr-pipeline
```

> **Tip**: You can use the default [values.yaml](values.yaml)

## Persistence

Persistent Volume Claims are used to keep the data across deployments. This is known to work in GCE, AWS, and minikube.
See the [Configuration](#configuration) section to configure the PVC or to disable persistence.

