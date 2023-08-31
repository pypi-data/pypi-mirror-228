import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from requests_aws4auth import AWS4Auth
import json


class AppSyncClient:
    def __init__(self,  url: str, access_key: str, secret_key: str, region: str) -> None:
        self.APPSYNC_API_ENDPOINT_URL = url
        self.connection: requests.Session = self.connect(
            access_key, secret_key, region)

    def connect(self, access_key: str, secret_key: str, region: str):
        session = requests.Session()
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        session.auth = AWS4Auth(
            access_key,
            secret_key,
            region,
            'appsync'
        )
        return session

    def run_query(self, query):
        response = self.connection.request(
            url=self.APPSYNC_API_ENDPOINT_URL,
            method='POST',
            json={'query': query}
        )
        return json.loads(response.text)
