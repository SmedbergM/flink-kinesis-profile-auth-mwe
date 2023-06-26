# flink-kinesis-profile-auth-mwe

The Kinesis consumer for Apache Flink is supposed to support profile auth for
local development. However, it does not. Instead, "profile" auth means checking
`~/.aws/credentials` for explicit credentials.

## Running

### Prerequisites

You need an SSO profile configured in AWS IAM -- this usually is configured in `~/.aws/profile`.

You need a Kinesis stream that this profile can write to and read from.

To run the Python utilities in the `bin/` directory, you need `boto3`. 

### Test your stream

Activate your AWS profile (e.g. `aws sso login --profile $PROFILE`) and open up two
terminals. In the first, do
```sh
bin/kinesis_consumer.py <profile-name> <stream-arn>
```
In the second, do
```sh
bin/kinesis_producer.py <profile-name> <stream-arn>
```
This should write ten random alphanumeric string messages to the indicated stream, which
should show up in the STDOUT of the consumer.

### Run MWE

From IntelliJ: create a run configuration that sets the three required environment
variables `AWS_REGION`, `AWS_PROFILE_NAME`, and `KINESIS_STREAM_NAME`. Then run 
that run configuration.

From SBT: export the above environment variables, then do `sbt run`.
