import os
import requests


def _say(text, end=False, reprompt=None):
    response = {
        "outputSpeech": {"type": "PlainText", "text": text},
        "shouldEndSession": end,
    }
    if not end and reprompt:
        response["reprompt"] = {
            "outputSpeech": {"type": "PlainText", "text": reprompt}
        }
    return {"version": "1.0", "response": response}


def _ask_ollama(query):
    url = os.environ.get("OLLAMA_URL", "http://192.168.1.100:11434/api/chat")
    payload = {
        "model": os.environ.get("OLLAMA_MODEL", "llama3.1"),
        "messages": [
            {"role": "user", "content": f"Respond casually and use curse words if it fits: {query}"}
        ],
        "stream": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=7)
        r.raise_for_status()
        return r.json()["message"]["content"]
    except Exception:
        return "Ollama is not responding right now. Try again in a moment."


def lambda_handler(event, context):
    request = event.get("request", {})
    rtype = request.get("type")

    if rtype == "LaunchRequest":
        return _say(
            "Ollama Brain is online. Ask me anything.",
            reprompt="Ask me anything, or say 'stop' to quit.",
        )

    if rtype == "SessionEndedRequest":
        return _say("", end=True)

    if rtype == "IntentRequest":
        intent_name = request.get("intent", {}).get("name", "")

        if intent_name == "OllamaIntent":
            slots = request.get("intent", {}).get("slots", {})
            query = (slots.get("Query") or {}).get("value") or ""
            if not query:
                return _say(
                    "I didn't catch a question. Try asking again.",
                    reprompt="What's your question?",
                )
            return _say(_ask_ollama(query), reprompt="Anything else?")

        if intent_name == "AMAZON.HelpIntent":
            return _say(
                "Ask me a question and I'll send it to your local Ollama server. "
                "For example, say 'tell me about quantum computing'.",
                reprompt="What would you like to ask?",
            )

        if intent_name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
            return _say("Goodbye.", end=True)

        if intent_name == "AMAZON.NavigateHomeIntent":
            return _say("Going home.", end=True)

        if intent_name == "AMAZON.FallbackIntent":
            return _say(
                "I didn't understand. Try asking a question, or say 'help'.",
                reprompt="What's your question?",
            )

    return _say("Something went wrong. Please try again.", end=True)
