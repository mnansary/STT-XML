#-----------------------------------------------------
# imports
#---------------------------------------------------
from transformers import AutoFeatureExtractor, pipeline
import librosa 
from wit import Wit
import os
from dotenv import load_dotenv


#---------------------------------------------
# fixed globals
#---------------------------------------------
load_dotenv()
model_name = os.getenv("WIT_CLIENT")
access_token=os.getenv("STT_MODEL")
#---------------------------------------------
# model instances
#---------------------------------------------
# wit
client = Wit(access_token)
# stt
asr = pipeline("automatic-speech-recognition", model=model_name, device=-1)
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name, cache_dir=None, use_auth_token=False)

#------------------------------------------------------------------------------------
def get_processed_text(text):
    resp=client.message(text)
    data={}
    data["text"]=resp["text"]
    data["intent"]=resp["intents"][0]["name"]
    if "service" in resp["traits"].keys():
        data["service"]=resp["traits"]["service"][0]["value"]
    else:
        data["service"]="others"
    if 'wit$agenda_entry:agenda_entry' in resp["entities"].keys():
        ents=[]
        for en in resp["entities"]['wit$agenda_entry:agenda_entry']:
            ents.append(en["value"])
        data["agendas"]=",".join(ents)
    return data
#------------------------------------------------------------------------------------
def read_file(file_path):
    try:
        speech, sr = librosa.load(file_path, sr=feature_extractor.sampling_rate)
        return speech
    except Exception as e:
        read_file(file_path)

def get_text(file_path):
    speech=read_file(file_path,feature_extractor)
    prediction = asr(speech, chunk_length_s=112, stride_length_s=None)
    pred = prediction["text"]
    return pred
#------------------------------------------------------------------------------------
def process(file_path):
    text=get_text(file_path)
    print("STT Result:",text)
    data=get_processed_text(text)
    print("Processed:",data)
    return data
