from py4j.java_gateway import JavaGateway
import requests
import pyaudio
import wave
import json


APIKEY = '6f52656b487370725637707565333842424866655a4c61353751513650414c754236707041534d7a486d33'

gateway = JavaGateway()
random = gateway.jvm.java.util.Random()

CHUNK = 1024
FORMAT = pyaudio.paInt16 # int16型
CHANNELS = 1             # ステレオ
RATE = 16000             # 441.kHz
RECORD_SECONDS = 3       # 5秒録音
WAVE_OUTPUT_FILENAME = "output.wav"


switch = 1

while switch==1:

    print("(1)会話 (0)終了")
    key = input()
    if int(key)==1:
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        recurl = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(APIKEY)
        files = {"a": open('output.wav', 'rb'), "v":"on"}
        r = requests.post(recurl, files=files)
        text = r.json()['text']
        print("me:"+r.json()['text'])


        aijson = {
            "utt":text,

        }

        AIurl = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY={}".format(APIKEY)
        air = requests.post(AIurl,json.dumps({"utt":text}), headers={'Content-Type': 'application/json'})
        resp = air.json()['utt']
        print("miku:"+resp)

        addiction_app = gateway.entry_point
        addiction_app.talk(resp)

    elif int(key)==0:
        addiction_app = gateway.entry_point
        addiction_app.talk("バイバイ")
        gateway.shutdown()
        print("終了しました")
        switch = 0


