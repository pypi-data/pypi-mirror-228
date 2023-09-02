class SatiDict(dict):
    ''' dict wrapper for using convenient dot-notation '''
    def __getattr__(self, key: str):
        if isinstance(self[key], dict):
            return SatiDict(self[key])
        return self[key]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__