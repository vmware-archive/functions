# [WIP] Prototype function that implements a toy k8s controller

It detects when a namespace is created and deploys a redis rc in it

It needs the k8s event to kafka event sync:
https://github.com/kubeless/kubeless/tree/master/docker/event-sources/kubernetes
