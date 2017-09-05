# Twitter function for Kubeless

Make sure `minikube` and `kubeless` are installed. See the respective installation guides:
* [Minikube](https://github.com/kubernetes/minikube#installation)
* [Kubeless](https://github.com/kubeless/kubeless/blob/master/README.md#usage)

Before deploy the function, you need to create a kubernetes secret storing your consumer_key, consumer_secret and token_key and token_secret. You can obtain them from the following URL by creating a new app.

https://apps.twitter.com/

Once you have your keys, you can deploy to kubernetes with the following command. Remember to update the placeholders with the correct values.

```bash
kubectl create secret generic twitter --from-literal=consumer_key=YOUR_CONSUME_KEY --from-literal=consumer_secret=YOUR_CONSUME_SECRET --from-literal=token_key=YOUR_TOKEN_KEY --from-literal=token_secret=YOUR_TOKEN_SECRET
```

Now you can deploy the function with kubeless or with the serverless plugin:

## Deploy the function with kubeless

### 1. Deploy

In order to deploy the function run the following command:

```bash
$ kubeless function deploy hello --from-file tweet.py --handler tweet.handler --runtime python2.7 --trigger-http --dependencies requirements.txt
```

You can list the function with `kubeless function ls` and you should see the following:

```
$ kubeless function ls
+-------+-----------+---------------+-----------+------+-------+----------------------------+
| NAME  | NAMESPACE |    HANDLER    |  RUNTIME  | TYPE | TOPIC |        DEPENDENCIES        |
+-------+-----------+---------------+-----------+------+-------+----------------------------+
| tweet | default   | tweet.handler | python2.7 | HTTP |       | python-twitter kubernetes  |
+-------+-----------+---------------+-----------+------+-------+----------------------------+
```

### 2. Invoke
You can now call your function:

```bash
kubeless function call tweet --data '{"tweet": "Testing twitter function from kubeless!"}'
```

## Deploy the function with the Serverless plugin

Make sure `serverless` is installed. You can see the installation instructions [here](https://github.com/serverless/serverless#quick-start).

### 1. Install Service Dependencies
Run `npm install` in this directory to download the modules from `package.json`.

### 2. Deploy
Run `serverless deploy` in order to deploy the function defined in `serverless.yml`

```bash
$ serverless deploy
Serverless: Packaging service...
Serverless: Function tweet succesfully deployed
```

### 3. Invoke the function

Run the following command:

```bash
$ serverless invoke -f tweet --log --data '{"tweet":"testing tweet from serverless kubeless plugin"}'
Serverless: Calling function: tweet...
--------------------------------------------------------------------
```

**For more information on the Serverless Kubeless plugin, please see the project repository: [https://github.com/serverless/serverless-kubeless](https://github.com/serverless/serverless-kubeless).**
