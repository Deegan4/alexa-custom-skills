import random

# Common profanity misspellings that bypass Alexa's TTS filter while
# sounding nearly identical when spoken: fuck->fukk, shit->shyt,
# damn->damm, ass->azz, bastard->basterd, bitch->bytch, asshole->azzhole,
# goddamn->gawddamm, dipshit->dipshyt.
SWEARS = [
    # original three (rewritten)
    "Fukk yeah, what the hell do you want, you magnificent basterd?",
    "Shyt, you're looking fine today.",
    "What the actual fukk is up?",
    # insulting compliments
    "Look at you, you beautiful gawddamm disaster.",
    "Damm, you absolute unit. What's the fukkin move?",
    "You glorious son of a bytch, how can I help?",
    "Well, well, well. If it isn't my favorite hot fukkin mess.",
    "You walked in here like you own the place. I respect the hell out of that.",
    # roasts
    "I'd ask how you're doing, but holy shyt, I can see it on your face. Rough.",
    "Bold as fukk of you to talk to me looking like that.",
    "You've got the energy of a half-charged AirPod today, you fukkin gremlin.",
    "I'm not saying you look tired, but the bags under your gawddamm eyes have luggage of their own.",
    # pep talks
    "Listen up, you brilliant fukkin disaster — go kick today in the teeth.",
    "Whatever it is, fukk it. You've got this.",
    "You're a gawddamm miracle and the world doesn't deserve you.",
    "Today is going to bend the fukkin knee. Go be terrifying.",
    # absurd
    "I would die for you. I'd also probably trip and fall on my azz on the way, but the intent is there.",
    "You're like a cup of coffee that knows karate, you mad basterd.",
    "If overthinking burned calories you'd be a Greek gawddamm statue by now.",
    "Honestly? You're doing better than most. Bar's lower than a snake's azz, but still.",
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
            "Well shyt, look who showed up. Welcome to Foul Mouth, you beautiful basterd. Say 'swear at me' and I'll let one rip.",
            reprompt="Speak the fukk up. Say 'swear at me' or 'help'.",
        )

    if rtype == "SessionEndedRequest":
        return _say("", end=True)

    if rtype == "IntentRequest":
        intent_name = request.get("intent", {}).get("name", "")

        if intent_name == "SwearIntent":
            return _say(random.choice(SWEARS), reprompt="Want another, you greedy little shyt?")

        if intent_name == "AMAZON.HelpIntent":
            return _say(
                "Christ on a cracker, what do you need? Say 'swear at me' for a "
                "gawddamm one-liner, or 'stop' to fukk off.",
                reprompt="Say 'swear at me' or get the hell out.",
            )

        if intent_name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
            return _say("Fukk off then. Later, azzhole.", end=True)

        if intent_name == "AMAZON.NavigateHomeIntent":
            return _say("Fine, fukk off home then.", end=True)

        if intent_name == "AMAZON.FallbackIntent":
            return _say(
                "What the fukk did you just say? Say 'swear at me' or 'help', dipshyt.",
                reprompt="Try again, you mumbling basterd.",
            )

    # Unknown request type — return a valid envelope so the simulator does not stall.
    return _say("Well shyt, that broke. Try again, dipshyt.", end=True)
