# --------------------------------------------
import random
from typing import List, Union

import codefast as cf
import joblib
import numpy as np
import pandas as pd
from codefast.patterns.pipeline import BeeMaxin, Pipeline
from pydantic import BaseModel
from rich import print


def random_swap(words: List[str], ratio: float = 0.07) -> str:
    '''Randomly swap two words in the list len(words)*ratio times
    '''
    assert isinstance(words, list), 'words must be a list'
    if len(words) <= 1:
        return words

    words = words.copy()
    n = max(1, int(len(words) * ratio))

    for _ in range(n):
        while True:
            ia = random.randint(0, len(words) - 1)
            ib = random.randint(0, len(words) - 1)
            if ia != ib:
                words[ia], words[ib] = words[ib], words[ia]
                break
    return ' '.join(words)


def random_delete(words: List[str], ratio: float = 0.1)->str:
    '''Randomly swap two words in the list len(words)*ratio times
    '''
    assert isinstance(words, list), 'words must be a list'
    if len(words) <= 1:
        return words

    words = words.copy()
    n = max(1, int(len(words) * ratio))

    for _ in range(n):
        ia = random.randint(0, len(words) - 1)
        words.pop(ia)
    return ' '.join(words)


# —--------------------------------------------
class DeeplAPI(object):
    '''Deepl tranlation API'''
    languages = [("BG", "Bulgarian"), ("CS", "Czech"), ("DA", "Danish"),
                 ("DE", "German"), ("EL", "Greek"), ("EN", "English"),
                 ("ES", "Spanish"), ("ET", "Estonian"), ("FI", "Finnish"),
                 ("FR", "French"), ("HU", "Hungarian"), ("ID", "Indonesian"),
                 ("IT", "Italian"), ("JA", "Japanese"), ("KO", "Korean"),
                 ("LT", "Lithuanian"), ("LV", "Latvian"), ("NB", "Norwegian"),
                 ("NL", "Dutch"), ("PL", "Polish"), ("PT", "Portuguese"),
                 ("RO", "Romanian"), ("RU", "Russian"), ("SK", "Slovak"),
                 ("SL", "Slovenian"), ("SV", "Swedish"), ("TR", "Turkish"),
                 ("UK", "Ukrainian"), ("ZH", "Chinese")]

    def __init__(self, deepl_token: str) -> None:
        self._url = 'https://api-free.deepl.com/v2'
        self._headers = '''Host: api-free.deepl.com
            User-Agent: 'Chrome/90.0.4430.212 Safari/537.36'
            Accept: */*
            Content-Length: [length]
            Content-Type: application/x-www-form-urlencoded'''
        self._params = {'auth_key': deepl_token}

    def do_request(self, api_path: str) -> dict:
        resp = cf.net.post(self._url + api_path,
                           headers=cf.net.parse_headers(self._headers),
                           data=self._params)
        if resp.status_code != 200:
            raise Exception(resp)
        # cf.info(resp.json())
        return resp.json()

    @property
    def stats(self):
        return self.do_request('/usage')

    def translate(self,
                  text: Union[str, List[str]],
                  target_lang=None) -> List[str]:
        # will always return a list of str no matter the input
        if not target_lang:
            target_lang = 'EN' if cf.nstr(text).is_cn() else 'ZH'
        self._params['text'] = text
        self._params['target_lang'] = target_lang
        response = self.do_request('/translate')
        return [r['text'] for r in response['translations']]

    def back_translate(self,
                       text: Union[str, List[str]],
                       source_lang,
                       target_lang=None,
                       random_lang=False) -> List[str]:
        """translate to EN first, then translate back to the original language
        :param text: text to translate
        :param source_lang: source language
        :param target_lang: target language
        :param random_lang: if True, will randomly choose a language to translate to
        """
        if not target_lang:
            target_lang = 'EN' if cf.nstr(text).is_cn() else 'ZH'
            if random_lang:
                target_lang = random.choice(
                    [l[0] for l in self.languages if l[0] != source_lang])
        # cf.info({'source_lang': source_lang, 'target_lang': target_lang})
        self._params['text'] = text
        self._params['target_lang'] = target_lang
        response = self.do_request('/translate')
        texts = [r['text'] for r in response['translations']]
        return self.translate(texts, target_lang=source_lang)
    