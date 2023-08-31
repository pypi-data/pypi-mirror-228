from pydantic import BaseModel
from typing import List, Optional


class Mora(BaseModel):
    text: str  # 文字
    consonant: Optional[str]  # 子音の音素
    consonant_length: Optional[float]  # 子音の音長
    vowel: str  # 母音の音素
    vowel_length: float  # 母音の音長
    pitch: float  # 音高


class AccentPhrase(BaseModel):
    moras: List[Mora]  # モーラのリスト
    accent: int  # アクセント箇所
    pause_mora: Optional[Mora]  # 後ろに無音を付けるかどうか
    is_interrogative: bool = False  # 疑問系かどうか


class AudioQuery(BaseModel):
    accent_phrases: List[AccentPhrase]  # アクセント句のリスト
    speedScale: float  # 全体の話速
    pitchScale: float  # 全体の音高
    intonationScale: float  # 全体の抑揚
    volumeScale: float  # 全体の音量
    prePhonemeLength: float  # 音声の前の無音時間
    postPhonemeLength: float  # 音声の後の無音時間
    outputSamplingRate: int  # 音声データの出力サンプリングレート
    outputStereo: bool  # 音声データをステレオ出力するか否か
    kana: Optional[str]  # [読み取り専用]AquesTalkライクな読み仮名。音声合成クエリとしては無視される
