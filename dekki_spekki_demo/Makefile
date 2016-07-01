all: deploy

pkg:
	-rm /tmp/lambda_demo.zip
	cd venv/lib/python2.7/site-packages && zip -q -r9 /tmp/lambda_demo.zip * && cd -
	zip -g /tmp/lambda_demo.zip lambda_function.py
	zip -g /tmp/lambda_demo.zip conf.py

deploy: pkg
	aws lambda update-function-code --function-name DekkiSpekkiDemo --zip-file fileb:///tmp/lambda_demo.zip

