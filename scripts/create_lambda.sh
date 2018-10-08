aws lambda create-function \
    --region $AWS_DEFAULT_REGION \
    --function-name LdLambda \
    --zip-file fileb://LdLambda.zip \
    --role $AWS_LAMBDA_ROLE_ARN \
    --handler LdLambda.handler \
    --runtime python3.6 \
    --timeout 15 \
    --memory-size 128

