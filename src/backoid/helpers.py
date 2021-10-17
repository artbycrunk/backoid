
# ----------------------------- Metaclass ---------------------
class MetaSingleton(type):
    
    def __init__(cls, name, bases, dic):
        super(MetaSingleton, cls).__init__(name, bases, dic)
        cls.instance = None
    
    def __call__(cls, *args, **kwargs):
        if cls.instance is not None:
            return cls.instance
        cls.instance = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls.instance
