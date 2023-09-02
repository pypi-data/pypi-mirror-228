# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skembeddings',
 'skembeddings.feature_extraction',
 'skembeddings.models',
 'skembeddings.preprocessing',
 'skembeddings.streams',
 'skembeddings.tokenizers']

package_data = \
{'': ['*']}

install_requires = \
['catalogue>=2.0.8,<3.0.0',
 'confection>=0.1.0,<0.2.0',
 'huggingface-hub>=0.16.0,<0.17.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'tokenizers>=0.13.0,<0.14.0']

extras_require = \
{'gensim': ['gensim==4.3.0'], 'spacy': ['spacy==3.5.0']}

setup_kwargs = {
    'name': 'scikit-embeddings',
    'version': '0.2.0',
    'description': 'Tools for training word and document embeddings in scikit-learn.',
    'long_description': '# scikit-embeddings\nUtilites for training word, document and sentence embeddings in scikit-learn pipelines.\n\n## Features\n - Train Word, Paragraph or Sentence embeddings in scikit-learn compatible pipelines.\n - Stream texts easily from disk and chunk them so you can use large datasets for training embeddings.\n - spaCy tokenizers with lemmatization, stop word removal and augmentation with POS-tags/Morphological information etc. for highest quality embeddings for literary analysis.\n - Fast and performant trainable tokenizer components from `tokenizers`.\n - Easy to integrate components and pipelines in your scikit-learn workflows and machine learning pipelines.\n - Easy serialization and integration with HugginFace Hub for quickly publishing your embedding pipelines.\n\n### What scikit-embeddings is not for:\n - Using pretrained embeddings in scikit-learn pipelines (for these purposes I recommend [embetter](https://github.com/koaning/embetter/tree/main))\n - Training transformer models and deep neural language models (if you want to do this, do it with [transformers](https://huggingface.co/docs/transformers/index))\n\n\n## Examples\n\n### Streams\n\nscikit-embeddings comes with a handful of utilities for streaming data from disk or other sources,\nchunking and filtering. Here\'s an example of how you would go about obtaining chunks of text from jsonl files with a "content field".\n\n```python\nfrom skembedding.streams import Stream\n\n# let\'s say you have a list of file paths\nfiles: list[str] = [...]\n\n# Stream text chunks from jsonl files with a \'content\' field.\ntext_chunks = (\n    Stream(files)\n    .read_files(lines=True)\n    .json()\n    .grab("content")\n    .chunk(10_000)\n)\n```\n\n### Word Embeddings\n\nYou can train classic vanilla word embeddings by building a pipeline that contains a `WordLevel` tokenizer and an embedding model:\n\n```python\nfrom skembedding.tokenizers import WordLevelTokenizer\nfrom skembedding.models import Word2VecEmbedding\nfrom skembeddings.pipeline import EmbeddingPipeline\n\nembedding_pipe = EmbeddingPipeline(\n    WordLevelTokenizer(),\n    Word2VecEmbedding(n_components=100, algorithm="cbow")\n)\nembedding_pipe.fit(texts)\n```\n\n### Fasttext-like\n\nYou can train an embedding pipeline that uses subword information by using a tokenizer that does that.\nYou may want to use `Unigram`, `BPE` or `WordPiece` for these purposes.\nFasttext also uses skip-gram by default so let\'s change to that.\n\n```python\nfrom skembedding.tokenizers import UnigramTokenizer\nfrom skembedding.models import Word2VecEmbedding\nfrom skembeddings.pipeline import EmbeddingPipeline\n\nembedding_pipe = EmbeddingPipeline(\n    UnigramTokenizer(),\n    Word2VecEmbedding(n_components=250, algorithm="sg")\n)\nembedding_pipe.fit(texts)\n```\n\n### Sense2Vec\n\nWe provide a spaCy tokenizer that can lemmatize tokens and append morphological information so you can get fine-grained\nsemantic information even on relatively small corpora. I recommend using this for literary analysis.\n\n```python\nfrom skembeddings.models import Word2VecEmbedding\nfrom skembeddings.tokenizers import SpacyTokenizer\nfrom skembeddings.pipeline import EmbeddingPipeline\n\n# Single token pattern that lets alphabetical tokens pass, but not stopwords\npattern = [[{"IS_ALPHA": True, "IS_STOP": False}]]\n\n# Build tokenizer that lemmatizes and appends POS-tags to the lemmas\ntokenizer = SpacyTokenizer(\n    "en_core_web_sm",\n    out_attrs=("LEMMA", "UPOS"),\n    patterns=pattern,\n)\n\n# Build a pipeline\nembedding_pipeline = EmbeddingPipeline(\n    tokenizer,\n    Word2VecEmbedding(50, algorithm="cbow")\n)\n\n# Fitting pipeline on corpus\nembedding_pipeline.fit(corpus)\n```\n\n### Paragraph Embeddings\n\nYou can train Doc2Vec paragpraph embeddings with the chosen choice of tokenization.\n\n```python\nfrom skembedding.tokenizers import WordPieceTokenizer\nfrom skembedding.models import ParagraphEmbedding\nfrom skembeddings.pipeline import EmbeddingPipeline\n\nembedding_pipe = EmbeddingPipeline(\n    WordPieceTokenizer(),\n    ParagraphEmbedding(n_components=250, algorithm="dm")\n)\nembedding_pipe.fit(texts)\n```\n\n### Iterative training\n\nIn the case of large datasets you can train on individual chunks with `partial_fit()`.\n\n```python\nfor chunk in text_chunks:\n    embedding_pipe.partial_fit(chunk)\n```\n\n### Serialization\n\nPipelines can be safely serialized to disk:\n\n```python\nembedding_pipe.to_disk("output_folder/")\n\nembedding_pipe = EmbeddingPipeline.from_disk("output_folder/")\n```\n\nOr published to HugginFace Hub:\n\n```python\nfrom huggingface_hub import login\n\nlogin()\nembedding_pipe.to_hub("username/name_of_pipeline")\n\nembedding_pipe = EmbeddingPipeline.from_hub("username/name_of_pipeline")\n```\n\n### Text Classification\n\nYou can include an embedding model in your classification pipelines by adding some classification head.\n\n```python\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import classification_report\n\nX_train, X_test, y_train, y_test = train_test_split(X, y)\n\ncls_pipe = make_pipeline(embedding_pipe, LogisticRegression())\ncls_pipe.fit(X_train, y_train)\n\ny_pred = cls_pipe.predict(X_test)\nprint(classification_report(y_test, y_pred))\n```\n\n\n### Feature Extraction\n\nIf you intend to use the features produced by tokenizers in other text pipelines, such as topic models,\nyou can use `ListCountVectorizer` or `Joiner`.\n\nHere\'s an example of an NMF topic model that use lemmata enriched with POS tags.\n\n```python\nfrom sklearn.decomposition import NMF\nfrom sklearn.pipelines import make_pipeline\nfrom sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer\nfrom skembedding.tokenizers import SpacyTokenizer\nfrom skembedding.feature_extraction import ListCountVectorizer\nfrom skembedding.preprocessing import Joiner\n\n# Single token pattern that lets alphabetical tokens pass, but not stopwords\npattern = [[{"IS_ALPHA": True, "IS_STOP": False}]]\n\n# Build tokenizer that lemmatizes and appends POS-tags to the lemmas\ntokenizer = SpacyTokenizer(\n    "en_core_web_sm",\n    out_attrs=("LEMMA", "UPOS"),\n    patterns=pattern,\n)\n\n# Example with ListCountVectorizer\ntopic_pipeline = make_pipeline(\n    tokenizer,\n    ListCountVectorizer(),\n    TfidfTransformer(), # tf-idf weighting (optional)\n    NMF(15), # 15 topics in the model \n)\n\n# Alternatively you can just join the tokens together with whitespace\ntopic_pipeline = make_pipeline(\n    tokenizer,\n    Joiner(),\n    TfidfVectorizer(),\n    NMF(15), \n)\n```\n',
    'author': 'Márton Kardos',
    'author_email': 'power.up1163@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
