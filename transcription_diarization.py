import boto3
import time
import json
import os
import urllib.parse
from moviepy.editor import VideoFileClip
import requests
from botocore.exceptions import ClientError
from config import aws_access_key_id, aws_secret_access_key

def convert_to_wav(video_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = f"{base_name}.wav"
    
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        
        # Write the audio to WAV file
        audio.write_audiofile(output_path, codec='pcm_s16le')
        
        video.close()
        audio.close()
        
        return output_path
    except Exception as e:
        print(f"Error during audio conversion: {str(e)}")
        return None

def upload_to_s3(local_file_path, bucket_name, s3_file_key):
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name='eu-central-1')
    s3_client.upload_file(local_file_path, bucket_name, s3_file_key)
    return f's3://{bucket_name}/{s3_file_key}'

def transcribe_audio(file_uri, job_name):
    transcribe = boto3.client('transcribe',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name='eu-central-1')

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='wav',
        IdentifyLanguage=True,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 4
        }
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(30)

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        identified_language = status['TranscriptionJob']['LanguageCode']
        print(f"Identified language: {identified_language}")
        return status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    else:
        print('Transcription Job returned None')
        return None

def download_transcript(transcript_url):
    try:
        response = requests.get(transcript_url)
        response.raise_for_status()
        return json.loads(response.text)
    except Exception as e:
        print(f"Error downloading transcript: {e}")
        return None

def extract_transcriptions_with_speakers(transcript_data):
    segments = transcript_data['results']['speaker_labels']['segments']
    items = transcript_data['results']['items']
    
    current_speaker = None
    current_text = []
    transcriptions = []
    
    speaker_mapping = {}
    speaker_count = 0

    for item in items:
        if item['type'] == 'pronunciation':
            start_time = float(item['start_time'])
            end_time = float(item['end_time'])
            content = item['alternatives'][0]['content']

            speaker_segment = next((seg for seg in segments if float(seg['start_time']) <= start_time and float(seg['end_time']) >= end_time), None)

            if speaker_segment:
                speaker_label = speaker_segment['speaker_label']
                
                # Map speaker labels to sequential numbers starting from 1
                if speaker_label not in speaker_mapping:
                    speaker_count += 1
                    speaker_mapping[speaker_label] = f"Speaker {speaker_count}"
                
                if speaker_mapping[speaker_label] != current_speaker:
                    if current_text:
                        transcriptions.append({
                            'speaker': current_speaker,
                            'text': ' '.join(current_text)
                        })
                        current_text = []
                    current_speaker = speaker_mapping[speaker_label]

            current_text.append(content)
        elif item['type'] == 'punctuation':
            current_text[-1] += item['alternatives'][0]['content']

    if current_text:
        transcriptions.append({
            'speaker': current_speaker,
            'text': ' '.join(current_text)
        })

    return transcriptions

def diarize_audio(video_path):
    # Convert video to WAV audio
    wav_path = convert_to_wav(video_path)
    
    if not wav_path:
        return "Audio conversion failed."
    
    bucket_name = 'transcriptionjobbucket'
    s3_file_key = os.path.basename(wav_path)
    file_uri = upload_to_s3(wav_path, bucket_name, s3_file_key)

    job_name = f'transcription_job_{int(time.time())}'
    transcript_url = transcribe_audio(file_uri, job_name)
    
    print('transcript url:', transcript_url)

    if transcript_url:
        transcript_data = download_transcript(transcript_url)
        if transcript_data is None:
            return "Failed to download transcript."
        
        transcriptions = extract_transcriptions_with_speakers(transcript_data)
        print('transcriptions:', transcriptions)

        output = []
        for i, trans in enumerate(transcriptions, 1):
            output.append(f"[{i}. {trans['speaker']} | text: {trans['text']}]\n")

        # Clean up: remove the temporary WAV file
        os.remove(wav_path)

        return '\n'.join(output)
    else:
        return "Transcription failed."