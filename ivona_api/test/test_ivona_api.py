import os
import tempfile
import filecmp
from uuid import uuid4

import pytest
from flaky import flaky

from ivona_api.ivona_api import IvonaAPI, IvonaAPIException


# Module fixtures
@pytest.fixture(scope='module')
def auth_keys():
    """Get working auth keys from environment variables"""
    access_key = os.environ["IVONA_ACCESS_KEY"]
    secret_key = os.environ["IVONA_SECRET_KEY"]
    assert access_key and secret_key

    return access_key, secret_key


# Tests
def test_init(auth_keys):
    """Test initializing"""
    # No arguments
    with pytest.raises(TypeError):
        IvonaAPI()

    # Wrong auth keys
    with pytest.raises(IvonaAPIException):
        IvonaAPI(str(uuid4()), str(uuid4()))

    # With incorrect region
    with pytest.raises(ValueError):
        IvonaAPI(auth_keys[0], auth_keys[1], region=str(uuid4()))

    # With nonexistent voice
    with pytest.raises(ValueError):
        IvonaAPI(auth_keys[0], auth_keys[1], voice_name=str(uuid4()))

    # With not allowed codec
    with pytest.raises(ValueError):
        IvonaAPI(auth_keys[0], auth_keys[1], codec=str(uuid4()))


@flaky
def test_available_voices(auth_keys):
    """Test getting available voices"""
    ivona_api = IvonaAPI(auth_keys[0], auth_keys[1])

    voices = ivona_api.available_voices
    assert len(voices) > 1

    # Make sure that default voice is available
    assert any([v['Name'] == 'Salli' and v['Language'] == 'en-US'
                for v in voices])


@flaky
def test_available_voices_with_filter(auth_keys):
    """Test getting available voices with filtering"""
    ivona_api = IvonaAPI(auth_keys[0], auth_keys[1])

    with pytest.raises(ValueError):
        ivona_api.get_available_voices(str(uuid4()))

    voices = ivona_api.get_available_voices('en-US')
    assert len(voices) > 1

    # Make sure that default voice is available
    assert any([v['Name'] == 'Salli' and v['Language'] == 'en-US'
                for v in voices])


@flaky
@pytest.mark.parametrize('voice_name,voice_language,content,org_file', [
    ('Salli', 'en-US', 'Hello world', 'files/salli_hello_world.mp3'),
    ('Maja', 'pl-PL', 'Dzień dobry', 'files/maja_dzien_dobry.mp3'),
])
def test_text_to_speech(auth_keys, voice_name, voice_language, content,
                        org_file):
    """Test synthesizing text to audio files"""
    ivona_api = IvonaAPI(
        auth_keys[0], auth_keys[1],
        voice_name=voice_name, language=voice_language,
    )

    with tempfile.NamedTemporaryFile() as temp_file:
        ivona_api.text_to_speech(content, temp_file)

        assert filecmp.cmp(org_file, temp_file.name)


def test_text_to_speech_custom_voice(auth_keys):
    """Test setting custom voice"""
    ivona_api = IvonaAPI(auth_keys[0], auth_keys[1])

    with pytest.raises(ValueError):
        with tempfile.NamedTemporaryFile() as temp_file:
            ivona_api.text_to_speech(
                str(uuid4()), temp_file,
                voice_name=str(uuid4()),
            )
