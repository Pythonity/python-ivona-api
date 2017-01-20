# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import tempfile
import filecmp

import pytest
import requests
import requests_aws4auth
from flaky import flaky

from ivona_api import IvonaAPI
from ivona_api.ivona_api import IVONA_ACCESS_KEY_ENV, IVONA_SECRET_KEY_ENV


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Tests
def test_init():
    """Test initializing"""
    ivona_api = IvonaAPI()

    assert ivona_api._access_key == os.environ[IVONA_ACCESS_KEY_ENV]
    assert ivona_api._secret_key == os.environ[IVONA_SECRET_KEY_ENV]

    assert ivona_api.region == 'eu-west-1'
    assert ivona_api.codec == 'mp3'
    assert ivona_api.voice_name == 'Salli'
    assert ivona_api.language == 'en-US'
    assert ivona_api.rate == 'default'
    assert ivona_api.volume == 'default'
    assert ivona_api.sentence_break == 400
    assert ivona_api.paragraph_break == 650

    assert isinstance(ivona_api._aws4auth, requests_aws4auth.AWS4Auth)
    assert isinstance(ivona_api.session, requests.Session)


def test_init_no_auth_data(monkeypatch):
    """Test initializing without auth data"""
    monkeypatch.delenv(IVONA_ACCESS_KEY_ENV, raising=False)
    monkeypatch.delenv(IVONA_SECRET_KEY_ENV, raising=False)

    with pytest.raises(ValueError):
        IvonaAPI()


@flaky
def test_available_voices():
    """Test getting available voices"""
    ivona_api = IvonaAPI()

    voices = ivona_api.get_available_voices()
    assert len(voices) > 1

    # Make sure that default voice is available
    assert any(
        [v['Name'] == 'Salli' and v['Language'] == 'en-US'
         for v in voices]
    )


@flaky
@pytest.mark.parametrize('voice_name,voice_language,content,org_file', [
    ('Salli', 'en-US', 'Hello world', 'files/salli_hello_world.mp3'),
    ('Maja', 'pl-PL', 'Dzień dobry', 'files/maja_dzien_dobry.mp3'),
])
def test_text_to_speech(voice_name, voice_language, content, org_file):
    """Test synthesizing text to audio files"""
    ivona_api = IvonaAPI(
        voice_name=voice_name, language=voice_language,
    )

    org_file = os.path.join(BASE_DIR, org_file)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        ivona_api.text_to_speech(content, temp_file)

    assert filecmp.cmp(org_file, temp_file.name)
