controller:
	kubeless function deploy controller --trigger-topic k8s --runtime python2.7 --handler ns.handler --from-file ns.py --dependencies requirements.txt
sync:
	kubectl run event --image=skippbox/k8s-events:0.10.13
