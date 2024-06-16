import os

def get_locale():
    language = os.getenv("LOCALE", "en")
    if language == "ru":
        from .ru import locale
    else:
        from .en import locale
    return locale
