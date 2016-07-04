# Amazon Lambda Demo

This demo uses Amazon Lambda and API Gateway to implement a serverless web service.

The repo contains two Lambda functions, *dekki_spekki_demo* handles OAuth callback and saves user profile data into DB, while *dekki_spekki_db_count* list all database content in table format.

## dekki_spekki_demo

This Lambda function performs those actions in order:

1. Get OAuth callback params from API Gateway.
1. Exchange `access_token` with passed `code` param.
1. Use `access_token` to get user profile.
1. Save user info into DynamoDB

### How to use

1. Create Lambda function in AWS console
  * Select *Python 2.7* as runtime.
  * Make sure the role of this Lambda has permission to *dynamodb*.
  * Enable API Gatway for this Lambda, default configuration is okay.
  * Use default for other fields.

1. Configure API Gateway to pass through correct params
  1. Get into API Gateway console
  1. Find *Method Request* block in the *GET* action diagram
  1. Add `code` and `state` to *URL Query String Parameters* section
  1. Back to diagram and get into *Integration Request* block
  1. In *Body Mapping Templates* section, add new mapping template:
    * Content-Type: `application/json`
    * Put those code into template editor box:
      ```
      {
         "state": "$input.params('state')",
         "code": "$input.params('code')"
      }
      ```
  1. Select *Deploy API* from Actions drop down menu after changes saved

1. Clone code to local, and activate virtualenv
  ```
  $ virtualenv venv -p `which python2.7`
  $ . ./venv/bin/activate
  $ pip install -r requirements.txt
  ```

1. Prepare Google app
  * Create web client in google developer console
  * Copy *conf.py.example* to *conf.py*
  * fill `client_id`, `client_secret` and `redirect_uri`

1. Configure aws cli tool

1. Build and upload the deploy package by `make` command

## dekki_spekki_db_count

This Lambda function gets all database record from related dynamo DB, and show it to user by HTML table.

### How to use

This demo only contains one single file, you can copy-paste the content to Lambda function editor, or use the Makefile in the directory. The creatation of Lambda function is similar with previous app, except configuration for API Gateway.

**Setup HTML Response in API Gateway**

The response from Lambda function is a string, and the API Gateway needs to add a appropriate Content-Type header to help browser to parse it.

Browser the DB API's method execution diagram, click *Integration Response* block, then click status line, and find *Body Mapping Templates*. In the Content-Type section, add mapping template named *text/html*, then paste those conteint into the editor box:

```
#set($inputRoot = $input.path('$'))
$inputRoot.html_data .
```

The `html_data` is the dict key returned from Lambda function.

After changes saved, click deploy API from action drop down menu.

