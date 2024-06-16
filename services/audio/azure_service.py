import os

from config.config import my_config
from services.audio.audio_service import AudioService
from tools.utils import must_have_value

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-text-to-speech-python for
    installation instructions.
    """)
    import sys

    sys.exit(1)

# audio_provider = my_config['audio']['provider']
# speech_key = my_config['audio']['Azure']['speech_key']
# service_region = my_config['audio']['Azure']['service_region']



class AzureAudioService(AudioService):

    def __init__(self):
        super().__init__()
        self.audio_provider = my_config['audio']['provider']
        self.speech_key = my_config['audio']['Azure']['speech_key']
        self.service_region = my_config['audio']['Azure']['service_region']
        must_have_value(self.audio_provider, "请设置audio provider")
        must_have_value(self.speech_key, "请设置Azure speech_key")
        must_have_value(self.service_region, "请设置Azure speech_key")

    def my_speech_synthesis_to_wave_file(self, text, file_name, voice="zh-CN-XiaoyiNeural"):
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        print(file_name)
        file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
        speech_config.speech_synthesis_voice_name = voice
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

        # Receives a text from console input and synthesizes it to wave file.
        result = speech_synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

    def my_speech_synthesis_to_wave_file_ssml(self, text, file_name):
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        print(file_name)
        file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
        # speech_config.speech_synthesis_voice_name = voice
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

        # Receives a text from console input and synthesizes it to wave file.
        result = speech_synthesizer.speak_ssml_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
            return True
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
            return False
        else:
            print("Speech synthesis error: {}".format(result))
            return False

    def speech_synthesis_with_voice(self, text, voice):
        """performs speech synthesis to the default speaker with specified voice"""
        # Creates an instance of a speech config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        # Sets the synthesis voice name.
        # e.g. "en-US-AndrewMultilingualNeural".
        # The full list of supported voices can be found here:
        # https://aka.ms/csspeech/voicenames
        # And, you can try get_voices_async method to get all available voices.
        # See speech_synthesis_get_available_voices() sample below.
        # voice = "en-US-AndrewMultilingualNeural"
        speech_config.speech_synthesis_voice_name = voice
        # Creates a speech synthesizer for the specified voice,
        # using the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        # Receives a text from console input and synthesizes it to speaker.
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}] with voice [{}]".format(text, voice))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

    def speech_synthesis_with_voice_ssml(self, ssml):
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        # voice = "zh-CN-XiaoyiNeural"
        # speech_config.speech_synthesis_voice_name = voice
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        result = speech_synthesizer.speak_ssml_async(ssml).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for ssml".format(ssml))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

    # save to file
    def save_with_ssml(self, text, file_name, voice, rate="0.00"):
        ssml = f"""
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        <voice name="{voice}">
            <prosody rate="{rate}%">
                {text}
            </prosody>
        </voice>
        </speak>
        """
        result = self.my_speech_synthesis_to_wave_file_ssml(ssml, file_name)
        # 如果出现异常，重试一次
        if not result:
            os.remove(file_name)
            self.my_speech_synthesis_to_wave_file_ssml(ssml, file_name)

    def read_with_ssml(self, text, voice, rate="0.00"):
        ssml = f"""
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        <voice name="{voice}">
            <prosody rate="{rate}%">
                {text}
            </prosody>
        </voice>
        </speak>
        """
        self.speech_synthesis_with_voice_ssml(ssml)
