---
name: alexa-response-lint
description: Reference for the Alexa Custom Skills response envelope. Use whenever editing or reviewing a Python Lambda handler under skills/*/lambda_function.py to verify the return shape is valid.
user-invocable: false
---

# alexa-response-lint

Background knowledge for editing Alexa skill Lambda handlers in this repo. Auto-apply when touching any `lambda_function.py`.

## The contract Alexa enforces

Every handler MUST return a dict matching this shape — a malformed envelope causes the Alexa simulator to silently fail with "There was a problem with the requested skill's response."

```python
{
    "version": "1.0",
    "response": {
        "outputSpeech": {"type": "PlainText", "text": "<string>"},
        "shouldEndSession": False,   # bool — keeps mic open for follow-up
    },
}
```

Optional response fields (add only when needed):
- `"reprompt": {"outputSpeech": {"type": "PlainText", "text": "..."}}` — required if `shouldEndSession` is `False` and you want a re-prompt after silence.
- `"card": {"type": "Simple", "title": "...", "content": "..."}` — visual card in the Alexa app.
- `"directives": [...]` — for audio playback, dialog control, etc.

## SSML variant

To use SSML, swap `outputSpeech`:

```python
"outputSpeech": {"type": "SSML", "ssml": "<speak>Hello <break time='200ms'/> world.</speak>"}
```

The `<speak>` wrapper is required.

## Checklist when reviewing a handler

- [ ] Top-level `version` is the string `"1.0"` (not `1.0` numeric).
- [ ] `response.outputSpeech.type` is `"PlainText"` or `"SSML"` exactly.
- [ ] `shouldEndSession` is a real `bool`, not `"false"`.
- [ ] Error/exception paths still return a valid envelope (do not return `None` or raise).
- [ ] Intent name lookup tolerates LaunchRequest / SessionEndedRequest types where `event['request']['intent']` does not exist.

## Common breakage in this repo

- `ollama-brain` uses bare `try/except` around the slot lookup AND around the HTTP call. Both fall back to a valid envelope — keep that pattern when adding new failure modes.
- Neither skill currently handles `LaunchRequest` (when the user says "Alexa, open foul mouth" with no intent). Adding one is fine but make sure the new branch returns a full envelope.

## Reference

Apple^H^H^H^H^H Amazon docs evolve; verify the latest shape with context7 if anything below looks stale:
- Response format: `Alexa Skills Kit / Custom Skill / Response Format`
- Request types: `LaunchRequest`, `IntentRequest`, `SessionEndedRequest`
