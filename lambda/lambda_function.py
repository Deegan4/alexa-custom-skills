import random

SWEARS = [
    "Fuck yeah, what the hell do you want, you magnificent bastard?",
    "Shit, you're looking fine today.",
    "What the actual fuck is up?",
]


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


def lambda_handler(event, context):
    request = event.get("request", {})
    rtype = request.get("type")

    if rtype == "LaunchRequest":
        return _say(
            "Welcome to Foul Mouth. Say 'swear at me' and I'll let one rip.",
            reprompt="Say 'swear at me' or 'help'.",
        )

    if rtype == "SessionEndedRequest":
        return _say("", end=True)

    if rtype == "IntentRequest":
        intent_name = request.get("intent", {}).get("name", "")

        if intent_name == "SwearIntent":
            return _say(random.choice(SWEARS), reprompt="Want another?")

        if intent_name == "AMAZON.HelpIntent":
            return _say(
                "I tell off-color jokes. Say 'swear at me' for a one-liner, or "
                "say 'stop' to quit.",
                reprompt="Say 'swear at me' or 'stop'.",
            )

        if intent_name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
            return _say("Later.", end=True)

        if intent_name == "AMAZON.NavigateHomeIntent":
            return _say("Going home.", end=True)

        if intent_name == "AMAZON.FallbackIntent":
            return _say(
                "I didn't catch that. Say 'swear at me' or 'help'.",
                reprompt="Say 'swear at me' or 'help'.",
            )

    # Unknown request type — return a valid envelope so the simulator does not stall.
    return _say("Something went sideways. Try again.", end=True)
