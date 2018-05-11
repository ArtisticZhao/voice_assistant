# coding:utf-8
from core.aiui import aiui
from core.iat import iat
from core.tts import tts


def get_a_conversation():
    query = iat()
    ans = aiui(query)
    print(ans)
    # tts()


if __name__ == '__main__':
    get_a_conversation()
