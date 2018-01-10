# Kubeless weekly technical call reminder

Trigger the function and it send a reminder for the Kubeless weekly technical call on every 10:30am Thursday.

You need a SLACK_API_TOKEN

## Store token

Store your SLACK API TOKEN in a Kubernetes secret

```
kubectl create secret generic slack --from-literal=token=<your_token>
```

## Launch the function

Edit `reminder.py` to specify the proper channel, message.

Deploy the function:

```
make reminder
```

Undeploy the function:

```
make clean
```
