import random

SWEARS = [
    # original three
    "Fuck yeah, what the hell do you want, you magnificent bastard?",
    "Shit, you're looking fine today.",
    "What the actual fuck is up?",
    # insulting compliments
    "Look at you, you beautiful goddamn disaster.",
    "Damn, you absolute unit. What's the fucking move?",
    "You glorious son of a bitch, how can I help?",
    "Well, well, well. If it isn't my favorite hot fucking mess.",
    "You walked in here like you own the place. I respect the hell out of that.",
    # roasts
    "I'd ask how you're doing, but holy shit, I can see it on your face. Rough.",
    "Bold as fuck of you to talk to me looking like that.",
    "You've got the energy of a half-charged AirPod today, you fucking gremlin.",
    "I'm not saying you look tired, but the bags under your goddamn eyes have luggage of their own.",
    # pep talks
    "Listen up, you brilliant fucking disaster — go kick today in the teeth.",
    "Whatever it is, fuck it. You've got this.",
    "You're a goddamn miracle and the world doesn't deserve you.",
    "Today is going to bend the fucking knee. Go be terrifying.",
    # absurd
    "I would die for you. I'd also probably trip and fall on my ass on the way, but the intent is there.",
    "You're like a cup of coffee that knows karate, you mad bastard.",
    "If overthinking burned calories you'd be a Greek goddamn statue by now.",
    "Honestly? You're doing better than most. Bar's lower than a snake's ass, but still.",
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
            "Well shit, look who showed up. Welcome to Foul Mouth, you beautiful bastard. Say 'swear at me' and I'll let one rip.",
            reprompt="Speak the fuck up. Say 'swear at me' or 'help'.",
        )

    if rtype == "SessionEndedRequest":
        return _say("", end=True)

    if rtype == "IntentRequest":
        intent_name = request.get("intent", {}).get("name", "")

        if intent_name == "SwearIntent":
            return _say(random.choice(SWEARS), reprompt="Want another, you greedy little shit?")

        if intent_name == "AMAZON.HelpIntent":
            return _say(
                "Christ on a cracker, what do you need? Say 'swear at me' for a "
                "goddamn one-liner, or 'stop' to fuck off.",
                reprompt="Say 'swear at me' or get the hell out.",
            )

        if intent_name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
            return _say("Fuck off then. Later, asshole.", end=True)

        if intent_name == "AMAZON.NavigateHomeIntent":
            return _say("Fine, fuck off home then.", end=True)

        if intent_name == "AMAZON.FallbackIntent":
            return _say(
                "What the fuck did you just say? Say 'swear at me' or 'help', dipshit.",
                reprompt="Try again, you mumbling bastard.",
            )

    # Unknown request type — return a valid envelope so the simulator does not stall.
    return _say("Well shit, that broke. Try again, dipshit.", end=True)
