# Design: Code Interpreter

**Project:** `code-interpreter`  
**Parent system design:** [07 — Agent Runtime with Hard Containment](../07-agent-runtime-containment.md)

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

> **Watch on YouTube:** [Code Interpreter — System Design #Shorts](https://youtu.be/AzS0gaU1PvU)
>
> Direct link: **https://youtu.be/AzS0gaU1PvU**

Also available in-repo:
- GIF preview: [`video/design-overview.gif`](./video/design-overview.gif)
- MP4 download: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Narration script: [`video/narration.txt`](./video/narration.txt)

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

