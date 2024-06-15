from abc import ABC, abstractmethod


class AudioService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def save_with_ssml(self, text, file_name, voice, rate="0.00"):
        pass

    @abstractmethod
    def read_with_ssml(self, text, voice, rate="0.00"):
        pass