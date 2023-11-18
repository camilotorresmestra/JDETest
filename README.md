# Technical Assessment: Migrating a Data Pipeline to Production
```
Scaling a Youtube video transcriber from a prototype in notebook to a production environment
```
## Introduction

This repository contains the scritps and files used in the implementation of the pipeline. The goal is to store the transcription of YouTube videos in a database. The pipeline is an ELTL (Extract, Load, Transform, Load) pipeline.
1. Extract: The Youtube metadata is extracted using the pytube API.
2. Load: The Youtube video is downloaded and the metadata is stored in a database.
3. Transform: The audio is extracted and then it is transcribed using the OpenAI Whisper API. The transcription is stored in the database.
4. Load: The transcriptions are loaded onto the pg database.
![ETL(2)](https://github.com/camilotorresmestra/JDETest/assets/15526142/e9995a82-f07d-45a3-88e9-588815de8ef7)

### Data Modelling
The proposed database consists of two tables. The first table 'video' basically contains metadata from the video that can be extracted with the pytube library.  The video ID is the primary key since it references the object.
The data is pre-processed in batches and loaded onto this table.

The second table in the schema is the transcriptions table itself. The table has a foreign key that matches an id in the first table, the relationship is hypothetically one to many because, since the Transcription API is not deterministic one can expect to have a non-identical output each time. By changing certain criteria in the script one can force the re-extraction of metadata from each video id, and by detecting significant changes (for example in the format or the filesize when a video is edited), an action can be triggered to re-transcribe the video and push it as a new row with the same id, since the changes are significant.

![Untitled](https://github.com/camilotorresmestra/JDETest/assets/15526142/a5d01a00-f032-461c-a4e5-1dfcf534a48c)


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
