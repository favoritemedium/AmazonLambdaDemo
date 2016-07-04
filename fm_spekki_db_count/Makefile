all: deploy

pkg:
	-rm /tmp/lambda_db_count.zip
	zip -g /tmp/lambda_db_count.zip lambda_function.py

deploy: pkg
	aws lambda update-function-code --function-name FmSpekkiDBCount --zip-file fileb:///tmp/lambda_db_count.zip

