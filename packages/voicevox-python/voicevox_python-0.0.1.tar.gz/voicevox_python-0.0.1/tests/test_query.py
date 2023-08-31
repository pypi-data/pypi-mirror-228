from voicevox_python import Client, AudioQuery


def test_audio_query():
    client = Client()
    query = client.create_audio_query("こんにちは", 0)
    assert isinstance(query, AudioQuery)


def test_synthesis():
    client = Client()
    query = client.create_audio_query("こんにちは", 0)
    audio = client.synthesis(query, 0)
    assert isinstance(audio, bytes)
