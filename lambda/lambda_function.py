import random

SWEARS = [
    # original three
    "Fuck yeah, what the hell do you want, you magnificent bastard?",
    "Shit, you're looking fine today.",
    "What the actual fuck is up?",
    # insulting compliments
    "Look at you, you beautiful disaster.",
    "Damn, you absolute unit. What's the move?",
    "You glorious son of a bitch, how can I help?",
    "Well, well, well. If it isn't my favorite hot mess.",
    "You walked in here like you own the place. I respect the hell out of that.",
    # roasts
    "I'd ask how you're doing, but I can see it on your face. Rough.",
    "Bold of you to talk to me looking like that.",
    "You've got the energy of a half-charged AirPod today.",
    "I'm not saying you look tired, but the bags under your eyes have luggage of their own.",
    # pep talks
    "Listen up, you brilliant disaster — go kick today in the teeth.",
    "Whatever it is, fuck it. You've got this.",
    "You're a goddamn miracle and the world doesn't deserve you.",
    "Today is going to bend the knee. Go be terrifying.",
    # absurd
    "I would die for you. I'd also probably trip on the way, but the intent is there.",
    "You're like a cup of coffee that knows karate.",
    "If overthinking burned calories you'd be a Greek statue by now.",
    "Honestly? You're doing better than most. Bar's low, but still.",
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
