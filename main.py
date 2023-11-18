import pandas as pd
import logging
import argparse
import tempfile
from pathlib import Path

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    # test_run:
    logging.basicConfig(level=logging.INFO)
    tmpdirname = tempfile.TemporaryDirectory()

    # parse the arguments
    parser = argparse.ArgumentParser(description='ETL pipeline for youtube videos and transcriptions')
    parser.add_argument('--video_id', type=str, nargs='+', help='video id to extract')
    parser.add_argument('--video_id_file', type=str, help='path to the txt file containing video ids to extract')
    args = parser.parse_args()
    
    if args.video_id:
        video_id = args.video_id
    elif args.video_id_file:
        #open text file and read the video ids
        video_id = open(args.video_id_file, "r").read().splitlines()
    else:
        raise ValueError("No video id or video id file provided")
    
    from datetime import datetime
    start_time = datetime.now()
    logger.info(f"Starting ETL at {start_time}")
    logger.info("#"*75)
    logger.info("STAGE 1: Extracting video metadata")
    
    
    # first test if the ids are valid
    # TODO: add a test for this
    # Chcek if the video_id is already in the database
    from scripts.pg_utils import ENGINE
    conn = ENGINE.connect()
    video = pd.read_sql_table(table_name="video",schema="videos", con=conn, columns=["id"])
    conn.close()
    video_id = list(set(video_id) - set(video.id))
    try:
        assert len(video_id) > 0
    except AssertionError:
        logger.info("All videos are already in the database")
        # jump to stage 2
        pass
    logger.info(f"Found {len(video_id)} new videos to extract")

    # TODO: add a test to validate metadata has not changed
    if len(video_id) > 0:
        from scripts.video_extractor import extract_metadata
        metadata = [extract_metadata(i) for i in video_id]
        video_temp = pd.DataFrame(metadata)
        video_temp["id"] = video_id
        # Now set the new index
        video_temp = video_temp.set_index("id").rename_axis(None, axis=1)
        assert video_temp.shape[0] == len(video_id), "Failed to extract all the videos"

        # TODO: add tests

        # push it to the database
        from scripts.pg_utils import insert_to_db
        try:
            #insert videos data to the database
            status = insert_to_db(video_temp, schema="videos", table_name="video")
        except Exception as e:
            logging.warning(e)
            logging.warning("Failed to insert video metadata to the database")
        
        assert status == True, "Failed to insert video metadata to the database"
        logger.info(f"Successfully inserted {video_temp.shape[0]} videos to the database")
    ############################################################################################################
    #STAGE 2
    ############################################################################################################
    logger.info("#"*75)
    conn = ENGINE.connect()
    # query the database for the video metadata
    logger.info("STAGE 2: Extracting video transcription")
    logger.info("#"*75)
    logger.info("Querying the database for videos to transcribe")
    try:
        videos_to_transcribe = pd.read_sql_query("SELECT v.* FROM videos.video v left JOIN videos.transcription t ON v.id=t.video_id where t is null", conn)
        conn.close()
    except Exception as e:
        logger.warning(e)
        logger.warning("Failed to query the database for videos to transcribe")
    else:
        videos_to_transcribe = videos_to_transcribe.set_index("id").rename_axis(None, axis=1)
        logger.info(f"Found {videos_to_transcribe.shape[0]} videos to transcribe")
        #download the audio files for the videos
        if videos_to_transcribe.shape[0] > 0:
            from scripts.video_extractor import get_audio_stream
            logging.info("Extracting audio files")
            try:
                audios = videos_to_transcribe.apply(lambda x: get_audio_stream( x.name, x["itag"]).download(output_path=tmpdirname.name, filename=f"{x.name}.mp3"), axis=1)
            except Exception as e:
                logger.warning(e)
                logger.warning("Failed to extract audio files")
            #test the transcription fucntion
            from scripts.video_extractor import get_transcription
            
            transcriptions = videos_to_transcribe.apply(lambda x: get_transcription(x.name, tmpdirname.name), axis=1)

            # set index name
            transcriptions = transcriptions.to_frame()
            transcriptions.rename(columns={0: 'transcription'}, inplace=True)
            transcriptions.index.name = "video_id"
            
            #push it to the database
            from scripts.pg_utils import insert_to_db
            logger.info("Pushing transcription to the database")
            try:
                insert_to_db(transcriptions, schema="videos", table_name="transcription")
            except Exception as e:
                logger.warning(e)
                logger.warning("Failed to insert transcription to the database")
    #delete the temporary directory
    tmpdirname.cleanup()
    time_elapsed = datetime.now() - start_time
    logger.info(f"ETL Completed. Time elapsed:{time_elapsed}")