# Send messages on objects upload to a bucket

Make sure `minikube` and `kubeless` are installed. See the respective installation guides:
* [Minikube](https://github.com/kubernetes/minikube#installation)
* [Kubeless](https://github.com/kubeless/kubeless/blob/master/README.md#usage)


## Prepare the environment

This example uses the Minio S3 clone to show case a kubeless pubsub function. Minio is configured to send notifications to Kafka, a function consumes those events and performs actions.

### Create Minio and Slack kubernetes secrets

In order to access to the minio object storage and to send messages to a slack channel you need

The access_key and secret_key for minio are configured in the helm chart template. You can edit the file values.yml and specify the keys you want to use. This secret will be deployed to kubernetes while deploying Minio so no further action is required.

For the slack secret you need to obtain your slack token from [this page](https://api.slack.com/custom-integrations/legacy-tokens) and then deploy a secret to kubernetes with this command:

```bash
kubectl create secret generic slack --from-literal=token=YOUR_SLACK_TOKEN
```

### Deploy Minio via Helm

```bash
helm repo add kubeless-functions-charts https://kubeless-functions-charts.storage.googleapis.com
helm install --name minio kubeless-functions-charts/minio --set serviceType=NodePort
```

### Configure Minio


You will need the Minio [client](https://github.com/minio/mc) `mc`:

```bash
brew install minio-mc
```

The following are Minio specific, it assumes your are using minikube on `192.168.99.100` and the minio service is running on port `32751`

```bash
export MINIO_HOST=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
export MINIO_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services minio-minio-svc)
mc config host add localminio http://$MINIO_HOST:$MINIO_PORT foobar foobarfoo
```

Create a foobar bucket:

```bash
$ mc mb localminio/foobar
```

Turn on events for a `foobar` bucket:

```bash
mc events add localminio/foobar arn:minio:sqs:us-east-1:1:kafka --events put
```

Check bucket

```bash
mc ls localminio/foobar
```


## Deploy the function with kubeless

### 1. Deploy

In order to deploy the function run the following command:

```bash
$ kubeless function deploy minio-slack --from-file minio-slack.py --handler minio-slack.handler --runtime python2.7 --trigger-topic s3 --dependencies requirements.txt
```

You can list the function with `kubeless function ls` and you should see the following:

```
$ kubeless function ls
minio-slack  	default  	minio-slack.handler  	python2.7	slackclient      	1/1 READY
             	         	                     	         	kubernetes==2.0.0
             	         	                     	         	minio
```

### 2. Invoke

To trigger the function you only need to upload a file to the `foobar` bucket using the Minio web interface of the minio client.

Login to the Minio UI and upload some file to the `foobar` bucket.

```bash
minikube service minio-minio-svc
```
