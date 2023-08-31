import requests
import json
import unittest
from unittest import mock
from urllib.parse import urlencode
import logging


def create_params(**kwargs):
    '''
    Used to create url parameters for API call
    '''
    path = kwargs.get("path")
    params = kwargs.get("params")
    if params:
        query_string = urlencode(eval(params))
    return f'{path}?{query_string}'

def mocked_requests_get(url, headers, data):
    class MockResponse:
        def __init__(self, url, headers, status_code):
            self.verb = "GET"
            self.url = url
            self.headers = headers
            self.data = data
            self.status_code = status_code

        def json(self):
            return {
                "verb": self.verb,
                "url": self.url,
                "headers": self.headers,
                "data": self.data
            }

    return MockResponse(url, headers, 200)

class APIRequester:
    '''
    Used to make the request
    '''
    def __init__(self, **kwargs):

        self.method = kwargs.get("method")
        self.url = kwargs.get("url")
        self.headers = kwargs.get("headers")
        self.data = kwargs.get("data")
    
    #@mock.patch('requests.get', side_effect=mocked_requests_get)
    #def get(self, mock_get):
    def get(self):
        logging.debug(f'Request:\nVerb: GET\nURL: {self.url}\nHeaders: {self.headers}\nData: {self.data}')
        response = requests.get(
                self.url,
                headers=self.headers,
                data=self.data
            )
        return response
    
    #@mock.patch('requests.post', side_effect=mocked_requests_get)
    #def post(self, mock_get):
    def post(self):
        logging.debug(f'Request:\nVerb:POST\nURL: {self.url}\nHeaders: {self.headers}\nData: {self.data}')
        response = requests.post(
                self.url,
                headers=self.headers,
                data=self.data
            )
        return response
    
    #@mock.patch('requests.post', side_effect=mocked_requests_get)
    #def post(self, mock_get):
    def delete(self):
        logging.debug(f'Request:\nVerb: DELETE\nURL: {self.url}\nHeaders: {self.headers}\nData: {self.data}')
        response = requests.delete(
                self.url,
                headers=self.headers,
                data=self.data
            )
        return response

class PathBuilder:
    '''
    Used to build the correct API path that includes
    parameters & filters
    '''
    def __init__(self, **kwargs):
        self.base_url = kwargs.get('base_url')
        self.domain = kwargs.get('domain')
        self.version = kwargs.get('version')
        self.object_id = kwargs.get('object_id')
        self.object_action = kwargs.get('object_action')
        self.domain_id = kwargs.get('domain_id')
        self.domain_action = kwargs.get('domain_action')
        self.params = kwargs.get('params')
        
    def build(self):
        paths = {
            "domains":{
                "asset": {
                    "path": 'assets'
                },
                "attribute": {
                    "path": 'attributes'
                },
                "branded_portal": {
                    "path": 'brandedportals'
                },
                "category": {
                    "path": 'categories'
                },
                "config": {
                    "path": 'config'
                },
                "connect": {
                    "path": 'connect'
                },
                "crop": {
                    "path": 'crop'
                },
                "direct_link": {
                    "path": 'directlinks'
                },
                "download": {
                    "path": 'downloads'
                },
                "home": {
                    "path": ''
                },
                "introduction_and_help": {
                    "path": 'introductionAndHelp'
                },
                "keyword_group": {
                    "path": 'keywordGroups'
                },
                "keyword": {
                    "path": 'keywords'
                },
                "notification": {
                    "path": 'notification'
                },
                "org_unit": {
                    "path": 'organizationalUnits'
                },
                "reports": {
                    "path": 'reports'
                },
                "saved_search": {
                    "path": 'savedsearches'
                },
                "search": {
                    "path": 'search'
                },
                "share": {
                    "path": 'share'
                },
                "public": {
                    "path": 'public'
                },
                "upload": {
                    "path": 'uploads'
                },
                "user_group": {
                    "path": 'groups'
                },
                "user": {
                    "path": 'users'
                }
            }
        }
        domain_info = paths['domains'][self.domain]
        sections = [domain_info['path']]

        if self.domain_action:
            sections.append(self.domain_action)
        if self.object_id:
            sections.append(self.object_id)
        if self.object_action:
            sections.append(self.object_action)
        
        
        uri = f'/{"/".join(sections)}'
        
        #manage params and filtering
        params = {}
        for param in self.params.keys():
            params[param] = self.params[param]
        if params:
            uri = create_params(params=json.dumps(params), path=uri)

        url = f'https://{self.base_url}{uri}'

        return [uri, url]