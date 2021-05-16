import traceback

def traceback_throw(err,advance:bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = (f'```py\n{err}{type(err).__name__}\n```')
    return error if advance else f"{type(err).__name__}: {err}"


