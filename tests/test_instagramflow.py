import pytest
from unittest.mock import MagicMock
from instagramflow.client import InstagramAPI
from instagramflow.modules.comment import CommentModule
from instagramflow.modules.story import StoryModule
from instagramflow.modules.note import NoteModule
from instagramflow.modules.media import MediaModule
from instagramflow.devices import get_device, list_presets, DEVICE_CATALOG
from instagramflow.session import SessionStorage
from instagramflow.types import UserSummary, MediaItem, CommentItem
from instagramflow.modules.friendship import FriendshipModule

def test_comment_module_methods():
    client = MagicMock()
    client._get.return_value = {"status": "ok", "comments": []}
    client._post.return_value = {"status": "ok"}
    
    comm = CommentModule(client)
    
    # list comments
    res = comm.list("123456")
    client._get.assert_called_with("/api/v1/media/123456/comments/", params=None)
    
    # replies
    comm.replies("123456", "987654")
    client._get.assert_called_with("/api/v1/media/123456/comments/987654/child_comments/", params=None)
    
    # add comment
    comm.add("123456", "Great post!", replied_to_comment_id="987654")
    client._post.assert_called_with(
        "/api/v1/media/123456/comment/",
        data={"comment_text": "Great post!", "replied_to_comment_id": "987654"}
    )
    
    # like & unlike
    comm.like("987654")
    client._post.assert_called_with("/api/v1/media/987654/comment_like/")
    
    comm.unlike("987654")
    client._post.assert_called_with("/api/v1/media/987654/comment_unlike/")
    
    # pin & unpin
    comm.pin("123456", "987654")
    client._post.assert_called_with("/api/v1/media/123456/comment/987654/pin/")
    
    comm.unpin("123456", "987654")
    client._post.assert_called_with("/api/v1/media/123456/comment/987654/unpin/")
    
    # delete
    comm.delete("123456", "987654")
    client._post.assert_called_with("/api/v1/media/123456/comment/987654/delete/")

def test_story_module_methods():
    client = MagicMock()
    client._get.return_value = {"status": "ok", "tray": []}
    client._post.return_value = {"status": "ok"}
    
    story = StoryModule(client)
    
    # user stories
    story.user_stories("112233")
    client._get.assert_called_with("/api/v1/feed/reels_media/", params={"reel_ids": "112233"})
    
    # highlights
    story.highlights("112233")
    client._get.assert_called_with("/api/v1/highlights/112233/highlights_tray/")
    
    # seen
    story.seen("story_7788", taken_at=1700000000)
    args, kwargs = client._post.call_args
    assert args[0] == "/api/v2/media/seen/"
    assert "story_7788" in kwargs["data"]["reels"]
    
    # like & unlike
    story.like("7788")
    client._post.assert_called_with("/api/v1/media/7788/like/", data={"media_id": "7788"})
    
    story.unlike("7788")
    client._post.assert_called_with("/api/v1/media/7788/unlike/", data={"media_id": "7788"})

def test_note_module_methods():
    client = MagicMock()
    client._get.return_value = {"status": "ok", "items": []}
    client._post.return_value = {"status": "ok"}
    
    note = NoteModule(client)
    
    # get notes
    note.get_notes()
    client._get.assert_called_with("/api/v1/notes/get_notes/")
    
    # create note
    note.create("Building headless IG SDK", audience=0)
    client._post.assert_called_with(
        "/api/v1/notes/create_note/",
        data={"text": "Building headless IG SDK", "audience": "0"}
    )
    
    # delete note
    note.delete("554433")
    client._post.assert_called_with("/api/v1/notes/delete_note/", data={"id": "554433"})

def test_media_extensions():
    client = MagicMock()
    client._get.return_value = {"status": "ok"}
    client._post.return_value = {"status": "ok"}
    
    media = MediaModule(client)
    
    # shortcode conversions
    code = "CGgDsi7JQdS"
    pk = media.pk_from_code(code)
    assert pk > 0
    assert media.code_from_pk(pk) == code
    
    # info
    media.info("12345")
    client._get.assert_called_with("/api/v1/media/12345/info/")
    
    # likers
    media.likers("12345")
    client._get.assert_called_with("/api/v1/media/12345/likers/")
    
    # user clips (Reels)
    media.user_clips("998877")
    client._post.assert_called_with("/api/v1/clips/user/", data={"target_user_id": "998877", "page_size": "12"})
    
    # save & unsave
    media.save("12345", collection_id="coll_1")
    client._post.assert_called_with("/api/v1/media/12345/save/", data={"added_collection_ids": "[coll_1]"})
    
    media.unsave("12345")
    client._post.assert_called_with("/api/v1/media/12345/unsave/")
    
    # archive & unarchive
    media.archive("12345")
    client._post.assert_called_with("/api/v1/media/12345/only_me/", data={"media_id": "12345"})
    
    media.unarchive("12345")
    client._post.assert_called_with("/api/v1/media/12345/undo_only_me/", data={"media_id": "12345"})

def test_devices_catalog():
    presets = list_presets()
    assert "iphone_15_pro" in presets
    assert "pixel_8_pro" in presets
    
    dev = get_device("iphone_15_pro")
    assert dev.model == "iPhone 15 Pro"
    assert dev.platform == "iOS"
    assert dev.capabilities == "3brTv10="

def test_session_storage(tmp_path):
    session = SessionStorage(session_token="test_tok_123", device_preset="iphone_15_pro")
    session.user_id = "998877"
    session.cookies = {"sessionid": "sess_abc"}
    
    filepath = str(tmp_path / "session.json")
    session.save_to_file(filepath)
    
    loaded = SessionStorage.load_from_file(filepath)
    assert loaded.session_token == "test_tok_123"
    assert loaded.user_id == "998877"
    assert loaded.cookies.get("sessionid") == "sess_abc"

def test_domain_types():
    user = UserSummary.from_dict({"user": {"pk": "123", "username": "alice", "is_verified": True}})
    assert user.pk == 123
    assert user.username == "alice"
    assert user.is_verified is True
    
    media = MediaItem.from_dict({"pk": 456, "id": "456_123", "code": "CGgDsi7JQdS", "caption": {"text": "Hello world"}})
    assert media.pk == 456
    assert media.code == "CGgDsi7JQdS"
    assert media.caption == "Hello world"

def test_close_friends_besties():
    client = MagicMock()
    client._post.return_value = {"status": "ok"}
    
    fr = FriendshipModule(client)
    fr.close_friend_add(123456)
    client._post.assert_called_with(
        "/api/v1/friendships/set_besties/",
        data={
            "source": "audience_manager",
            "module": "favorites_home_list",
            "add": "[123456]",
            "remove": "[]"
        }
    )
    
    fr.close_friend_remove(123456)
    client._post.assert_called_with(
        "/api/v1/friendships/set_besties/",
        data={
            "source": "audience_manager",
            "module": "favorites_home_list",
            "add": "[]",
            "remove": "[123456]"
        }
    )

def test_media_and_story_download_links():
    client = MagicMock()
    client._get.return_value = {
        "items": [{
            "pk": 111,
            "media_type": 2,
            "video_versions": [{"url": "https://cdn.example.com/video.mp4"}]
        }]
    }
    
    media = MediaModule(client)
    dl = media.download(111)
    assert dl["url"] == "https://cdn.example.com/video.mp4"
    assert dl["media_type"] == "video"
    assert dl["ext"] == "mp4"
    
    story = StoryModule(client)
    story_dl = story.download(111)
    assert story_dl["url"] == "https://cdn.example.com/video.mp4"
    assert story_dl["ext"] == "mp4"
