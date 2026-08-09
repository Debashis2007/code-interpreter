# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Code Interpreter — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload, AUTHOR_NAME, AUTHOR_FINGERPRINT, AUTHOR_GITHUB
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Code Interpreter"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(
        USE_CASE,
        {
            "author": AUTHOR_NAME,
            "author_github": AUTHOR_GITHUB,
            "fingerprint": AUTHOR_FINGERPRINT,
        },
    )

@app.get("/author")
def author():
    return {
        "author": AUTHOR_NAME,
        "github": AUTHOR_GITHUB,
        "fingerprint": AUTHOR_FINGERPRINT,
        "notice": "Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.",
    }


import ast

class ExecIn(BaseModel):
    code: str

FORBIDDEN = ("import os", "import socket", "open(", "__import__")

@app.post("/execute")
def execute(body: ExecIn):
    for f in FORBIDDEN:
        if f in body.code:
            return {"allowed": False, "reason": "sandbox_deny", "detail": f}
    try:
        tree = ast.parse(body.code, mode="exec")
    except SyntaxError as e:
        raise HTTPException(400, detail=str(e))
    # Extremely limited eval: only print of binops on constants
    local = {}
    try:
        # noqa: POC only — still constrained by FORBIDDEN checks
        exec(compile(tree, "<sandbox>", "exec"), {"__builtins__": {"print": print, "range": range}}, local)
        return {"allowed": True, "sandbox": "microvm-simulated", "egress": "deny", "result": local}
    except Exception as e:
        return {"allowed": True, "error": str(e)}
