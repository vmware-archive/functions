## WARNING: Kubeless is no longer actively maintained by VMware.

VMware has made the difficult decision to stop driving this project and therefore we will no longer actively respond to issues or pull requests. If you would like to take over maintaining this project independently from VMware, please let us know so we can add a link to your forked project here.

Thank You.

# Functions for Kubeless

This repository contains Kubeless Functions. Kubeless is a Kubernetes-native serverless framework that makes use of Kubernetes' ThirdPartyResource to be able to create functions as custom Kubernetes resources

The purpose of this repository is to provide a place for maintaining and contributing official Kubeless functions, with CI processes in place for assuring an always up-to-date repository.

## Repository structure
The Charts in this repository are organized into two folders:
* charts
* incubator

Stable functions counts with an CI process in place and they are maintained and updated 
Incubator functions are those to be shared and improved on until they are ready to be moved into the charts folder.

## Structure of a Kubeless Function 
Each kubeless functions must have:
 - A metadata file 
 - A README.md file
 - A way to declare dependencies 

