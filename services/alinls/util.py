# Copyright (c) Alibaba, Inc. and its affiliates.

from struct import *

__all__=['wav2pcm', 'GetDefaultContext']

def GetDefaultContext():
    """
    Return Default Context Object
    """
    return {
        'sdk': {
            'name': 'nls-python-sdk',
            'version': '0.0.1',
            'language': 'python'
        }
    }


def wav2pcm(wavfile, pcmfile):
    """
    Turn wav into pcm
    
    Parameters
    ----------
    wavfile: str
        wav file path
    pcmfile: str
        output pcm file path
    """
    with open(wavfile, 'rb') as i, open(pcmfile, 'wb') as o:
        i.seek(0)
        _id = i.read(4)
        _id = unpack('>I', _id)
        _size = i.read(4)
        _size = unpack('<I', _size)
        _type = i.read(4)
        _type = unpack('>I', _type)
        if _id[0] != 0x52494646 or _type[0] != 0x57415645:
            raise ValueError('not a wav!')
        i.read(32)
        result = i.read()
        o.write(result)

