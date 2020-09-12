scheduled_rule=fedex-case-analyser-dev
function_name=twitter-trends-dev-analyser
statement_id=fedex-case-analyser-id

aws events put-rule \
    --name $scheduled_rule \
    --schedule-expression 'rate(1 hour)'

aws lambda add-permission \
    --function-name $function_name \
    --statement-id  $statement_id \
    --action 'lambda:InvokeFunction' \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:eu-central-1:534692912862:rule/$scheduled_rule

aws events put-targets --rule $scheduled_rule --targets file://targets.json
