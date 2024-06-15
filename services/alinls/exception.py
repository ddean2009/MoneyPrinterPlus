# Copyright (c) Alibaba, Inc. and its affiliates.


class InvalidParameter(Exception):
    pass

# Token
class GetTokenFailed(Exception):
    pass

# Connection
class ConnectionTimeout(Exception):
    pass

class ConnectionUnavailable(Exception):
    pass

class StartTimeoutException(Exception):
    pass

class StopTimeoutException(Exception):
    pass

class NotStartException(Exception):
    pass

class CompleteTimeoutException(Exception):
    pass