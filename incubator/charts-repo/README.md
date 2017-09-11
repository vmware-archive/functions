# Manage a Helm Chart Repository using Minio and Kubeless

## Create 'charts' topic

```console
$ kubeless topic create charts
```

## Deploy Minio using Helm

```console
$ helm install -n minio stable/minio --set minioConfig.kafka.enable=true,minioConfig.kafka.brokers="[\"kafka.kubeless:9092\"]",minioConfig.kafka.topic=charts
```

## Configure Minio client to connect to Minio and setup

```console
$ mc config host add myminio $MINIO_HOST $MINIO_ACCESS_KEY $MINIO_SECRET_KEY
$ mc mb myminio/charts
$ mc policy download myminio/charts
$ mc events add myminio/charts arn:minio:sqs:us-east-1:1:kafka --events put --suffix .tgz
```

## Deploy this function

```console
$ kubeless function deploy charts-repo-indexer --from-file indexer.js --handler indexer.handler --runtime nodejs8 --trigger-topic charts --dependencies package.json --env REPO_URL=$MINIO_HOST/charts,MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY,MINIO_SECRET_KEY=$MINIO_SECRET_KEY
```

## Add a chart to the bucket

```console
$ helm fetch stable/redis
$ mc cp redis*.tgz myminio/charts
```

## Add chart repository to Helm

```console
$ helm repo add myminio $MINIO_HOST/charts
$ helm repo update
$ helm search myminio/
```
