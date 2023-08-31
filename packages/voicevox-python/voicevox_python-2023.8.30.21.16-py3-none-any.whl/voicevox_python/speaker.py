from enum import Enum
from typing import Optional, Union, Dict, Tuple

speaker2id_dict: Dict[Tuple[str, str], int] = {
    ("四国めたん", "ノーマル"): 2,
    ("四国めたん", "あまあま"): 0,
    ("四国めたん", "ツンツン"): 6,
    ("四国めたん", "セクシー"): 4,
    ("四国めたん", "ささやき"): 36,
    ("四国めたん", "ヒソヒソ"): 37,
    ("ずんだもん", "ノーマル"): 3,
    ("ずんだもん", "あまあま"): 1,
    ("ずんだもん", "ツンツン"): 7,
    ("ずんだもん", "セクシー"): 5,
    ("ずんだもん", "ささやき"): 22,
    ("ずんだもん", "ヒソヒソ"): 38,
    ("春日部つむぎ", "ノーマル"): 8,
    ("雨晴はう", "ノーマル"): 10,
    ("波音リツ", "ノーマル"): 9,
    ("玄野武宏", "ノーマル"): 11,
    ("玄野武宏", "喜び"): 39,
    ("玄野武宏", "ツンギレ"): 40,
    ("玄野武宏", "悲しみ"): 41,
    ("白上虎太郎", "ふつう"): 12,
    ("白上虎太郎", "わーい"): 32,
    ("白上虎太郎", "びくびく"): 33,
    ("白上虎太郎", "おこ"): 34,
    ("白上虎太郎", "びえーん"): 35,
    ("青山龍星", "ノーマル"): 13,
    ("冥鳴ひまり", "ノーマル"): 14,
    ("九州そら", "ノーマル"): 16,
    ("九州そら", "あまあま"): 15,
    ("九州そら", "ツンツン"): 18,
    ("九州そら", "セクシー"): 17,
    ("九州そら", "ささやき"): 19,
    ("もち子さん", "ノーマル"): 20,
    ("剣崎雌雄", "ノーマル"): 21,
    ("WhiteCUL", "ノーマル"): 23,
    ("WhiteCUL", "たのしい"): 24,
    ("WhiteCUL", "かなしい"): 25,
    ("WhiteCUL", "びえーん"): 26,
    ("後鬼", "人間ver."): 27,
    ("後鬼", "ぬいぐるみver."): 28,
    ("No.7", "ノーマル"): 29,
    ("No.7", "アナウンス"): 30,
    ("No.7", "読み聞かせ"): 31,
    ("ちび式じい", "ノーマル"): 42,
    ("櫻歌ミコ", "ノーマル"): 43,
    ("櫻歌ミコ", "第二形態"): 44,
    ("櫻歌ミコ", "ロリ"): 45,
    ("小夜/SAYO", "ノーマル"): 46,
    ("ナースロボ＿タイプＴ", "ノーマル"): 47,
    ("ナースロボ＿タイプＴ", "楽々"): 48,
    ("ナースロボ＿タイプＴ", "恐怖"): 49,
    ("ナースロボ＿タイプＴ", "内緒話"): 50,
    ("†聖騎士 紅桜†", "ノーマル"): 51,
    ("雀松朱司", "ノーマル"): 52,
    ("麒ヶ島宗麟", "ノーマル"): 53,
    ("春歌ナナ", "ノーマル"): 54,
    ("猫使アル", "ノーマル"): 55,
    ("猫使アル", "おちつき"): 56,
    ("猫使アル", "うきうき"): 57,
    ("猫使ビィ", "ノーマル"): 58,
    ("猫使ビィ", "おちつき"): 59,
    ("猫使ビィ", "人見知り"): 60,
}


class SpeakerName(Enum):
    """話者の名前"""

    SHIKOKU_METAN = "四国めたん"
    ZUNDAMON = "ずんだもん"
    KASUKABE_TSUMUGI = "春日部つむぎ"
    AMEHARE_HAU = "雨晴はう"
    NAMINE_RITSU = "波音リツ"
    KURONO_TAKEHIRO = "玄野武宏"
    SHIRAKAMI_KOTAROU = "白上虎太郎"
    AOYAMA_RYUSEI = "青山龍星"
    MEIMEI_HIMARI = "冥鳴ひまり"
    KYUSHU_SORA = "九州そら"
    MOCHIKOSAN = "もち子さん"
    KENZAKI_MESUO = "剣崎雌雄"
    WHITE_CUL = "WhiteCUL"
    GOKI = "後鬼"
    NUMBER_SEVEN = "No.7"
    CHIBISHIKIJI = "ちび式じい"
    OUKA_MIKO = "櫻歌ミコ"
    SAYO = "小夜/SAYO"
    NURSE_ROBO_TYPET = "ナースロボ＿タイプＴ"
    HORINAITO_BENIZAKURA = "†聖騎士 紅桜†"
    WAKAMATSU_AKASHI = "雀松朱司"
    KIGASHIMA_SOURIN = "麒ヶ島宗麟"
    HARUKA_NANA = "春歌ナナ"
    NEKOTSUKA_ARU = "猫使アル"
    NEKOTSUKA_BI = "猫使ビィ"


class SpeakerStyle(Enum):
    """キャラのスタイル"""

    NORMAL = "ノーマル"
    AMAAMA = "あまあま"
    TSUNTSUN = "ツンツン"
    SEXY = "セクシー"
    SASAYAKI = "ささやき"
    HISOHISO = "ヒソヒソ"
    YOROKOBU = "喜び"
    TSUNGIRE = "ツンギレ"
    KANASHIMI = "悲しみ"
    WAIWAI = "わーい"
    BIKUBIKU = "びくびく"
    OKO = "おこ"
    BIEEN = "びえーん"
    JINEN_VER = "人間ver."
    NUIGURUMI_VER = "ぬいぐるみver."
    ANAUNSU = "アナウンス"
    YOMIKIKASE = "読み聞かせ"
    DAINI_KEITAI = "第二形態"
    LOLI = "ロリ"
    OCHITSUKI = "おちつき"
    UKIUKI = "うきうき"
    HITOMISHIRI = "人見知り"
    RAKURAKU = "楽々"
    KYOFU = "恐怖"
    NAISHOWA = "内緒話"


def speaker2id(speaker: Union[str, SpeakerName], style: Union[str, SpeakerStyle]) -> Optional[int]:
    """
    話者名とスタイル名からidに変換する

    Args:
        speaker (Union[str, SpeakerName]): 話者名
        style (Union[str, SpeakerStyle]): スタイル名

    Returns:
        Optional[int]: id
    """
    speaker = speaker if isinstance(speaker, str) else speaker.value
    style = style if isinstance(style, str) else style.value
    return speaker2id_dict.get((speaker, style), None)
