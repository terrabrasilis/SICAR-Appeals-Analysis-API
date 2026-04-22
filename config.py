import os


class Config:
    # used for frontend App
    SCRIPT_NAME = os.environ.get('SCRIPT_NAME') or ''