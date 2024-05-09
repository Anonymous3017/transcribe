import urllib
import urllib.request
import boto3
import time
import json
 
transcribe = boto3.client("transcribe")
 
def transcribe_file(job_name,file_url,transcribe):
    transcribe.start_transcription_job(
        TranscriptionJobName = job_name,
        Media = {"MediaFileUri":file_url},
        MediaFormat = "mp3",
        LanguageCode = "en-US"
    )
    max_tries = 60
    while max_tries >0:
        max_tries-= 1
        job = transcribe.get_transcription_job(TranscriptionJobName = job_name)
        job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status in ["COMPLETED","FAILED"]:
            print(f'Job: {job_name} is {job_status}')
            if job_status == "COMPLETED":
                response = urllib.request.urlopen(job["TranscriptionJob"]["Transcript"]["TranscriptFileUri"])
                data = json.loads(response.read())
                text = data["results"]["transcripts"][0]["transcript"]
                print("******************Output : sppech to text****************")
                print(text)
                print("==========================================")
 
            break    
 
        else:
            print(f"Waiting for {job_name} to process. Current status :{job_status}")
       
        time.sleep(10)
 
def main():
    file_url = "s3://van-buck-kendra/ayush.mp3"
    transcribe_file("ayush", file_url,transcribe)
 
 
if __name__ == "__main__":
    main()