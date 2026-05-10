import random

def lambda_handler(event, context):
    intent_name = event['request']['intent']['name']
    if intent_name == "SwearIntent":
        responses = [
            "Fuck yeah, what the hell do you want, you magnificent bastard?",
            "Shit, you're looking fine today.",
            "What the actual fuck is up?"
        ]
        speech_text = random.choice(responses)
    else:
        speech_text = "The fuck you just say?"
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": speech_text},
            "shouldEndSession": False
        }
    }