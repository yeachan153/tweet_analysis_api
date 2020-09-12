## Overview
Repository contains code for lambda trend analyzer and the lambda backend to query the dynamoDB from API gateway.

### Creating DynamoDB table
The dynamoDB table to store trends can be called. This will put a table in `eu-central-1`. The partition key is the date in format `%Y%m%d` and the secondary key if the hour.

```
from dynamodb.create_table import create_trend_table

create_trend_table()
```

### Calling API
Only method available is `GET`, and the query parameter it accepts is a date based on the format `%Y%m%d`. It then gives you a return of all the most re-tweeted text for that hashtag for that day.

### Deploying
1. git clone and activate venv with poetry (not strictly necessary as deployed with lambda layer)
2. I used this lambda layer [here](https://github.com/vbalasu/pandas-gbq-layer). Put it as a layer in Lambda and copy paste the ARN to the serverless yaml file.
3. Go to `analysis/trend_analysis` `sudo serverless deploy`
4. Need to run `cloudwatch_schedular.sh` to activate schedular to run every hour. Change the `target.json` as well to match your lambda ARN.
