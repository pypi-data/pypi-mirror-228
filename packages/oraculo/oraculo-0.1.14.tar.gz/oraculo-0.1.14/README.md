# Project: Oráculo

Oráculo is a versatile CLI and WebApp application developed for transcription of audios and semantic search. It leverages Sentence Transformers and embeddings to create a compact search engine that aids in retrieving and organizing important information from a collection of documents.

This application is particularly useful for professionals dealing with substantial amounts of audio data and requiring an efficient system to transcribe and conduct semantic search operations on the data.

## Features:

- Audio Transcription: Oráculo can transcribe audio files. You can transcribe a single file or bulk transcribe a folder.
- Semantic Search: A web app to perform semantic searches on the transcribed audio data.

## Requirements:

<!-- create an admonition for it -->
:warning: IMPORTANT :warning: In order to run Oráculo, you need to have the following requirements installed on your machine:

- Python 3.10
- FFmpeg
- Git

## Installation:

You can install Oráculo with pip:

```bash
pip install oraculo
```

## Setup:

:warning::warning:**Warning**:warning::warning:: The following steps are required to run Oráculo. Please follow the steps carefully.

Initialize the Oráculo application with the following command:

```bash
oraculo init
```

You will be prompted to enter the following information:
<!-- table -->
| Information | Description |
| ----------- | ----------- |
| ChromaDB Persist Directory | The directory where the ChromaDB will be stored. This is important to store vector embeddings of text|
| ChromaDB Implementation | Defaults to `duckdb+parquet`. For more implementations, please refer to [Source Code](https://github.com/chroma-core/chroma/blob/main/chromadb/config.py) |


Whenever you want to change the config file, just run the same command again.

## Usage:

### Semantic Search:
To start the Semantic Search Application, use the following command:

```bash
oraculo webapp
```

### Single File Transcription:
To initiate a transcription for a single file:

```bash
oraculo transcribe
```

### Multiple File Transcription:
To initiate bulk transcription for a folder:

```bash 
oraculo bulk-transcribe
```

to transcribe youtube videos:

### YouTube Video Transcription:
```bash
oraculo transcribe-yt
```


--- 
### Help:
If you need help with the commands, use the following command:

```bash
oraculo --help
```


## About

- Version: 0.1.14
- Author: Joao Tedeschi
- Contact: joaorafaelbt@gmail.com

The development of Oráculo is aimed at information retrieval capabilities for businesses and individual users. Please feel free to reach out with any feedback or suggestions to improve Oráculo further.
