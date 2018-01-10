reminder:
	kubeless function deploy scheduled-hello --schedule "30 10 * * THU" --runtime python2.7 --handler reminder.remind --from-file reminder.py --dependencies requirements.txt
clean:
	kubeless function delete scheduled-hello
	kubectl delete secret slack
