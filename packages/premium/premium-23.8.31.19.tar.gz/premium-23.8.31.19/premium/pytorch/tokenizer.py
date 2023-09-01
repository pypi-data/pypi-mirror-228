#!/usr/bin/env python

import os
from abc import ABC, abstractmethod
from typing import List, Union

import codefast as cf
import numpy as np
import torch


def seq_to_embedding(seq, to_ix):
    '''
    This is a good entry point for passing in different kinds of embeddings and
    :param seq: sequence of words
    :param to_ix: embedding lib
    :return:
    '''
    idxs = [to_ix[w] for w in seq]
    return torch.tensor(idxs, dtype=torch.long)


def seqs_to_dictionary(training_data: list):
    '''
    Parameters
    ----------
    training_data: training data as a list of tuples.

    Returns
    -------
    word_to_ix: a dictionary mapping words to indices
    '''
    # Prepare for padding; need to change count to 1 as well.
    word_to_ix = {'<PAD>': 0}
    count1 = 1

    for sent, _ in training_data:
        for word in sent:
            if word not in word_to_ix:
                word_to_ix[word] = count1
                count1 += 1

    return word_to_ix


# Note: we are stealing this from tf.keras.preprocessing.sequence, to avoid having an additional
# dependency for tensorflow.
# It's perfectly fine if you want to install tf and call the function directly from there.


def pad_sequences(sequences,
                  maxlen=None,
                  dtype='int32',
                  padding='pre',
                  truncating='pre',
                  value=0.):
    """Pads sequences to the same length.
    This function transforms a list of
    `num_samples` sequences (lists of integers)
    into a 2D Numpy array of shape `(num_samples, num_timesteps)`.
    `num_timesteps` is either the `maxlen` argument if provided,
    or the length of the longest sequence otherwise.
    Sequences that are shorter than `num_timesteps`
    are padded with `value` at the end.
    Sequences longer than `num_timesteps` are truncated
    so that they fit the desired length.
    The position where padding or truncation happens is determined by
    the arguments `padding` and `truncating`, respectively.
    Pre-padding is the default.
    Arguments:
        sequences: List of lists, where each element is a sequence.
        maxlen: Int, maximum length of all sequences.
        dtype: Type of the output sequences.
        padding: String, 'pre' or 'post':
            pad either before or after each sequence.
        truncating: String, 'pre' or 'post':
            remove values from sequences larger than
            `maxlen`, either at the beginning or at the end of the sequences.
        value: Float, padding value.
    Returns:
        x: Numpy array with shape `(len(sequences), maxlen)`
    Raises:
        ValueError: In case of invalid values for `truncating` or `padding`,
            or in case of invalid shape for a `sequences` entry.
    """
    if not hasattr(sequences, '__len__'):
        raise ValueError('`sequences` must be iterable.')
    lengths = []
    for x in sequences:
        if not hasattr(x, '__len__'):
            raise ValueError('`sequences` must be a list of iterables. '
                             'Found non-iterable: ' + str(x))
        lengths.append(len(x))

    num_samples = len(sequences)
    if maxlen is None:
        maxlen = np.max(lengths)

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.
    sample_shape = tuple()
    for s in sequences:
        if len(s) > 0:  # pylint: disable=g-explicit-length-test
            sample_shape = np.asarray(s).shape[1:]
            break

    x = (np.ones((num_samples, maxlen) + sample_shape) * value).astype(dtype)
    for idx, s in enumerate(sequences):
        if not len(s):  # pylint: disable=g-explicit-length-test
            continue  # empty list/array was found
        if truncating == 'pre':
            trunc = s[-maxlen:]  # pylint: disable=invalid-unary-operand-type
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" not understood' %
                             truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError('Shape of sample %s of sequence at position %s '
                             'is different from expected shape %s' %
                             (trunc.shape[1:], idx, sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x


class Vectorizer(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def fit(self, texts: List[str]):
        pass

    @abstractmethod
    def transform(self, texts: List[str]):
        pass

    @abstractmethod
    def fit_transform(self, texts: List[str]):
        pass

    @abstractmethod
    def inverse_transform(self, tokens: List[int]):
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @abstractmethod
    def load(self, path: str):
        pass


class VocabVectorizer(object):

    def __init__(self, max_length, padding, tokenizer):
        """
        padding is either `pre` or `post`
        """
        self.vocab = {}
        self.index2token = {}
        self.max_length = max_length
        self.padding = padding
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.vocab)

    def pad_sequence(self, vector: List[int]):
        vector = vector[:self.max_length]
        if len(vector) >= self.max_length:
            return vector
        if self.padding == 'pre':
            return [0 for _ in range(self.max_length - len(vector))] + vector
        else:
            return vector + [0 for _ in range(self.max_length - len(vector))]

    def fit(self, texts: List[List[str]]):
        assert isinstance(self.tokenizer(texts[0]),
                          list), 'tokenizer must return a list'
        token_idx = 1
        for t in texts:
            for token in self.tokenizer(t):
                if token not in self.vocab:
                    self.vocab[token] = token_idx
                    self.index2token[token_idx] = token
                    token_idx += 1

    def transform(
        self,
        texts: Union[str, List[str]],
    ) -> Union[List[List[int]], np.ndarray]:
        if isinstance(texts, str):
            texts = [texts]

        vectors = []
        for x in texts:
            x = x[:self.max_length]
            vector = [self.vocab.get(token, 0) for token in self.tokenizer(x)]
            if self.padding is not None:
                vector = self.pad_sequence(vector)
            vectors.append(vector)
        return vectors

    def fit_transform(self, texts: Union[str, List[str]]) -> List[List[int]]:
        if isinstance(texts, str):
            texts = [texts]
        return self.fit(texts).transform(texts)

    def inverse_transform(self, tokens: List[int]) -> List[str]:
        return [self.index2token.get(idx, '') for idx in tokens]

    def save(self, path: str):
        cf.js.write(self.vocab, os.path.join(path, 'vocab.json'))
        cf.js.write(self.index2token, os.path.join(path, 'index.json'))

    def load(self, path: str):
        vocab_path = os.path.join(path, 'vocab.json')
        index_path = os.path.join(path, 'index.json')
        self.vocab = cf.js(vocab_path)
        self.index2token = cf.js(index_path)

    def __call__(self, texts: Union[str, List[str]]) -> List[int]:
        return self.transform(texts)
