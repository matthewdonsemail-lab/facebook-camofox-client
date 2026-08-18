"""Messenger action contracts."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Message(BaseModel):
    message_id: str | None = None
    text: str
    direction: str
    sender_name: str | None = None


class Thread(BaseModel):
    thread_id: str
    name: str
    preview: str = ""


class SendMessageInput(BaseModel):
    thread_id: str | None = None
    thread_name: str | None = None
    text: str = Field(min_length=1)


class SendMessageOutput(BaseModel):
    sent: bool
    thread_id: str | None = None
    error: str | None = None
