# Simple Python function for Kubeless

Make sure `minikube` and `kubeless` are installed. See the respective installation guides:
* [Minikube](https://github.com/kubernetes/minikube#installation)
* [Kubeless](https://github.com/kubeless/kubeless/blob/master/README.md#usage)

You can deploy the function with kubeless or with the serverless plugin:

## Deploy the function with kubeless

### 1. Deploy
In order to deploy the function run the following command:

```bash
$ kubeless function deploy hello --from-file hellowithdata.py --handler hellowithdata.handler --runtime python2.7 --trigger-http
```

You can list the function with `kubeless function ls` and you should see the following:

```
$ kubeless function ls
+---------------+-----------+-----------------------+-----------+------+-------+--------------+
|     NAME      | NAMESPACE |        HANDLER        |  RUNTIME  | TYPE | TOPIC | DEPENDENCIES |
+---------------+-----------+-----------------------+-----------+------+-------+--------------+
| hellowithdata | default   | hellowithdata.handler | python2.7 | HTTP |       |              |
+---------------+-----------+-----------------------+-----------+------+-------+--------------+
```

### 2. Invoke
You can now call your function:

```bash
kubeless function call hellowithdata --data '{"name": "Tomas"}'
```

## Deploy the function with the serverless plugin

Make sure `serverless` is installed. You can see the installation instructions [here](https://github.com/serverless/serverless#quick-start).

### 1. Install Service Dependencies
Run `npm install` in this directory to download the modules from `package.json`.

### 2. Deploy
Run `serverless deploy` in order to deploy the function defined in `serverless.yml`

```bash
$ serverless deploy
Serverless: Packaging service...
Serverless: Function hellowithdata succesfully deployed
```

### 3. Invoke deployed function
Run `serverless invoke --function hello --log

In your terminal window you should see the response from Kubernetes.

```$ serverless invoke -f hellowithdata --log --data '{"name":"Bob"}'
Serverless: Calling function: hellowithdata...
--------------------------------------------------------------------
{ name: 'Bob' }
```

**For more information on the Serverless Kubeless plugin, please see the project repository: [https://github.com/serverless/serverless-kubeless](https://github.com/serverless/serverless-kubeless).**
