# --------------------------------------------
import codefast as cf
from rich import print

from premium.preprocessing.ner import extract_bieso, extract_biso

# —--------------------------------------------


def test_extract_bieso():
    text = '[伦敦]是[英国]的首都'
    expected = {
        'sentence': '伦敦是英国的首都',
        'tags': ['B', 'E', 'O', 'B', 'E', 'O', 'O', 'O']
    }
    assert extract_bieso(text) == expected

    text = '[华盛顿]是[美国]的首都'
    expected = {
        'sentence': '华盛顿是美国的首都',
        'tags': ['B', 'I', 'E', 'O', 'B', 'E', 'O', 'O', 'O']
    }
    assert extract_bieso(text) == expected


def test_extract_biso():
    text = '[伦敦]是[英国]的首都'
    expected = {
        'sentence': '伦敦是英国的首都',
        'tags': ['B', 'I', 'O', 'B', 'I', 'O', 'O', 'O']
    }
    assert extract_biso(text) == expected

    text = '[华盛顿]是[美国]的首都'
    expected = {
        'sentence': '华盛顿是美国的首都',
        'tags': ['B', 'I', 'I', 'O', 'B', 'I', 'O', 'O', 'O']
    }
    assert extract_biso(text) == expected
