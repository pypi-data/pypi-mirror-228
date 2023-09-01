#!/usr/bin/env python3
import re
from typing import Dict, List, Tuple, Union
import json 
import pandas as pd
from codefast.ds import flatten
from sklearn.base import BaseEstimator, TransformerMixin
from collections import OrderedDict

import ast 
def parse_list(s: str):
    return ast.literal_eval(s)


def tostr(tags):
    return ''.join(tags)


def generate_label_maps(labels: List[str], seperator=','):
    """ Generate label maps from labels
    Args:
        labels: list of labels
        seperator: seperator of labels
    Returns:
        tag2id: tag to id mapping
        id2tag: id to tag mapping
    """
    gen = flatten([label.split(seperator) for label in labels])
    entities = set([x for x in gen])
    tag2id = {tag: idx for idx, tag in enumerate(entities)}
    id2tag = {idx: tag for idx, tag in tag2id.items()}
    return tag2id, id2tag


def get_sequence(tokens: List[str], tags: List[str]):
    # Get labelled sequence
    res, tmp = [], []
    for x, y in zip(tokens, tags):
        if y == 'O':
            if tmp:
                res.append(tmp)
                tmp = []
        else:
            tmp.append(x)
    return [''.join(x) for x in res]


class NerLabelEncoder(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        assert isinstance(X, list)
        assert isinstance(X[0],
                          list), 'input to fit method should be a list of list'
        entities = set(flatten(X))
        self.ids_mapping = {tag: idx for idx, tag in enumerate(entities)}
        self.label_mapping = {idx: tag for idx, tag in self.ids_mapping.items()}
        return self

    def transform(self, X, y=None):
        assert isinstance(X, list)
        return [self.ids_mapping[x] for x in X]

    def inverse_transform(self, X, y=None):
        assert isinstance(X, list)
        return [self.label_mapping[x] for x in X]

    def save(self, path: str):
        pd.DataFrame(self.ids_mapping.items(),
                     columns=['label', 'id']).to_csv(path, index=False)

    @classmethod
    def load(cls, path: str):
        df = pd.read_csv(path)
        obj = cls()
        obj.ids_mapping = dict(df.values)
        obj.label_mapping = {idx: tag for idx, tag in obj.ids_mapping.items()}
        return obj

    def __len__(self):
        return len(self.ids_mapping)


class TagValueFormer(OrderedDict):

    def __init__(self, values: List[List[str]]=None):
        """ Tag to value mapping
        """
        super().__init__()
        self['O'] = 0
        if values:
            self.fit(values)
    
    def _validate_list(self, y:List[List[str]]):
        if y:
            assert isinstance(y, list), "y must be a list"
            assert isinstance(y[0], list), "y must be a list of list"
            assert isinstance(y[0][0], str), "y must be a list of list of str"
        return y 

    def fit(self, y: List[List[str]]):
        for z in sorted(set(flatten(self._validate_list(y)))):
            self[z] = self.get(z, len(self))
        
    def transform(self, y: List[List[str]]):
        return [[self[z] for z in x] for x in y]

    def inverse_transform(self, y: Union[List, int]):
        _reverse = {idx: tag for tag, idx in self.items()}
        if isinstance(y, int):
            return _reverse[y]
        else:
            return [self.inverse_transform(x) for x in y]
    
    def save(self, json_path: str):
        with open(json_path, 'w') as f:
            json.dump(self, f)
        return json_path
        
    @classmethod
    def load(cls, json_path: str):
        with open(json_path, 'r') as f:
            obj = cls()
            obj.update(json.load(f))
        return obj
    
    
def format_to_csv(source_file: str,
                  target_file: str,
                  reverse_text_label=False,
                  seperator='\t'):
    """read file from source_file, reformat it and save to target_file
    The format of source file is as follows:
    ```
    New B-CITY
    York I-CITY
    is  O
    a   O
    big O
    city O
    .   O

    How O
    are O
    you O
    ? O
    ```
    """
    df = pd.DataFrame(columns=['text', 'label'])
    text, label, tuples = [], [], []
    with open(source_file, 'r') as f:
        for line in f:
            if line.strip():
                t, l = line.strip().split(seperator)
                if reverse_text_label:
                    t, l = l, t
                text.append(t)
                label.append(l)
            else:
                tuples.append((text, label))
                text, label = [], []
    df['text'] = [' '.join(text) for text, _ in tuples]
    df['label'] = [','.join(label) for _, label in tuples]
    df.to_csv(target_file, index=False)
    return tuples


def extract_bio(text: str) -> List[str]:
    """ Get NER BIO sequence from text
    """
    bio = []
    for it in re.split(r'(\[[^\[\]]+\])', text.strip()):
        if it.startswith('['):
            bio += ['B'] + ['I'] * (len(it) - 3)
        else:
            bio += ['O'] * len(it)
    return bio


def extract_bieso(text: str) -> Dict[str, Union[str, List[str]]]:
    """ Get NER BIESO sequence from text. 
    Example:
    1. [伦敦]是[英国]的首都。 -> B E O B E O O O 
    2. [华盛顿]是[美国]的首都。 -> B I E O B E O O O
    """
    bar = '🧵'
    text=text.replace('/','')
    pieces = text.replace('[', '/' + bar).replace(']', bar + '/').split('/')
    tags = []
    for piece in pieces:
        if piece.startswith(bar):
            piece = piece.replace(bar, '')
            if len(piece) == 1:
                tags.append('S')
            elif len(piece) > 1:
                tags += ['B'] + ['I'] * (len(piece) - 2) + ['E']
        else:
            tags += ['O'] * len(piece)
    tokens = list(text.replace('[', '').replace(']', ''))
    assert len(tokens) == len(tags), "length of tokens and tags should be equal"
    return {'tokens': tokens, 'tags': tags}


def extract_biso(text: str) -> Dict[str, Union[str, List[str]]]:
    """ Get NER BISO sequence from text. The only difference with 
    `extract_bisoe` is that the end tag is `I` instead of `E`.
    E.g., [伦敦]是[英国]的首都。 -> B I O B I O O O 
    """
    bar = '🧵'
    pieces = text.replace('[', '/' + bar).replace(']', bar + '/').split('/')
    tags = []
    for piece in pieces:
        if piece.startswith(bar):
            piece = piece.replace(bar, '')
            if len(piece) == 1:
                tags.append('S')
            elif len(piece) > 1:
                tags += ['B'] + ['I'] * (len(piece) - 1)
        else:
            tags += ['O'] * len(piece)
    tokens = list(text.replace('[', '').replace(']', ''))
    assert len(tokens) == len(tags), "length of tokens and tags should be equal"
    return {'tokens': tokens, 'tags': tags}


def restore_brackets(tokens:List[str], tags:List[str])->str:
    # restore '[word]' text from tokens and tags
    assert len(tokens) == len(tags), "length of tokens and tags should be equal"
    indexes=extract_indexes(tags)
    for start, end in indexes:
        tokens[start] = f'[{tokens[start]}'
        tokens[end-1] = f'{tokens[end-1]}]'
    return ''.join(tokens)

def bio_to_bieo(bio: List[str]) -> List[str]:
    # Convert sequence from BISO to BISEO,
    # assume both of have `S` tag.
    bieo = []
    for i, tag in enumerate(bio):
        if tag in ('B', 'O', 'S'):
            bieo.append(tag)
        else:
            if i + 1 < len(bio) and bio[i + 1] == 'I':
                bieo.append('I')
            else:
                bieo.append('E')
    return bieo


def to_dict(text: str) -> Dict:
    """ 格式化实体。
    E.g., 
    [伦敦]是[英国]的首都。 -> {
        'sentence': '伦敦是英国的首都。',
        'entities': [
            {
                'start': 0,
                'end': 2,
                'word': '伦敦',
            },
            {
                'start': 3,
                'end': 5,
                'word': '英国',
            }
        ]
    }
    """
    bar = '🧵'
    pieces = text.replace('[', '/' + bar).replace(']', bar + '/').split('/')
    rmap = {'sentence': text.replace('[', '').replace(']', ''), 'entities': []}
    prefix = ''
    for p in pieces:
        if p.startswith(bar):
            p = p.replace(bar, '')
            rmap['entities'].append({
                'start': len(prefix),
                'end': len(prefix) + len(p),
                'word': p,
            })
        prefix += p
    return rmap


def extract_indexes(tags: List[str]) -> List[Tuple[int, int]]:
    assert isinstance(tags, list), 'tags must be list'
    """ Get [(start_index, end_index + 1)], assume bio format
    """
    res = []
    left, right = -1, -1
    for i, t in enumerate(tags):
        if t.startswith('B') or t.startswith('I'): # E.g., 'OOOIIOO'
            if i == 0 or (i>0 and tags[i-1]=='O'):
                left = i
        elif t.startswith('O'):
            if i > 0 and tags[i - 1].startswith('I'):
                right = i
                res.append((left, right))
                left, right = -1, -1
    return res
