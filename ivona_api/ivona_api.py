from urllib.parse import urljoin

import requests
from requests_aws4auth import AWS4Auth


IVONA_REGION_ENDPOINTS = {
    'eu-west-1': 'https://tts.eu-west-1.ivonacloud.com',  # EU, Dublin
    'us-east-1': 'https://tts.us-east-1.ivonacloud.com',  # US East, N. Virginia
    'us-west-2': 'https://tts.us-west-2.ivonacloud.com',  # US West, Oregon
}


class IvonaAPI:
    """
    Base class that for accessing Ivona web API.
    Currently implements 'CreateSpeech' and 'ListVoices' endpoints, without
    support for lexicon actions.
    """
    ALLOWED_CODECS = ['ogg', 'mp3', 'mp4']

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        if value not in IVONA_REGION_ENDPOINTS.keys():
            raise ValueError("Incorrect region: {}".format(value))
        self._region = value

    @property
    def codec(self):
        return self._codec

    @codec.setter
    def codec(self, value):
        if value.lower() not in self.ALLOWED_CODECS:
            raise ValueError("Incorrect codec - only ogg, mp3 and mp4 allowed.")
        self._codec = value

    def __init__(self, access_key, secret_key, voice_name='Salli',
                 language='en-US', codec='mp3', region='eu-west-1'):
        self.region = region
        self._aws4auth = AWS4Auth(access_key, secret_key, region, 'tts')

        self.available_voices = self.get_available_voices()
        self.set_voice(voice_name, language)

        self.codec = codec.lower()

        # Below are listed additional parameters that have default values,
        # but are initialized here so that they can be changed on instance
        # basis if need be

        # ['x-slow', 'slow', 'medium', 'fast', 'x-fast', 'default']
        self.rate = 'default'
        # ['silent', 'x-soft', 'soft', 'medium', 'loud', 'x-loud', 'default']
        self.volume = 'default'
        # Integer in the range of 0-3000 (in milliseconds)
        self.sentence_break = 400
        # Integer in the range of 0-5000 (in milliseconds)
        self.paragraph_break = 650

    def _check_if_voice_exists(self, voice_name, language):
        if not any([v['Name'] == voice_name and v['Language'] == language
                    for v in self.available_voices]):
            return False
        else:
            return True

    def set_voice(self, voice_name, language):
        """Make sure that passed voice name and language pair exists"""
        if not self._check_if_voice_exists(voice_name, language):
            raise ValueError("Incorrect voice name-language pair.")
        self._voice_name = voice_name
        self._language = language

    def get_available_voices(self, filter_language=None):
        """
        Returns a list of available voices, via 'ListVoices' endpoint
            http://developer.ivona.com/en/speechcloud/actions.html#ListVoices
        """
        endpoint = urljoin(
            IVONA_REGION_ENDPOINTS[self.region], 'ListVoices',
        )
        if filter_language:
            if not any([v['Language'] == filter_language
                        for v in self.available_voices]):
                raise ValueError("Incorrect language.")

            data = {
                'Voice': {
                    'Language': filter_language,
                },
            }
            r = requests.post(endpoint, auth=self._aws4auth, json=data)
        else:
            r = requests.get(endpoint, auth=self._aws4auth)

        if 'x-amzn-ErrorType' in r.headers:
            raise IvonaAPIException(r.headers['x-amzn-ErrorType'])

        return r.json()['Voices']

    def text_to_speech(self, text, file, voice_name=None, language=None):
        """
        Saves given text synthesized audio file, via 'CreateSpeech' endpoint
            http://developer.ivona.com/en/speechcloud/actions.html#CreateSpeech
        """
        if voice_name or language:
            if not self._check_if_voice_exists(voice_name, language):
                raise ValueError("Incorrect voice name-language pair.")
        else:
            voice_name = self._voice_name
            language = self._language

        endpoint = urljoin(
            IVONA_REGION_ENDPOINTS[self.region], 'CreateSpeech',
        )

        data = {
            'Input': {
                'Data': str(text),
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
                'Name': voice_name,
                'Language': language,
            },
        }

        r = requests.post(endpoint, auth=self._aws4auth, json=data)

        if 'x-amzn-ErrorType' in r.headers:
            raise IvonaAPIException(r.headers['x-amzn-ErrorType'])

        file.write(r.content)

        return True


class IvonaAPIException(Exception):
    """Base IvonaAPI exception"""
    pass
