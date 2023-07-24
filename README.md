# Corpus Reader
A fast and memory-efficient indexing tool for reading large-scale corpora.

## Introduction
`CorpusReader` is a Python class designed to efficiently access documents in a corpus using an index. This tool is particularly useful for large-scale corpora where standard reading methods might be memory-intensive.

## Usage

### Initialization
```python
from corpus_reader import CorpusReader
reader = CorpusReader(index_path="path_to_index", verbose=True)
```

### Fetching a Document
You can fetch a document by its ID (string) or by its index (integer).
```python
doc = reader["document_id"]
doc = reader[index]
```

### Getting the Number of Documents
```python
num_docs = len(reader)
```

### Converting Data to String
```python
str_data = reader.to_str(data)
```

### Building an Index for Data
This method allows you to build an index file for a given data file.
```python
reader.build_index(data_path="path_to_data", index_path="path_for_index", keys=["key1", "key2"], verbose=True)
```

## Methods
- __init__(index_path: str, verbose: bool=False): Initialize the corpus reader.
- __del__(): Clean up resources.
- __getitem__(index: Union[int, str]) -> str: Fetch a document by its ID or index.
- __len__() -> int: Return the number of documents in the corpus.
- to_str(data: Union[str, list]) -> str: Convert data into string representation.
- build_index(data_path: str, index_path: str, keys: List[str], verbose: bool=False): Build an index file.
