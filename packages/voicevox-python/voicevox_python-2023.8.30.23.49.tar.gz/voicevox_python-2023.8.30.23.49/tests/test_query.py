from voicevox_python import Client, AudioQuery


def test_audio_query():
    client = Client()
    query = client.audio_query("こんにちは", 0)
    assert isinstance(query, AudioQuery)


def test_audio_query_from_preset():
    client = Client()
    query = client.audio_query_from_preset("こんにちは", 1)
    assert isinstance(query, AudioQuery)


def test_synthesis():
    client = Client()
    query = client.audio_query("こんにちは", 0)
    audio = client.synthesis(query, 0)
    assert isinstance(audio, bytes)


def test_multi_synthesis():
    client = Client()
    query = client.audio_query("こんにちは", 0)
    audio = client.multi_synthesis([query], 0)
    assert isinstance(audio, bytes)
