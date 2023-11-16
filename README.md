# Technical Assessment: Migrating a Data Pipeline to Production
```
Scaling a Youtube video transcriber from a prototype in notebook to a production environment
```
## Introduction

This repository contains the scritps and files used in the implementation of the pipeline. The goal is to store the transcription of Youtube videos in a database. The pipeline is an ELT (Extract, Load, Transform) pipeline.
1. Extract: The Youtube metadata is extracted using the pytube API.
2. Load: The Youtube video is downloaded and the metadata is stored in a database.
3. Transform: The video is transcribed using the OpenAI Whisper API. The transcription is stored in the database.

## Implementation

The pipeline is implemented using the following technologies:
- Python 3.8
- Docker
- PostgreSQL
- SQLAlchemy



