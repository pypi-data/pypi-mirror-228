#!/usr/bin/env python3
from enum import Enum


class BERTChineseModels(str, Enum):
    tiny = 'ckiplab/bert-tiny-chinese'
    base = 'bert-base-chinese'
    # https://huggingface.co/hfl/chinese-macbert-base
    macbert = 'hfl/chinese-macbert-base'
    macbert_large = 'hfl/chinese-macbert-large'
    xlnet_base = 'hfl/chinese-xlnet-base'


class BERTEnglishModels(str, Enum):
    base = 'bert-base-uncased'
    base_cased = 'bert-base-cased'
    large = 'bert-large-uncased'
    large_cased = 'bert-large-cased'
    xlnet_base = 'xlnet-base-cased'
    xlnet_large = 'xlnet-large-cased'
    tiny = 'prajjwal1/bert-tiny'
    albert_base = 'albert-base-v2'
    albert_large = 'albert-large-v2'
    albert_xlarge = 'albert-xlarge-v2'
    distil = 'distilbert-base-uncased'
    roberta = 'roberta-base'
    roberta_large = 'roberta-large'
    deberta = 'microsoft/deberta-v3-base'
    xlm_roberta = 'xlm-roberta-base' # 100 languages
    base_multilingual_cased='bert-base-multilingual-cased'
    base_multilingual_uncased='bert-base-multilingual-uncased'
    snli = 'symanto/xlm-roberta-base-snli-mnli-anli-xnli' # A strong base model for snli


if __name__ == '__main__':
    print(BERTChineseModels.tiny.value)
