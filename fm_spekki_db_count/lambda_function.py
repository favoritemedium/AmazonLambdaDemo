from __future__ import print_function

import json
import boto3

print('Loading function')

html_scaffold = """<html>
<head>
<meta charset="UTF-8">
<title>FmSpekkiDemo DB Records</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">
</head>
<body>
<div class='container'>
<h1 class='page-header'>
FmSpekkiDemo DB Records
</h1>
%s
</div>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
</body>
</html>"""

table_scaffold = """<table class='table'>
<thead>
<tr>
<th>Email</th>
<th>DisplayName</th>
<th>AccessToken</th>
</tr>
</thead>
<tbody>%s</tbody>
</table>"""

single_table_row = '<tr><td>{}</td><td>{}</td><td>{}...</td></tr>'


def lambda_handler(event, context):
    dynamo_table = boto3.resource('dynamodb').Table('FmSpekkiDemo')
    all_records = dynamo_table.scan()['Items']
    table_rows = []

    for rcd in all_records:
        table_rows.append(single_table_row.format(rcd['email'], rcd['displayName'], rcd['access_token'][2:13]))

    html_content = html_scaffold % (table_scaffold % ''.join(table_rows))
    return {'html_data': html_content}

