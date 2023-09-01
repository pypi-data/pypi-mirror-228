from typing import List

def en_tokenizer(text)->List[str]:
    # English tokenizer
    return [x for x in text.split(' ') if x.strip()]
    
def zh_tokenizer(text)->List[str]:
    # Chinese tokenizer
    import jieba
    return [x for x in jieba.cut(text) if x.strip()]