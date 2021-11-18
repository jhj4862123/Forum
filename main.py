                            # Copyrighted by ZOAS(STT ver1.0)
"""패키지는 pip install google, pip install google-cloud, pip install google-storage 세개 하면 됩니다.
JSON 파일은 환경변수에 지정해두면 매번 불러올 필요 없으니 코드에 안 적어뒀음."""

from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech

import sys

""" 업로드하는 부분 """

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} 가 {} 이름으로 업로드 되었습니다.".format( filename, destination_blob_name )
    )
    return upload_blob
    print("Upload complete!")

def google_transcribe(filename):
    gcs_uri = 'gs://zoastts-1/' + filename
    transcript = ""

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    speech_context = speech.SpeechContext(phrases=['가방','날개','개나리']) # https://cloud.google.com/speech-to-text/docs/context-strength , https://cloud.google.com/speech-to-text/docs/speech-adaptation text adaptation 할 곳.

    config = speech.RecognitionConfig(
    sample_rate_hertz = 16000,  # 헤르츠 부분
    language_code = "ko-KR",  # 인식언어 부분
    encoding = speech.RecognitionConfig.AudioEncoding.FLAC,  # 오디오 포맷 바꿀때 여기만 건들기 ex. LINEAR16,FLAC,등등...
    enable_automatic_punctuation = True,  # 자동구두점 부분
    enable_word_time_offsets = True,  # 타임스탬프 삽입부분
    speech_contexts = [speech_context],  # 스피치 컨텍스트 부분
    profanity_filter = False, #욕설 필터링 부분
    )
    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result()  # 타임아웃 옵션 없음

    for result in response.results:
        alternative = result.alternatives[0]
        transcript += alternative.transcript + "\n" # transcript 저장 부분
        """ 여기는 단어 타임스탬프 적용하는 부분인데 주석처리 풀면 일단 쉘에만 나올거. 일단 비활성화해둘게요 
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )"""
    return transcript

def write_transcripts(transcript_filename, transcript):
    f = open(transcript_filename, 'w', encoding='UTF-8')
    f.write(transcript)
    f.close()

filename = str(sys.argv[1])
print(filename + "의 업로드 및 다운로드를 실행하겠습니다.")
print("Start uploading...")
upload_blob('zoastts-1', "C:/Users/hyo/Desktop/p/" + filename, "" + filename)
# 끊어칠곳.
print("업로드 완료. 스크립트 다운로드 작업을 시작합니다...\n")
sentences = {}
output = google_transcribe(filename)
print("스크립트 다운로드가 완료되었습니다.")
write_transcripts(filename + "-script.txt", output)
print("스크립트 파일이 저장되었습니다.")
