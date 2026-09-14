"""
Data transfer objects and domain models for Instagram & Threads entities.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class UserSummary:
    pk: int
    username: str
    full_name: str = ""
    is_private: bool = False
    is_verified: bool = False
    profile_pic_url: str = ""
    follower_count: int = 0
    following_count: int = 0
    media_count: int = 0
    biography: str = ""
    external_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UserSummary:
        u = data.get("user", data)
        return cls(
            pk=int(u.get("pk", 0)),
            username=str(u.get("username", "")),
            full_name=str(u.get("full_name", "")),
            is_private=bool(u.get("is_private", False)),
            is_verified=bool(u.get("is_verified", False)),
            profile_pic_url=str(u.get("profile_pic_url", "")),
            follower_count=int(u.get("follower_count", 0)),
            following_count=int(u.get("following_count", 0)),
            media_count=int(u.get("media_count", 0)),
            biography=str(u.get("biography", "")),
            external_url=u.get("external_url"),
        )

@dataclass
class MediaItem:
    pk: int
    id: str
    code: str
    media_type: int
    caption: str = ""
    like_count: int = 0
    comment_count: int = 0
    taken_at: int = 0
    user: Optional[UserSummary] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MediaItem:
        user_data = data.get("user")
        user = UserSummary.from_dict(user_data) if user_data else None
        caption_dict = data.get("caption") or {}
        caption_text = caption_dict.get("text", "") if isinstance(caption_dict, dict) else str(caption_dict)
        return cls(
            pk=int(data.get("pk", 0)),
            id=str(data.get("id", "")),
            code=str(data.get("code", "")),
            media_type=int(data.get("media_type", 1)),
            caption=caption_text,
            like_count=int(data.get("like_count", 0)),
            comment_count=int(data.get("comment_count", 0)),
            taken_at=int(data.get("taken_at", 0)),
            user=user,
        )

@dataclass
class CommentItem:
    pk: int
    text: str
    created_at: int
    like_count: int = 0
    user: Optional[UserSummary] = None
    child_comment_count: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CommentItem:
        user_data = data.get("user")
        user = UserSummary.from_dict(user_data) if user_data else None
        return cls(
            pk=int(data.get("pk", 0)),
            text=str(data.get("text", "")),
            created_at=int(data.get("created_at", 0)),
            like_count=int(data.get("comment_like_count", 0)),
            user=user,
            child_comment_count=int(data.get("child_comment_count", 0)),
        )

@dataclass
class DirectThread:
    thread_id: str
    thread_title: str
    users: List[UserSummary] = field(default_factory=list)
    is_group: bool = False
    last_activity_at: int = 0
    unread_count: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DirectThread:
        users = [UserSummary.from_dict(u) for u in data.get("users", [])]
        return cls(
            thread_id=str(data.get("thread_id", "")),
            thread_title=str(data.get("thread_title", "")),
            users=users,
            is_group=bool(data.get("is_group", False)),
            last_activity_at=int(data.get("last_activity_at", 0)),
            unread_count=int(data.get("unread_count", 0)),
        )

@dataclass
class StoryItem:
    pk: int
    id: str
    taken_at: int
    expiring_at: int
    media_type: int
    user: Optional[UserSummary] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StoryItem:
        user_data = data.get("user")
        user = UserSummary.from_dict(user_data) if user_data else None
        return cls(
            pk=int(data.get("pk", 0)),
            id=str(data.get("id", "")),
            taken_at=int(data.get("taken_at", 0)),
            expiring_at=int(data.get("expiring_at", 0)),
            media_type=int(data.get("media_type", 1)),
            user=user,
        )
