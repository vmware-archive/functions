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


> **Tip**: List all releases using `helm list`

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

