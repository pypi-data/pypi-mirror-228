from functools import wraps

from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.utils.authenticator import Authenticator


def spoof_user_agent(user_agent_value, get_function):
    @wraps(get_function)
    def wrapper(*args, **kwargs):
        kwargs = dict(**kwargs)  # In case dict type is immutable
        if kwargs and 'headers' in kwargs:
            kwargs['headers'] = {**(kwargs['headers'] or {}), 'User-agent': user_agent_value}
        else:
            kwargs['headers'] = {'User-agent': user_agent_value}
        return get_function(*args, **kwargs)

    return wrapper


class SpooferPlugin(ApplicationPlugin):
    def activate(self, *args, **kwargs):
        # Spoofing User agent information with a different header
        Authenticator.get = spoof_user_agent('curl/7.54.1', Authenticator.get)
        Authenticator.post = spoof_user_agent('curl/7.54.1', Authenticator.post)
