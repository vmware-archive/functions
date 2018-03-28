# Parse PDF files to obtain plain text stored in a MongoDbB collection

Make sure `minikube` and `kubeless` are installed. See the respective installation guides:
* [Minikube](https://github.com/kubernetes/minikube#installation)
* [Kubeless](http://kubeless.io/docs/quick-start/)


## Prepare the environment

This example uses the Minio S3 clone to show case a kubeless pubsub function. Minio is configured to send notifications to Kafka, then a function consume those events to parse PDF files using Apache Tika and store the plain text in a MongoDB collection.

### Deploy Minio, Apache Tika and MongoDB via Helm

```bash
helm repo add kubeless-functions-charts https://kubeless-functions-charts.storage.googleapis.com
helm install --name minio kubeless-functions-charts/minio --set serviceType=NodePort
helm install --name tika kubeless-functions-charts/tika-server --set serviceType=NodePort
helm install --name mongodb kubeless-functions-charts/mongodb --set serviceType=NodePort
```

### Configure Minio


You will need the Minio [client](https://github.com/minio/mc) `mc`:

```bash
brew install minio-mc
```

The following are Minio specific, it assumes your are using minikube on `192.168.99.100` and the minio service is running on port `32751`. You can check your IP with `$ minikue ip` command and the port with `$ kubectl get svc`

```bash
mc config host add localminio http://192.168.99.100:32751 foobar foobarfoo
```

Create an `input` and a `done` bucket:

```bash
$ mc mb localminio/input
$ mc mb localminio/done
```

Turn on events for a `input` bucket for .pdf files:

```bash
mc events add localminio/input arn:minio:sqs:us-east-1:1:kafka --events put,delete --suffix .pdf
```

## Deploy the function with kubeless

### 1. Deploy

In order to deploy the function run the following command:

```bash
$ kubeless function deploy ocr --from-file ocr.py --handler ocr.handler --runtime python2.7 --trigger-topic s3 --dependencies requirements.txt
```

You can list the function with `kubeless function ls` and you should see the following:

```
$ kubeless function ls
NAME         	NAMESPACE	HANDLER              	RUNTIME  	DEPENDENCIES     	STATUS
ocr          	default  	ocr.handler          	python2.7	minio            	1/1 READY
             	         	                     	         	tika
             	         	                     	         	pymongo
             	         	                     	         	kubernetes==2.0.0
```

### 2. Trigger the function

To trigger the function you only need to upload a PDF file to the `input` bucket using the Minio web interface of the minio client.

Login to the Minio UI and upload some file to the `input` bucket.

```bash
minikube service minio-minio-svc
```

### 3. Check results

You should check that the text has been stored in MongoDB. For that first get your mongodb pod:

``` $ kubectl get pods -o=custom-columns=NAME:.metadata.name -l app=mongodb-mongodb
NAME
mongodb-mongodb-123307584-5hf33
```

And now execute the following:

```bash
$ kubectl exec -it mongodb-mongodb-123307584-5hf33 -- mongo --eval "printjson(db.processed.findOne())" localhost/ocr
```
