Debezium Kafka Connect
=====

[Debezium Kafka Connect](http://debezium.io/docs/tutorial/) is a server that can monitor a MySQL database and send the events to a kafka-server.

Introduction
------------

This chart bootstraps a Kafka Connect deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

Prerequisites
-------------

-	Kubernetes 1.4+ with Beta APIs enabled for default standalone mode.
-	PV provisioner support in the underlying infrastructure.

Installing the Chart
--------------------

Install this chart using:

```bash
$ helm repo add kubeless-functions-charts https://kubeless-functions-charts.storage.googleapis.com
$ helm install kubeless-functions-charts/debezium-connect
```

The command deploys Kafka-Connect on the Kubernetes cluster in the default configuration. The [configuration](#configuration) section lists the parameters that can be configured during installation.

### Release name

An instance of a chart running in a Kubernetes cluster is called a release. Each release is identified by a unique name within the cluster. Helm automatically assigns a unique release name after installing the chart. You can also set your preferred name by:

```bash
$ helm install --name my-release kubeless-functions-charts/debezium-connect
```

### Updating Kafka-Connect configuration via Helm

[ConfigMap](https://kubernetes.io/docs/user-guide/configmap/) allows injecting containers with configuration data even while a Helm release is deployed.

To update your Kafka-Connect server configuration while it is deployed in a release, you need to

1. Check all the configurable values in the Kafka-Connect chart using `helm inspect values kubeless-functions-charts/debezium-connect`.
2. Override the `config` settings in a YAML formatted file, and then pass that file like this `helm upgrade -f config.yaml kubeless-functions-charts/debezium-connect`.
3. Restart the Kafka-Connect server(s) for the changes to take effect.

You can also check the history of upgrades to a release using `helm history my-release`. Replace `my-release` with the actual release name.

Uninstalling the Chart
----------------------

Assuming your release is named as `my-release`, delete it using the command:

```bash
$ helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

Configuration
-------------

The following tables lists the configurable parameters of the Kafka-Connect chart and their default values.

| Parameter                  | Description                         | Default                                                 |
|----------------------------|-------------------------------------|---------------------------------------------------------|
| `image.repository`         | Kafka-Connect image name            | `debezium/kafka-connect`                                |
| `image.tag`                | Kafka-Connect image tag.            | `0.5`                                                   |
| `image.pullPolicy`         | Image pull policy                   | `IfNotPresent`                                                |
| `service.name`             | Kubernetes service name             | `mysql`                                                 |
| `service.type`             | Kubernetes service type             | `ClusterIP`                                             |
| `service.internalPort`     | Kubernetes service internal port    | `8083`                                                  |
| `service.externalPort`     | Kubernetes service externam port    | `8083`                                                  |
| `config.groupId`           | Kafka group Id                      | `debezium`                                              |
| `config.configStorageTopic`| Topic to store the configs          | `mysqlUser`                                             |
| `config.offsetStorageTopic`| Topic to store the offsets          | `mysqlpw`                                               |
| `config.bootstrapServers`  | Kafka server host                   | `mysqlpw`                                               |
| `resources`                | CPU/Memory resource requests/limits | Memory: `256Mi`, CPU: `100m`                            |

You can specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example,

```bash
$ helm install --name my-release \
  --set config.mysqlRootPassword=rootpassword \
    kubeless-functions-charts/debezium-connect
```
Alternately, you can provide a YAML file that specifies parameter values while installing the chart. For example,

```bash
$ helm install --name my-release -f values.yaml kubeless-functions-charts/debezium-connect
```

> **Tip**: You can use the default [values.yaml](values.yaml)
