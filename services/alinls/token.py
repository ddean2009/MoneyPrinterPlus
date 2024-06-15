# Copyright (c) Alibaba, Inc. and its affiliates.

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from .exception import GetTokenFailed

import json

__all__ = ['getToken']

def getToken(akid, aksecret, domain='cn-shanghai',
             version='2019-02-28',
             url='nls-meta.cn-shanghai.aliyuncs.com'):
    """
    Help methods to get token from aliyun by giving access id and access secret
    key

    Parameters:
    -----------
    akid: str
        access id from aliyun
    aksecret: str
        access secret key from aliyun
    domain: str:
        default is cn-shanghai
    version: str:
        default is 2019-02-28
    url: str
        full url for getting token, default is
        nls-meta.cn-shanghai.aliyuncs.com
    """
    if akid is None or aksecret is None:
        raise GetTokenFailed('No akid or aksecret')
    client = AcsClient(akid, aksecret, domain)
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain(url)
    request.set_version(version)
    request.set_action_name('CreateToken')
    response = client.do_action_with_exception(request)
    response_json = json.loads(response)
    if 'Token' in response_json:
        token = response_json['Token']
        if 'Id' in token:
            return token['Id']
        else:
            raise GetTokenFailed(f'Missing id field in token:{token}') 
    else:
        raise GetTokenFailed(f'Token not in response:{response_json}')
