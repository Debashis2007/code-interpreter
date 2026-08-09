# Design: Code Interpreter

**Project:** `code-interpreter`  
**Parent system design:** `07-agent-runtime-containment.md`

## 1. What this POC demonstrates

Mock sandbox: deny dangerous imports/egress patterns; allow trivial exec in constrained builtins.

## 2. Architecture (POC)

```text
POST /execute → FORBIDDEN scan → ast parse → constrained exec
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Deny-by-default capabilities | Model text must not grant host power. | `FORBIDDEN` substrings. |
| Constrained builtins | Reduce blast radius of exec. | `__builtins__` whitelist. |
| Sandbox metadata | Signals micro-VM/egress policy intent. | `egress=deny`. |

## 4. Key endpoints

`GET /health`, `POST /execute`

## 5. Tradeoffs / POC limits

Not a real micro-VM — do not run untrusted code outside lab.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

