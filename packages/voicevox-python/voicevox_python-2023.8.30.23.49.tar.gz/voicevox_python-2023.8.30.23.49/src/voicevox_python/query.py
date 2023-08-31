from voicevox_python.model import AudioQuery
from typing import List, Optional, Dict, Any, Union
from requests import Response, Session


class Client:
    def __init__(self, url: str = "http://localhost:50021", timeout: Optional[float] = None) -> None:
        self.url = url
        self.timeout = timeout
        self.session = Session()

    def post(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    ) -> Response:
        try:
            return self.session.post(self.url + path, params=params, json=json, timeout=self.timeout)
        except:
            raise ValueError("failed to connect to VoiceVox Server")

    def audio_query(self, text: str, speaker: int) -> AudioQuery:
        response = self.post("/audio_query", params={"text": text, "speaker": speaker})
        if response.status_code == 200:
            return AudioQuery(**response.json())
        else:
            raise ValueError(f"failed to create audio query: {response.text}")

    def audio_query_from_preset(self, text: str, preset_id: int, core_version: Optional[str] = None) -> AudioQuery:
        response = self.post(
            "/audio_query_from_preset",
            params={"text": text, "preset_id": preset_id, "core_version": core_version},
        )
        if response.status_code == 200:
            return AudioQuery(**response.json())
        else:
            raise ValueError(f"failed to create audio query from preset: {response.text}")

    def synthesis(
        self,
        query: AudioQuery,
        speaker: int,
        enable_interrogative_upspeak: bool = True,
        core_version: Optional[str] = None,
    ) -> bytes:
        params = {
            "speaker": speaker,
            "enable_interrogative_upspeak": enable_interrogative_upspeak,
            "core_version": core_version,
        }
        response = self.post("/synthesis", params=params, json=query.model_dump())

        if response.status_code == 200:
            return response.content
        else:
            raise ValueError(f"failed to synthesis: {response.text}")

    def multi_synthesis(self, queries: List[AudioQuery], speaker: int, core_version: Optional[str] = None) -> bytes:
        """
        複数のクエリを同時に合成し,zip圧縮したバイナリを返す
        """
        response = self.post(
            "/multi_synthesis",
            params={"speaker": speaker, "core_version": core_version},
            json=[q.model_dump() for q in queries],
        )
        if response.status_code == 200:
            return response.content
        else:
            raise ValueError(f"failed to multi synthesis: {response.text}")
