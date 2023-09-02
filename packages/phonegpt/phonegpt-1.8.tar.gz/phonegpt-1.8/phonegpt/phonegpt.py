from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Start, Stream

import openai


import vosk
import audioop
import base64
import json

import time

import threading


    
class Twilio:
    ACCOUNT_SID = None
    AUTH_TOKEN = None
    client = None
    call_sid = None
    stream_url = None
    max_wait_time_for_new_command = 600
    
    def __init__(self, phone_gpt_object, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN):
        self.phone_gpt_object = phone_gpt_object        
        self.ACCOUNT_SID = TWILIO_ACCOUNT_SID
        self.AUTH_TOKEN = TWILIO_AUTH_TOKEN
        self.client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)

    def answer_call_with_async_audio_stream(self, call_sid, stream_url, intro_mesaage, voice):
        self.stream_url = stream_url
        self.call_sid = call_sid
        response = VoiceResponse()
        response.say(intro_mesaage, voice=voice)
        start = Start()
        stream_inbound = Stream(url=self.stream_url, track="both_tracks")
        start.append(stream_inbound)
        response.append(start)
        response.pause(self.max_wait_time_for_new_command)
        return str(response)


    def say_and_wait(self, text, voice):
        response = VoiceResponse()
        response.say(text, voice=voice)
        response.pause(self.max_wait_time_for_new_command)

        try:
            call = self.client.calls(str(self.call_sid))
            call.update(twiml=str(response))
            self.phone_gpt_object.vosk.outbound_silence_limit = 100
            print("Saying: ", text)
            return True
        except Exception as e:
            print("Error in running command with provided xml: ", str(response), e)
            return None
        
    def send_text_message(self, from_phone_number, to_phone_number, message_body):
        message = self.client.messages.create(
            body=message_body,
            from_=from_phone_number,
            to=to_phone_number
        )
        return message
            
    
        
    
class Openai:
    API_KEY = None

    gpt_role = "If you receive an incomplete or unclear grammatical command from me, please make a guess about my intention/command/question and provide assistance accordingly."
    max_tokens = 90
    temperature = 0
    model = "gpt-3.5-turbo"

    messages = []

    def __init__(self, phone_gpt_object, OPENAI_API_KEY):
        self.phone_gpt_object = phone_gpt_object    
        self.API_KEY = OPENAI_API_KEY


    
    def get_gpt_response(self, user_msg, gpt_role):
        openai.api_key = self.API_KEY
        if self.messages == []:
            self.messages = [{"role": "system", "content": gpt_role}]
        self.messages.append({"role": "user", "content": user_msg})
        completion = openai.ChatCompletion.create(
        model=self.model,
        max_tokens=self.max_tokens,
        temperature=self.temperature,
        messages = self.messages
        )
        self.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion.choices[0].message.content

class Vosk:
    MODEL_PATH = None
    model = None
    continue_transcribing = True
    outbound_silence_limit = 5000

    silence_time_out = 2
    
    def __init__(self, phone_gpt_object, VOSK_MODEL_PATH):
        self.phone_gpt_object = phone_gpt_object
        self.MODEL_PATH = VOSK_MODEL_PATH
        self.model = vosk.Model(self.MODEL_PATH)

    def speech_to_text_from_stream(self, ws):
        """Receive and transcribe audio stream with vosk."""
        print("ws is coming")
        CL='\x1b[0K'
        BS='\x08'
        accepted_input = ""
        silence_start_time = None
        
        rec = vosk.KaldiRecognizer(self.model, 16000)
        while True:
            message = ws.receive()
            packet = json.loads(message)
            if packet['event'] == 'start':
                print('Streaming is starting')
            elif packet['event'] == 'stop':
                print('\nStreaming has stopped')
            elif (packet['event'] == 'media'):
                if self.continue_transcribing == False:
                    if packet['media']['track'] == 'outbound':
                        self.outbound_silence_limit += 1
                    else:
                        self.outbound_silence_limit -= 1
                    
                    if self.outbound_silence_limit < 0:
                        self.continue_transcribing = True
                        self.outbound_silence_limit = 5000
                    else:
                        continue
                
                audio = base64.b64decode(packet['media']['payload'])
                audio = audioop.ulaw2lin(audio, 2)
                audio = audioop.ratecv(audio, 2, 1, 8000, 16000, None)[0]
            
                if rec.AcceptWaveform(audio):
                    r = json.loads(rec.Result())                  
                    silence_start_time = time.time()
                    accepted_input += r['text']
                    print(CL + r['text'] + ' ', end='', flush=True)
                else:
                    if silence_start_time is not None:
                        if accepted_input.replace(" ","") == "":
                            # accepted_input is empty                            
                            silence_start_time = time.time()
                        if time.time() - silence_start_time > self.silence_time_out:
                            self.continue_transcribing = False
                            threading.Thread(target=self.phone_gpt_object.on_new_user_input, args=(accepted_input,)).start()
                            accepted_input = ""
                            continue
                    else:
                        pass
                    r = json.loads(rec.PartialResult())
                    print(CL + r['partial'] + BS * len(r['partial']), end='', flush=True)





class PhoneGPT:

        
    def __init__(self, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, OPENAI_API_KEY, VOSK_MODEL_PATH, ON_NEW_MSG_FUNC=None):
        self.twilio = Twilio(self, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.openai = Openai(self, OPENAI_API_KEY)
        self.vosk = Vosk(self, VOSK_MODEL_PATH)
        if ON_NEW_MSG_FUNC is not None:
            self.on_new_user_input = ON_NEW_MSG_FUNC

    def on_new_user_input(self, new_user_msg):
            response = self.get_gpt_response(new_user_msg)
            self.say_and_wait(response)

    def answer_call_with_async_audio_stream(self, call_sid, stream_url, intro_mesaage='Hi there! How can I help you today?', voice='Google.en-US-Standard-J'):
        return self.twilio.answer_call_with_async_audio_stream(call_sid, stream_url, intro_mesaage, voice)

    def say_and_wait(self, text = '', voice='Polly.Salli-Neural'):
        self.twilio.say_and_wait(text, voice)

    def send_text_message(self, from_phone_number=None, to_phone_number=None, message_body='The body is empty.'):
        if from_phone_number is None:
            from_phone_number = self.twilio.client.incoming_phone_numbers.list()[0].phone_number
        if to_phone_number is None:
            to_phone_number = self.twilio.client.incoming_phone_numbers.list()[0].phone_number
        return self.twilio.send_text_message(from_phone_number, to_phone_number, message_body)

    
    def get_gpt_response(self, user_msg = '', gpt_role=Openai.gpt_role):
        return self.openai.get_gpt_response(user_msg, gpt_role)
    
    def speech_to_text_from_stream(self, ws):
        self.vosk.speech_to_text_from_stream(ws)


