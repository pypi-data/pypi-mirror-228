# voicevox-python

## example

```python
from voicevox_python import Client, speaker2id

speaker_id = speaker2id("ずんだもん", "ノーマル")
client = Client()
query = client.audio_query("こんにちは", speaker_id)
audio = client.synthesis(query, speaker_id)
with open("out.wav", mode="wb") as f:
    f.write(audio)
```