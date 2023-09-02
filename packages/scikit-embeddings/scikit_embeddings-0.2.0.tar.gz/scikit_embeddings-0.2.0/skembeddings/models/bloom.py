import collections
from itertools import islice
from typing import Iterable

import mmh3
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import NotFittedError
from thinc.api import Adam, CategoricalCrossentropy, Relu, Softmax, chain
from thinc.types import Floats2d
from tqdm import tqdm

from skembeddings.streams.utils import deeplist


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def hash_embed(
    tokens: list[str], n_buckets: int, seeds: tuple[int]
) -> np.ndarray:
    """Embeds ids with the bloom hashing trick."""
    embedding = np.zeros((len(tokens), n_buckets), dtype=np.float16)
    n_seeds = len(seeds)
    prob = 1 / n_seeds
    for i_token, token in enumerate(tokens):
        for seed in seeds:
            i_bucket = mmh3.hash(token, seed=seed) % n_buckets
            embedding[i_token, i_bucket] = prob
    return embedding


class BloomWordEmbedding(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        vector_size: int = 100,
        window_size: int = 5,
        n_buckets: int = 1000,
        n_seeds: int = 4,
        epochs: int = 5,
    ):
        self.vector_size = vector_size
        self.n_buckets = n_buckets
        self.window_size = window_size
        self.epochs = epochs
        self.encoder = None
        self.seeds = tuple(range(n_seeds))
        self.n_seeds = n_seeds

    def _extract_target_context(
        self, docs: list[list[str]]
    ) -> tuple[list[str], list[str]]:
        target: list[str] = []
        context: list[str] = []
        for doc in docs:
            for window in sliding_window(doc, n=self.window_size * 2 + 1):
                middle_index = (len(window) - 1) // 2
                _target = window[middle_index]
                _context = [
                    token
                    for i, token in enumerate(window)
                    if i != middle_index
                ]
                target.extend([_target] * len(_context))
                context.extend(_context)
        return target, context

    def _init_model(self):
        self.encoder = Relu(self.vector_size)
        self.context_predictor = chain(self.encoder, Softmax(self.n_buckets))
        self.loss_calc = CategoricalCrossentropy()
        self.optimizer = Adam(
            learn_rate=0.001,
            beta1=0.9,
            beta2=0.999,
            eps=1e-08,
            L2=1e-6,
            grad_clip=1.0,
            use_averages=True,
            L2_is_weight_decay=True,
        )

    def _hash_embed(self, tokens: list[str]) -> Floats2d:
        ops = self.context_predictor.ops
        emb = hash_embed(tokens, self.n_buckets, self.seeds)
        return ops.asarray2f(emb)

    def _train_batch(self, batch: tuple[list[str], list[str]]):
        targets, contexts = batch
        _targets = self._hash_embed(targets)
        _contexts = self._hash_embed(contexts)
        try:
            Yh, backprop = self.context_predictor.begin_update(_targets)
        except KeyError:
            self.context_predictor.initialize(_targets, _contexts)
            Yh, backprop = self.context_predictor.begin_update(_targets)
        dYh = self.loss_calc.get_grad(Yh, _contexts)
        backprop(dYh)
        self.context_predictor.finish_update(self.optimizer)

    def fit(self, X: Iterable[Iterable[str]], y=None):
        X_eval = deeplist(X)
        self._init_model()
        ops = self.context_predictor.ops
        targets, contexts = self._extract_target_context(X_eval)
        batches = ops.multibatch(128, targets, contexts, shuffle=True)
        for batch in tqdm(batches):
            self._train_batch(batch)
        return self

    def partial_fit(self, X: Iterable[Iterable[str]], y=None):
        if self.encoder is None:
            return self.fit(X)
        X_eval = deeplist(X)
        targets, contexts = self._extract_target_context(X_eval)
        ops = self.context_predictor.ops
        batches = ops.multibatch(128, targets, contexts, shuffle=True)
        for batch in batches:
            self._train_batch(batch)
        return self

    def transform(self, X: Iterable[Iterable[str]], y=None) -> np.ndarray:
        """Transforms the phrase text into a numeric
        representation using word embeddings."""
        if self.encoder is None:
            raise NotFittedError(
                "Model has not been trained yet, can't transform."
            )
        ops = self.encoder.ops
        X_eval = deeplist(X)
        X_new = []
        for doc in X_eval:
            doc_emb = hash_embed(doc, self.n_buckets, self.seeds)
            doc_emb = ops.asarray2f(doc_emb)  # type: ignore
            doc_vecs = ops.to_numpy(self.encoder.predict(doc_emb))
            X_new.append(np.nanmean(doc_vecs, axis=0))
        return np.stack(X_new)
