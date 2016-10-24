import functools

def get(path):
    '''
    Define decorator @get('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator

@get('/')
def demo(oop):
    print("asdasdasdggg")
    return oop

print(demo("test"))