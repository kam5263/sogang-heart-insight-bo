import openai
from flask import current_app
from openai import OpenAI

def get_openai_client():
    openai.api_key = current_app.config['OPENAI_API_KEY']
    return OpenAI(api_key=openai.api_key)