"""Conversation history stored in TinyDB (NoSQL-style JSON).

Each record: {session_id, tenant_id, role, content, ts}. We use this to
re-hydrate the agent across turns and to power analytics.
"""
from __future__ import annotations

import time
from typing import Iterable

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from tinydb import Query, TinyDB

from app.tenancy import TenantContext


def _db(tenant: TenantContext) -> TinyDB:
    return TinyDB(tenant.conversations_db)


def append_turn(tenant: TenantContext, session_id: str, role: str, content: str) -> None:
    with _db(tenant) as db:
        db.insert(
            {
                "session_id": session_id,
                "tenant_id": tenant.tenant_id,
                "role": role,
                "content": content,
                "ts": time.time(),
            }
        )


def load_history(tenant: TenantContext, session_id: str, limit: int = 20) -> list[BaseMessage]:
    Q = Query()
    with _db(tenant) as db:
        rows = db.search(Q.session_id == session_id)
    rows.sort(key=lambda r: r["ts"])
    rows = rows[-limit:]
    return [_to_message(r) for r in rows]


def _to_message(row: dict) -> BaseMessage:
    role, content = row["role"], row["content"]
    if role == "user":
        return HumanMessage(content=content)
    if role == "assistant":
        return AIMessage(content=content)
    return SystemMessage(content=content)


def session_summary(tenant: TenantContext) -> list[dict]:
    """Aggregate sessions for analytics / debugging."""
    with _db(tenant) as db:
        rows = db.all()
    by_session: dict[str, dict] = {}
    for r in rows:
        s = by_session.setdefault(
            r["session_id"], {"session_id": r["session_id"], "turns": 0, "started_at": r["ts"]}
        )
        s["turns"] += 1
        s["last_ts"] = r["ts"]
    return list(by_session.values())
