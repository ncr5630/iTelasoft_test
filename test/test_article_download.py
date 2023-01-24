import json
import os
import unittest
import boto3
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch
from moto import mock_s3, mock_sqs
from moto import mock_dynamodb2
import traceback
import logging

DEFAULT_REGION = 'eu-west-1'
BUCKET = "core-mcnews-monitoring-dev-databucket"        
DOWNLOAD_TIMEOUT = "10"      
STATUS_INDEX_TABLE = "MCNewsMonitoringClassificationDataTable"
CLASSIFY_ARTICLE_URL ="https://i596wph81i.execute-api.eu-west-1.amazonaws.com/dev2/classify"  
MOCK_REQUEST_POST = "requests.post"


ARTICLE_ITEM = {
    'Records': [{
            'messageId': '131323ce-3256-4f34-9cf0-4d3331efd284',
            'receiptHandle': 'AQEB7+M/wv/GaPo9PbEKF/VOq4EclTDLtZeVE5PV+DQy+UUnMMiTZLLdUFwFTyfpzlcdJxYIkESETW2XS4ZWeoE6BgBPtfX5wOzeJH+L1PccT+OxXc8oLspED4g8dpYw5EihFKJkH9KMc8L7BhqUsUpvLtdMdoJTquVnyZXVRCLhloq44U/maIz/c5kJKZWldQUGMNmPTTIkXLzbzul0GWOqpkqrZnlChZ0KuKXMEq+5XMYibA0CkuqCzf/faLOqJ3eHxpK86iEpbhuZNOdjlc89fBsnLrMYLO4GkEpUS+uO7+UthvoJR9Sn6QgcJF0SlEuWjBJIAoxUj41MrPMk29fEixR9BGNupikUovkua/wDP25Fjl1xXIl63ldRg9Pj4tUwU5qFnqffLMWeKJFokzhUgFFZF39Qs0UeLhmyDVsG7SAPa5Pn8jQb08nQ0FHorJhI',
            'body': '{"ap_syndicated": false, "collect_date": "2018-12-07 08:22:33.487678", "feeds": null, "guid": "http://www.nguoiduatin.vn/clip-tay-khong-quat-chet-ran-ho-mang-chua-de-tra-thu-cho-con-trai-a219651.html", "language": "vi", "media_id": 531608, "media_name": "nguoiduatin.vn", "media_url": "http://nguoiduatin.vn/", "processed_stories_id": 1576468102, "publish_date": "2021-06-05 20:00:00", "stories_id": 1112979919, "story_tags": [{"stories_id": 1112979919, "tag": "readability-lxml-0.7", "tag_set": "extractor_version", "tag_sets_id": 1354, "tags_id": 81092444}], "title": "Clip: Tay kh\\u00f4ng qu\\u1eadt ch\\u1ebft r\\u1eafn h\\u1ed5 mang ch\\u00faa \\u0111\\u1ec3 tr\\u1ea3 th\\u00f9 cho con trai", "url": "http://www.nguoiduatin.vn/clip-tay-khong-quat-chet-ran-ho-mang-chua-de-tra-thu-cho-con-trai-a219651.html", "word_count": null, "req_id": "youtub22-c54-4b01-90e6-d701748f0851", "key_word": "youtube", "bearer_token": "Bearer eyJraWQiOiIwRzREUk9FUnRSaCsxTGdSeG5WR3FyWjdieENNSmpwR2tBSlUxVXVIcHo0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJjYjMwNjZmZi02MzE5LTRiYjEtYTlmOS1kM2ZmZjI4MGVlMGIiLCJjb2duaXRvOmdyb3VwcyI6WyJBZG1pbiJdLCJldmVudF9pZCI6IjZkZDU0YTI1LWJhOTYtNDJjZS05MmUwLWZjN2E4OWJjODIwMCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2MjM4NDYzMTMsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS13ZXN0LTEuYW1hem9uYXdzLmNvbVwvZXUtd2VzdC0xX2kyRVlDVWo3TSIsImV4cCI6MTYyMzkzMjcxMywiaWF0IjoxNjIzODQ2MzEzLCJqdGkiOiJkMWQ2Yzg4NS1iYmI5LTQ4YzEtODQwNy1kNmNkZGI3YjdhNDUiLCJjbGllbnRfaWQiOiI3a2lybGp0b250YW9wYmNwMjVjcmw1ODkzYyIsInVzZXJuYW1lIjoiY2IzMDY2ZmYtNjMxOS00YmIxLWE5ZjktZDNmZmYyODBlZTBiIn0.uTiP5wfyzAa6tzLxaUH6EgDrqaAeiEq7R5L8gZC09iE4Pf4oNlCEiOmZg4k2eQ5ajT3Q7h3sRnMbrpJP4K4MvpqdJR_k6K8BJ6Sg_2Bg_ysiHpkxRM83efL5DcvA9gSLbXATDk9luiNf-ps0CVHs53U2mnXsfl2hQqdomRmrn6SMjfzsuG-C-TEU1Nyn9_QrggmsfhjwpK2bxlAeR8oXxqx8gKAuFvC_tGI5ivSF2Yh79Fhl_6CPE-qezEA9tbCsdohh1cwHrTj7J89IAWhrZ0yhbXFt6DLvnf9sWEV7AjjsmmxLkqOdR68KfV37n_MequfpzY2OEdCOtb2vOt28ag"}',
            'attributes': {
                'ApproximateReceiveCount': '1',
                'SentTimestamp': '1623846317627',
                'SenderId': 'AROAWFTNE4S3H3UPFQQM2:core-mcnews-monitoring-dev-NewsSourcesChartData-70mOApu9wfcJ',
                'ApproximateFirstReceiveTimestamp': '1623846323026'
            },
            'messageAttributes': {},
            'md5OfBody': '52b2c4f7ddcdcd1187a14f0383685297',
            'eventSource': 'aws:sqs',
            'eventSourceARN': 'arn:aws:sqs:eu-west-1:424356930742:core-mcnews-monitoring-dev-MediaCloudSqs-RPJOV0866ELQ',
            'awsRegion': 'eu-west-1'
        }
    ]
}

CLASSIFICATION = {
    "classification":[{
            "code-number": "01000000",
            "code-title": "arts, culture and entertainment",
            "sub-codes": []
        }, 
        {
            "code-number": "04000000",
            "code-title": "economy, business and finance",
            "sub-codes": [{
                    "code-number": "04003000",
                    "code-title": "computing and information technology",
                    "sub-codes": []
                }
            ]
        }, 
        {
            "code-number": "13000000",
            "code-title": "science and technology",
            "sub-codes": []
        }]
    }
class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def content(self):
        return self.content

@mock_s3
@mock_dynamodb2
@mock_sqs
@mock.patch.dict(os.environ, {"BUCKET": BUCKET})
@mock.patch.dict(os.environ, {"DOWNLOAD_TIMEOUT": DOWNLOAD_TIMEOUT})
@mock.patch.dict(os.environ, {"STATUS_INDEX_TABLE": STATUS_INDEX_TABLE})  
@mock.patch.dict(os.environ, {"CLASSIFY_ARTICLE_URL": CLASSIFY_ARTICLE_URL})
class TestLambdaFunction(TestCase):

    def setUp(self):        
        # S3 setup
        self.s3_client = boto3.client('s3')
        try:
            self.s3_client.create_bucket(
                Bucket=BUCKET,
                CreateBucketConfiguration={'LocationConstraint': DEFAULT_REGION}
            ) 
        except Exception as e:
            logging.error(traceback.format_exc())             

        # DynamoDB setup
        self.dynamodb = boto3.client('dynamodb')
        try:
            self.table = self.dynamodb.create_table(
                TableName=STATUS_INDEX_TABLE,
                KeySchema=[
                    {'KeyType': 'HASH', 'AttributeName': 'req_id'},
                    {'KeyType': 'RANGE', 'AttributeName': 'uniq_id'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'req_id', 'AttributeType': 'S'},
                    {'AttributeName': 'uniq_id', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 20,
                    'WriteCapacityUnits': 20
                }
            )
        except self.dynamodb.exceptions.ResourceInUseException:
            self.table = boto3.resource('dynamodb').Table(STATUS_INDEX_TABLE)

    def test_handler(self): 
        with mock.patch(MOCK_REQUEST_POST) as cla_article:
            cla_article.return_value = MockResponse(json.dumps(CLASSIFICATION),200)
            from src.download_article.lambda_function import lambda_handler            
            result = lambda_handler(ARTICLE_ITEM, {})

    def test_timeout_exception(self):
        with mock.patch(MOCK_REQUEST_POST) as cla_article_post:
            from src.download_article.lambda_function import lambda_handler
            cla_article_post.return_value = MockResponse(json.dumps({"tt":"ddd"}),504)
            try:
                result = lambda_handler(ARTICLE_ITEM, {})
            except Exception:
                return

    def test_notfound_exception(self):
        with mock.patch(MOCK_REQUEST_POST) as cla_article_post:
            from src.download_article.lambda_function import lambda_handler
            cla_article_post.return_value = MockResponse(json.dumps({"tt":"ddd"}),404)
            try:
                result = lambda_handler(ARTICLE_ITEM, {})
            except Exception:
                return

if __name__ == '__main__':
    unittest.main()