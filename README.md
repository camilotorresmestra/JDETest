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
- Python 3.10
- Docker
- Pandas
- PostgreSQL
- SQLAlchemy

## How to run

1. Clone the repository
2. Set the environment variables under the configs folder in the db_cred.env file
```bash
db_user=
db_host=
db_name=jde_test
db_password=
db_port=
pg_admin_email=
pg_admin_password=
```
3. Set the api_key in the configs folder in the api_key.env file
```bash
OPENAI_API_KEY=
```
4. Set the ssh connection with the virtual machine.
5. Run the following command to start the pipeline
```bash
ssh user@host 'docker compose -f "src/jde_test/docker-compose.yml" --env-file=src/jde_test/configs/db_creds.env up -d --build'
```