# Send messages to slack on changes to a mysql table

Make sure `minikube` and `kubeless` are installed. See the respective installation guides:
* [Minikube](https://github.com/kubernetes/minikube#installation)
* [Kubeless](https://github.com/kubeless/kubeless/blob/master/README.md#usage)


## Prepare the environment

This example uses the Minio S3 clone to show case a kubeless pubsub function. Minio is configured to send notifications to Kafka, a function consumes those events and performs actions.

### Create Slack kubernetes secrets

Obtain your slack token from [this page](https://api.slack.com/custom-integrations/legacy-tokens) and then deploy a secret to kubernetes with this command:

```bash
$ kubectl create secret generic slack --from-literal=token=YOUR_SLACK_TOKEN
```

### Add kubeless-functions-charts repository

```bash
$ helm repo add kubeless-functions-charts https://kubeless-functions-charts.storage.googleapis.com
```


### Deploy Debezium MySQL via Helm

```bash
$ helm install --name debezium-mysql kubeless-functions-charts/debezium-mysql --set service.type=NodePort
```

### Deploy Debezium Kafka-Connect via Helm

```bash
$ helm install --name debezium-connect kubeless-functions-charts/debezium-connect --set service.type=NodePort
```

### Get kafka-connect host and port

```bash
$ export KAFKA_CONNECT_HOST=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
$ export KAFKA_CONNECT_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services debezium-connect-debezium-connect)
```

### Start connector monitoring

```bash
$ curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" $KAFKA_CONNECT_HOST:$KAFKA_CONNECT_PORT/connectors/ -d '{ "name": "inventory-connector", "config": { "connector.class": "io.debezium.connector.mysql.MySqlConnector", "tasks.max": "1", "database.hostname": "debezium-mysql-debezium-mysql", "database.port": "3306", "database.user": "debezium", "database.password": "dbz", "database.server.id": "184054", "database.server.name": "dbserver1", "database.whitelist": "inventory", "database.history.kafka.bootstrap.servers": "kafka.kubeless:9092", "database.history.kafka.topic": "dbhistory.inventory" } }'
```

## Deploy the function with kubeless

### 1. Deploy

In order to deploy the function run the following command:

```bash
$ kubeless function deploy kafka-connect --from-file kafka-connect.py --handler kafka-connect.handler --runtime python2.7 --trigger-topic  dbserver1.inventory.customers --dependencies requirements.txt
```

You can list the function with `kubeless function ls` and you should see the following:

```
$ kubeless function ls

NAME         	NAMESPACE	HANDLER              	RUNTIME  	TYPE  	TOPIC
kafka-connect	default  	kafka-connect.handler	python2.7	PubSub	dbserver1.inventory.customers
```


## Deploy the function with the Serverless plugin

Alternatively you can deploy the function with the Serverless plugin for Kubeless.
Make sure `serverless` is installed. You can see the installation instructions [here](https://github.com/serverless/serverless#quick-start).

### 1. Install Service Dependencies
Run `npm install` in this directory to download the modules from `package.json`.

### 2. Deploy
Run `serverless deploy` in order to deploy the function defined in `serverless.yml`

```bash
$ serverless deploy
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Deploying function kafka-connect...
Serverless: Function kafka-connect succesfully deployed
```

**For more information on the Serverless Kubeless plugin, please see the project repository: [https://github.com/serverless/serverless-kubeless](https://github.com/serverless/serverless-kubeless).**

## Invoke the function

To trigger the function you should log into the mysql container, open a client session and make som INSERT, UPDATE or DELETE operation in the customers table.


```bash
$ kubectl get pods
$ kubectl exec -it <mysql-pod> -- bash
$ mysql -uroot -pdebezium
mysql> use inventory;
mysql> UPDATE customers SET first_name='Anne Marie' WHERE id=1004;
mysql> INSERT INTO customers VALUES (default, "Sarah", "Thompson", "kitt@acme.com");
mysql> DELETE FROM customers WHERE id=1004;
```
