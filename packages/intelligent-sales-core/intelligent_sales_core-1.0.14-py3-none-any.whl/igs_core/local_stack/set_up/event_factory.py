# TODO: divide event class  into separated classes per event type
# TODO: modularize events depending on which service/microservice is launching the event
class EventS3Put:
    s3_event_put = {
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "aws:s3",
                "awsRegion": "eu-central-1",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {"principalId": "EXAMPLE"},
                "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                "responseElements": {
                    "x-amz-request-id": "EXAMPLE123456789",
                    "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "s3-data-intake",
                        "ownerIdentity": {"principalId": "PRINCIPALID"},
                        "arn": "arn:aws:s3:::s3-data-intake",
                    },
                    "object": {
                        "key": "route/of/my_fantastic_object.json",
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0A1B2C3D4E5F678901",
                    },
                },
            }
        ]
    }

    s3_eventbridge_put = {
        "source": "aws.s3",
        "region": "eu-central-1",
        "resources": [
            "arn:aws:s3:::lokoelstack-intelligentsales-s3-raw"
        ],
        "detail": {
            "bucket": {
                "name": "lokoelstack-intelligentsales-s3-raw"
            },
            "object": {
                "key": "simmix/MSI_MATS_20111231.zip"
            }
        }
    }

    def __init__(self, bucket: str, key: str):
        self.s3_event_put["Records"][0]["s3"]["bucket"]["name"] = bucket
        self.s3_event_put["Records"][0]["s3"]["object"]["key"] = key
        self.s3_eventbridge_put["detail"]["bucket"]["name"] = bucket
        self.s3_eventbridge_put["detail"]["object"]["key"] = key

    def get_fixture_event(self) -> dict:
        return self.s3_event_put

    def get_fixture_eventbridge_event(self) -> dict:
        return self.s3_eventbridge_put
