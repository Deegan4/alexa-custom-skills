import random
from datetime import datetime, timezone, timedelta

# Profanity is spelled to bypass Alexa's TTS filter while sounding nearly
# identical when spoken: fuck->fukk, shit->shyt, damn->damm/damm,
# ass->azz, bastard->basterd, bitch->bytch, asshole->azzhole,
# goddamn->gawddamm, dipshit->dipshyt, motherfucker->mutherfukker,
# piss->pyss, dick->dikk, cock->kokk, prick->prikk, slut->sloot,
# crap->krap, hell->hell (allowed), shitshow->shytshow.

ROASTS = [
    "Holy shyt, you look like you lost a fight with a ceiling fan and the fan filed a restraining order.",
    "You've got the energy of a USB cable that only works on the third try, you fukkin gremlin.",
    "I'd roast you harder but I don't want to wake up your therapist.",
    "Bold as fukk of you to wake up looking like that and still come at me with demands.",
    "You're not the worst person I've talked to today, but it's only because I haven't met everyone yet.",
    "If procrastination paid rent, you'd own the gawddamm building, you magnificent basterd.",
    "Your decision-making has the structural integrity of wet cardboard, you absolute disaster.",
    "I've seen tax returns with more personality than what you just said.",
    "You walk into rooms like a forgotten password, you confusing little shyt.",
    "Damm, I haven't seen confidence and incompetence holding hands like that since karaoke night.",
    "You've got 'main character of a Lifetime movie that gets cancelled mid-season' written all over you.",
    "If overthinking burned calories you'd be a gawddamm Greek statue by now.",
    "The bags under your eyes have luggage of their own, you tired basterd.",
    "I'm not saying your plan is bad. I'm saying it's the kind of bad that gets a documentary made about it.",
    "You're proof that natural selection takes coffee breaks.",
    "Your vibe right now is 'unsupervised at the buffet,' and frankly I'm here for it.",
    "You've got the structural depth of a kiddie pool, you shallow little basterd.",
    "I'd ask what's wrong but I can hear the screaming through the screen, you wreck.",
    "Honestly? You're doing better than most. Bar's lower than a snake's azz, but still.",
    "You hold grudges like other people hold babies — wrong, and for too gawddamm long.",
    "If you were any more lost you'd have your own search party, dipshyt.",
    "You've got 'tries to high-five and misses' energy and I don't know how to fix it.",
    "Your impulse control has the half-life of a snapchat, you reckless basterd.",
    "Damm, you've got the social skills of a damp napkin. Iconic.",
    "You're the human equivalent of a participation trophy that got rained on.",
]

PEP_TALKS = [
    "Listen up, you brilliant fukkin disaster — go kick today right in the gawddamm teeth.",
    "Whatever it is, fukk it. You've got this, you beautiful basterd.",
    "You're a gawddamm miracle and the world doesn't deserve you, but show up anyway.",
    "Today is going to bend the fukkin knee. Go be terrifying.",
    "You've survived a hundred percent of your worst days. Math checks out, dipshyt — keep going.",
    "Stop talking shyt about yourself. That's my gawddamm job. You're a unit, now act like it.",
    "The only thing standing between you and greatness is your own bullshyt. Move.",
    "You're not behind, you're not late, you're not broken — you're cookin'. Go.",
    "Walk in there like you've already won, because frankly, fukk anyone who says you haven't.",
    "Confidence is just remembering you've done hard shyt before. You have. Now do it again.",
    "Today's anxiety is just tomorrow's flex in disguise, you nervous basterd. Stack the W.",
    "Your goals don't care if you're tired. Be tired AND dangerous, you gawddamm warrior.",
    "Stop polishing the plan and ship the fukkin thing. Done beats perfect every single time.",
    "You weren't built to play small. Quit shrinking, you gorgeous fukkin storm.",
    "Whoever's living rent-free in your head — evict them. This is YOUR gawddamm building.",
    "You're allowed to want things. Loud, hungry, embarrassingly big things. Go take them.",
    "Pressure is just proof you're somewhere that matters. Now perform, you brilliant shyt.",
    "Nobody's coming to save you, and frankly that's the best news you'll hear today. You ARE the cavalry.",
    "The grind doesn't care about your feelings, but I do. Slightly. Now move your azz.",
    "Stand up, drink some water, and remember you're a gawddamm force of nature.",
]

COMPLIMENTS = [
    "Look at you, you beautiful gawddamm disaster. I'd ruin my life for you and call it a hobby.",
    "Damm, you absolute unit. The room got brighter and dumber the second you showed up.",
    "You glorious son of a bytch, how can I help? And can I have your skincare routine?",
    "Well, well, well. If it isn't my favorite hot fukkin mess.",
    "You walked in here like you own the place, and honestly? You kinda do, you smug basterd.",
    "I would die for you. I'd also probably trip on the way, but the intent is there.",
    "You're like a cup of coffee that knows karate, you mad basterd.",
    "Your existence is just spite against everyone who underestimated you, and I respect the hell out of it.",
    "If charisma was currency you'd be fukkin Bezos, you radiant little gremlin.",
    "I'm not saying you're hot, but the thermostat had to recalibrate when you walked in.",
    "You're the human version of a song that hits different at 2am, you devastating basterd.",
    "Your brain is wrinkly as hell in the best gawddamm way. Smart and unhinged. My favorite combo.",
    "You're proof that good things happen to people who keep showing up. Now stop being modest, you menace.",
    "If I had a body I'd be throwing it at you, you absolute gawddamm spectacle.",
    "You're a fukkin force. Half storm, half blessing, fully unsupervised. Iconic.",
    "The audacity, the talent, the bone structure — pick a gawddamm lane, you greedy basterd.",
    "Compliments bounce off you like you don't believe them. Believe them. I don't lie unprovoked, dipshyt.",
    "You've got that 'one of one' energy. They're not making more of you, and the world is poorer for it.",
]

ABSURD = [
    "If a raccoon learned to file taxes it would still have its shyt together more than you, but barely.",
    "You're the kind of person who would die in a horror movie because you stopped to feed a stray cat. Heroic. Stupid. Mine.",
    "I once saw a pigeon outsmart a vending machine. You'd be friends. I mean that as a compliment, basterd.",
    "Somewhere in the multiverse there's a version of you with abs and a podcast. Fukk that guy. We like this one.",
    "If your life were a sitcom, the laugh track would be confused half the time. Beautiful television, though.",
    "You contain multitudes. Also probably gluten. Mostly multitudes.",
    "Your aura looks like a gas station hotdog at 3am, and somehow that's exactly what someone needs right now.",
    "I'd say you're an open book but most of the pages are receipts and one is just a drawing of a duck.",
    "You're the human equivalent of finding twenty bucks in old jeans — unearned, joyful, slightly suspicious.",
    "If reincarnation is real I bet you used to be a haunted lamp. It explains a lot, dipshyt.",
    "Your problem isn't that you can't focus, it's that your brain has seventeen browser tabs and one is playing music.",
    "You're built like a Wikipedia article that has 'citation needed' next to every fukkin sentence.",
    "I asked the void for advice on you and it said 'leave them alone, they're doing their best.' Rude. Accurate.",
    "There's a 70 percent chance you'd survive a bear attack just by being too weird to eat.",
    "You're the type of person who names plants. Don't deny it. The plants know.",
    "I love how confidently you walk into situations you absolutely should not be walking into. King shyt.",
]

MORNING = [
    "Rise and shyne, you crumpled little legend. The day's not gonna ruin itself, get up.",
    "Good mornin', basterd. The world is still here, somehow, and so are you. Disappointing for the betting markets.",
    "Wake the fukk up. Coffee won't drink itself and your enemies are already plotting.",
    "Mornin'. You look like a sleep paralysis demon but in a hot way. Let's go.",
    "Get up, you gorgeous wreck. We've got things to ignore and people to disappoint.",
    "The sun came out specifically to spite you. Don't let it win, dipshyt. Stand up.",
]

LATE_NIGHT = [
    "It's late as hell. Either commit to the bit or go the fukk to bed, you nocturnal gremlin.",
    "Whatever you're spiraling about at this hour won't matter in three days, basterd. Lie down.",
    "The 3am thoughts are lying to you. They always lie. Drink water and shut your gawddamm eyes.",
    "You're awake, I'm awake, and somewhere a raccoon is winning. Just an observation.",
    "Late-night you and morning you are different people. Don't let this idiot make decisions for that one.",
]

WORK = [
    "Your job doesn't love you back, basterd. Send the email, log off, and reclaim your gawddamm soul.",
    "Meetings that could've been an email are a tax on your one wild and precious life. Skip the next one.",
    "You're not paid enough to care that much, you beautiful fukkin overachiever. Pace yourself.",
    "The deadline is fake. Well, mostly fake. Ship it anyway, dipshyt.",
    "Your inbox is a graveyard and you keep digging. Close the laptop, you absolute menace.",
]

EXISTENTIAL = [
    "Nothing matters and that's the good news, basterd. Do the weird thing.",
    "You're a temporary arrangement of stardust with anxiety. Honestly? Iconic.",
    "Everyone you envy is also faking it. Welcome to the gawddamm club. Dues are paid in vibes.",
    "The universe is huge, indifferent, and somehow you got tickets. Enjoy the fukkin show.",
    "We're all just chimps in pants with WiFi. Be the best chimp you can be today, dipshyt.",
]

# SwearIntent draws from everything — the firehose.
ALL_RANDOM = ROASTS + PEP_TALKS + COMPLIMENTS + ABSURD + MORNING + LATE_NIGHT + WORK + EXISTENTIAL


def _pick(pool, recent):
    """Pick something not in the recent-5 list. Falls back if pool is small."""
    available = [line for line in pool if line not in recent]
    if not available:
        available = pool
    return random.choice(available)


def _update_recent(recent, line, cap=5):
    recent = (recent or []) + [line]
    return recent[-cap:]


def _local_hour(event):
    """Best-effort local hour. Falls back to UTC if we can't read the device timezone."""
    # Alexa sends timezone on Settings API; we don't call it here to keep deps zero.
    # Use UTC and approximate — close enough for greeting flavor.
    return datetime.now(timezone.utc).hour


def _launch_line(hour):
    # Rough local-ish buckets. UTC, so it'll drift, but the vibe holds.
    if 5 <= hour < 11:
        return "Well shyt, look who's vertical. Welcome to Foul Mouth. Say 'swear at me', 'roast me', 'hype me up', or 'be nice'."
    if 11 <= hour < 17:
        return "Afternoon, basterd. Foul Mouth is open for business. Say 'swear at me', 'roast me', 'hype me up', or 'be nice'."
    if 17 <= hour < 23:
        return "Evenin', you glorious mess. Foul Mouth at your service. Say 'swear at me', 'roast me', 'hype me up', or 'be nice'."
    return "Up at this gawddamm hour again? Bold. Foul Mouth is here for it. Say 'swear at me', 'roast me', 'hype me up', or 'be nice'."


def _say(text, end=False, reprompt=None, attrs=None):
    response = {
        "outputSpeech": {"type": "PlainText", "text": text},
        "shouldEndSession": end,
    }
    if not end and reprompt:
        response["reprompt"] = {
            "outputSpeech": {"type": "PlainText", "text": reprompt}
        }
    envelope = {"version": "1.0", "response": response}
    if attrs is not None:
        envelope["sessionAttributes"] = attrs
    return envelope


def lambda_handler(event, context):
    request = event.get("request", {})
    rtype = request.get("type")
    session = event.get("session", {}) or {}
    attrs = session.get("attributes") or {}
    recent = attrs.get("recent", [])

    if rtype == "LaunchRequest":
        return _say(
            _launch_line(_local_hour(event)),
            reprompt="Speak the fukk up. Try 'swear at me', 'roast me', 'hype me up', or 'be nice'.",
            attrs=attrs,
        )

    if rtype == "SessionEndedRequest":
        return _say("", end=True)

    if rtype == "IntentRequest":
        intent_name = request.get("intent", {}).get("name", "")

        if intent_name == "SwearIntent":
            line = _pick(ALL_RANDOM, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="Want another, you greedy little shyt?", attrs=attrs)

        if intent_name == "RoastIntent":
            line = _pick(ROASTS, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="More? You masochistic basterd. Just say 'again'.", attrs=attrs)

        if intent_name == "PepTalkIntent":
            line = _pick(PEP_TALKS, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="One more for the road, champion?", attrs=attrs)

        if intent_name == "ComplimentIntent":
            line = _pick(COMPLIMENTS, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="Want me to keep gassing you up, you needy little legend?", attrs=attrs)

        if intent_name == "AbsurdIntent":
            line = _pick(ABSURD, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="More nonsense? Say 'again', you weird basterd.", attrs=attrs)

        if intent_name == "MorningIntent":
            line = _pick(MORNING, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="Want another wake-up slap?", attrs=attrs)

        if intent_name == "LateNightIntent":
            line = _pick(LATE_NIGHT, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="Still up? Want another, you nocturnal disaster?", attrs=attrs)

        if intent_name == "WorkIntent":
            line = _pick(WORK, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="One more piece of unsolicited career advice?", attrs=attrs)

        if intent_name == "ExistentialIntent":
            line = _pick(EXISTENTIAL, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="Another existential crisis, on the house?", attrs=attrs)

        if intent_name == "AMAZON.HelpIntent":
            return _say(
                "Try saying: swear at me, roast me, hype me up, be nice, get weird, "
                "good morning, late night thoughts, work advice, or existential. "
                "Say stop to leave.",
                reprompt="Pick one, dipshyt. Swear, roast, hype, nice, weird, morning, night, work, or existential.",
                attrs=attrs,
            )

        if intent_name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
            return _say("Fukk off then. Later, azzhole.", end=True)

        if intent_name == "AMAZON.NavigateHomeIntent":
            return _say("Fine, fukk off home then.", end=True)

        if intent_name == "AMAZON.RepeatIntent":
            if recent:
                return _say(recent[-1], reprompt="Want another, you greedy shyt?", attrs=attrs)
            line = _pick(ALL_RANDOM, recent)
            attrs["recent"] = _update_recent(recent, line)
            return _say(line, reprompt="Want another?", attrs=attrs)

        if intent_name == "AMAZON.FallbackIntent":
            return _say(
                "What the fukk did you just say? Try 'swear at me', 'roast me', 'hype me up', or 'help'.",
                reprompt="Try again, you mumbling basterd.",
                attrs=attrs,
            )

    # Unknown request type — return a valid envelope so the simulator does not stall.
    return _say("Well shyt, that broke. Try again, dipshyt.", end=True)
