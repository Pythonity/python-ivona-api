# -*- coding: utf-8 -*-
"""
ivona_api main module
"""
from __future__ import absolute_import, unicode_literals

import os

import requests
from requests_aws4auth import AWS4Auth
from six.moves.urllib.parse import urljoin

from ivona_api.exceptions import IvonaAPIException


IVONA_ACCESS_KEY_ENV = 'IVONA_ACCESS_KEY'
IVONA_SECRET_KEY_ENV = 'IVONA_SECRET_KEY'

IVONA_REGION_ENDPOINTS = {
    'eu-west-1': 'https://tts.eu-west-1.ivonacloud.com',  # EU
    'us-east-1': 'https://tts.us-east-1.ivonacloud.com',  # US East
    'us-west-2': 'https://tts.us-west-2.ivonacloud.com',  # US West
}


class IvonaAPI(object):
    """
    Base class that for accessing Ivona web API.
    Currently implements 'CreateSpeech' and 'ListVoices' endpoints, without
    support for lexicon actions.
    """
    def __init__(self, access_key=None, secret_key=None, voice_name='Salli',
                 language='en-US', codec='mp3', region='eu-west-1'):
        """
        Initialize class instance with AWS4Auth object and default voice
        export values

        :param access_key: Ivona access key
        :type access_key: str
        :param secret_key: Ivona secret key
        :type secret_key: str
        :param voice_name: voice name
        :type voice_name: str
        :param language: voice language
        :type language: str
        :param codec: codec that will be used to encode the audio file
        :type codec: str
        :param region: Amazon datacenter region
        :type region: str
        """
        self._access_key = access_key or os.environ.get(IVONA_ACCESS_KEY_ENV)
        self._secret_key = secret_key or os.environ.get(IVONA_SECRET_KEY_ENV)

        if not all([self._access_key, self._secret_key]):
            raise ValueError(
                "Ivona access key and secret key need to be avalible"
            )

        # Choices: 'eu-west-1', 'us-east-1', 'us-west-2'
        self.region = region
        # Choices: 'ogg', 'mp3', 'mp4'
        self.codec = codec.lower()
        self.voice_name = voice_name
        self.language = language

        self._aws4auth = AWS4Auth(
            self._access_key, self._secret_key,
            region, 'tts',
        )

        self.session = requests.Session()
        self.session.auth = self._aws4auth

        # Below are listed additional parameters that have default values,
        # but are initialized here so that they can be changed on instance
        # basis if need be

        # Choices: 'x-slow', 'slow', 'medium', 'fast', 'x-fast', 'default'
        self.rate = 'default'
        # Choices:
        # 'silent', 'x-soft', 'soft', 'medium', 'loud', 'x-loud', 'default'
        self.volume = 'default'
        # Integer in the range of 0-3000 (in milliseconds)
        self.sentence_break = 400
        # Integer in the range of 0-5000 (in milliseconds)
        self.paragraph_break = 650

    def _get_response(self, method, endpoint, data=None):
        """
        Helper method for wrapping API requests, mainly for catching errors
        in one place.

        :param method: valid HTTP method
        :type method: str
        :param endpoint: API endpoint
        :type endpoint: str
        :param data: extra parameters passed with the request
        :type data: dict
        :returns: API response
        :rtype: Response
        """
        url = urljoin(IVONA_REGION_ENDPOINTS[self.region], endpoint)

        response = getattr(self.session, method)(
            url, json=data,
        )

        if 'x-amzn-ErrorType' in response.headers:
            raise IvonaAPIException(response.headers['x-amzn-ErrorType'])

        if response.status_code != requests.codes.ok:
            raise IvonaAPIException(
                "Something wrong happened: {}".format(response.json())
            )

        return response

    def get_available_voices(self, language=None, gender=None):
        """
        Returns a list of available voices, via 'ListVoices' endpoint

        Docs:
            http://developer.ivona.com/en/speechcloud/actions.html#ListVoices

        :param language: returned voices language
        :type language: str
        :param gender: returned voices gender
        :type gender: str
        """
        endpoint = 'ListVoices'

        data = dict()
        if language:
            data.update({'Voice': {'Language': language}})

        if gender:
            data.update({'Voice': {'Gender': gender}})

        print(data)

        response = self._get_response('get', endpoint, data)

        return response.json()['Voices']

    def text_to_speech(self, text, file, voice_name=None, language=None):
        """
        Saves given text synthesized audio file, via 'CreateSpeech' endpoint

        Docs:
            http://developer.ivona.com/en/speechcloud/actions.html#CreateSpeech

        :param text: text to synthesize
        :type text: str
        :param file: file that will be used to save the audio
        :type file: file
        :param voice_name: voice name
        :type voice_name: str
        :param language: voice language
        :type language: str
        """
        endpoint = 'CreateSpeech'

        data = {
            'Input': {
                'Data': text,
            },
            'OutputFormat': {
                'Codec': self.codec.upper(),
            },
            'Parameters': {
                'Rate': self.rate,
                'Volume': self.volume,
                'SentenceBreak': self.sentence_break,
                'ParagraphBreak': self.paragraph_break,
            },
            'Voice': {
                'Name': voice_name or self.voice_name,
                'Language': language or self.language,
            },
        }

        response = self._get_response('post', endpoint, data)

        file.write(response.content)
