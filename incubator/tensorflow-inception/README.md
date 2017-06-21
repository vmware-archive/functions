# TensorFlow Inception Example

## Introduction

This example uses the Minio S3 clone to show case a kubeless pubsub function.
Minio is configured to send notifications to Kafka, a function consumes those events and performs actions.

The Minio access keys are stored as a Kubernetes secret

### 1. Install kubeless on your kubernetes cluster

```bash
$ kubeless install
```

### 2. Deploy TensorFlow Inception via Helm

From this folder:

```bash
$ helm install --name tensorflow-inception ./charts/tensorflow-inception --set serviceType=NodePort
```

> NOTE: It can take a couple of minutes to the tensorflow deployment to be in running state as it need to run a Jon to populate the training data.

### 3. Deploy Minio via Helm

If you have cloned the kubeless repo:

```bash
$ helm install --name minio ./charts/minio --set serviceType=NodePort
```

This will use the default values in `./charts/minio/values.yaml`

Check the logs of the Minio pod for configuration info.

### 4. Configure Minio

You will need the [Minio client](https://github.com/minio/mc) `mc`:

```bash
$ brew install minio-mc
```

The following are Minio specific, it assumes your are using minikube on `192.168.99.100`

```bash
$ mc config host add localminio http://192.168.99.100:32751 foobar foobarfoo
```

Create the bucket:

```bash
$ mc mb localminio/images
```

Turn on events for a `images` bucket:

```bash
$ mc events add localminio/images arn:minio:sqs:us-east-1:1:kafka --events put
```

Check bucket

```bash
$ mc ls localminio/images
```

### 5. Create kubernetes secret for slack token

In order to access to Slack we need the token to be available from the kubeless function. To keep it secure we will use kubernetes secrets to store this info and we will retrieve it from the function itself.

```bash
$ kubectl create secret generic slack-token --from-literal=token=YOUR_SLACK_TOKEN
```

We also need the `access_key` and `secret_key` in order to access to the Minio server but a kubernetes secret containing this values was already created installing the helm chart.


### 6. Deploy minio-tf-slack-bot function

```bash
kubeless function deploy minio-tf-slack-bot --trigger-topic s3 --from-file bot.py --handler bot.handler --runtime python2.7 --dependencies requirements.txt
```
