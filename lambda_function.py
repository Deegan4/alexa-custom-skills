import json
import os
import requests

def lambda_handler(event, context):
    try:
        query = event['request']['intent']['slots']['Query']['value']
    except:
        query = 'What the fuck is up?'
    
    ollama_url = os.environ.get('OLLAMA_URL', 'http://192.168.1.100:11434/api/chat')
    payload = {
        'model': 'llama3.1',
        'messages': [{'role': 'user', 'content': f'Respond casually and use curse words if it fits: {query}'}],
        'stream': False
    }
    
    try:
        r = requests.post(ollama_url, json=payload)
        reply = r.json()['message']['content']
    except:
        reply = "Ollama not responding, you lazy shit."
    
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {'type': 'PlainText', 'text': reply},
            'shouldEndSession': False
        }
    }
