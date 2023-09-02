from typing import Iterable, Literal, Union

import numpy as np
from gensim.models import KeyedVectors
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import MiniBatchKMeans
from sklearn.exceptions import NotFittedError
from tqdm import tqdm

from skembeddings.streams.utils import deeplist


class VlaweEmbedding(BaseEstimator, TransformerMixin):
    """Scikit-learn compatible VLAWE model."""

    def __init__(
        self,
        word_embeddings: Union[TransformerMixin, KeyedVectors],
        prefit: bool = False,
        n_clusters: int = 10,
    ):
        self.word_embeddings = word_embeddings
        self.prefit = prefit
        self.kmeans = None
        self.n_clusters = n_clusters

    def _collect_vectors_single(self, tokens: list[str]) -> np.ndarray:
        if isinstance(self.word_embeddings, KeyedVectors):
            kv = self.word_embeddings
            embeddings = []
            for token in tokens:
                try:
                    embeddings.append(kv[token])  # type: ignore
                except KeyError:
                    continue
            if not embeddings:
                return np.full((1, kv.vector_size), np.nan)
            return np.stack(embeddings)
        else:
            return self.word_embeddings.transform(tokens)

    def _infer_single(self, doc: list[str]) -> np.ndarray:
        if self.kmeans is None:
            raise NotFittedError(
                "Embeddings have not been fitted yet, can't infer."
            )
        vectors = self._collect_vectors_single(doc)
        residuals = []
        for centroid in self.kmeans.cluster_centers_:
            residual = np.sum(vectors - centroid, axis=0)
            residuals.append(residual)
        return np.concatenate(residuals)

    def fit(self, X: Iterable[Iterable[str]], y=None):
        """Fits a model to the given documents."""
        X_eval = deeplist(X)
        if (
            not isinstance(self.word_embeddings, KeyedVectors)
            and not self.prefit
        ):
            print("Fitting word embeddings")
            self.word_embeddings.fit(X_eval)
        print("Collecting vectors")
        all_vecs = np.concatenate(
            [self._collect_vectors_single(doc) for doc in X_eval]
        )
        print("Fitting Kmeans")
        self.kmeans = MiniBatchKMeans(n_clusters=self.n_clusters)
        self.kmeans.fit(all_vecs)
        return self

    def partial_fit(self, X: Iterable[Iterable[str]], y=None):
        """Partially fits model (online fitting)."""
        if self.kmeans is None:
            return self.fit(X)
        X_eval = deeplist(X)
        if (
            not isinstance(self.word_embeddings, KeyedVectors)
            and not self.prefit
        ):
            self.word_embeddings.partial_fit(X_eval)
        all_vecs = np.concatenate(
            [self._collect_vectors_single(doc) for doc in X_eval]
        )
        self.kmeans.partial_fit(all_vecs)
        return self

    def transform(self, X: Iterable[Iterable[str]]) -> np.ndarray:
        """Infers vectors for all of the given documents."""
        vectors = [self._infer_single(doc) for doc in tqdm(deeplist(X))]
        return np.stack(vectors)
