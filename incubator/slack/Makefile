slack:
	kubeless function deploy slack --runtime python2.7 --handler bot.handler --from-file bot.py --dependencies requirements.txt
events:
        kubeless function deploy k8s-events --trigger-topic k8s --from-file botevents.py --handler botevents.handler --runtime python2.7 --dependencies requirements.txt
