"""
Keyless fallback for YouTube data using yt-dlp (no API key, no quota).

Used automatically by fetch_channel_data.py and search_competitor_videos.py
when no YOUTUBE_API_KEY is configured. Output mirrors the Data API scripts.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

try:
    import yt_dlp
except ImportError:  # pragma: no cover
    yt_dlp = None

BASE_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "ignore_no_formats_error": True,
    "noprogress": True,
}


def available():
    return yt_dlp is not None


def _extract(url, flat=False, end=None):
    opts = dict(BASE_OPTS)
    if flat:
        opts["extract_flat"] = "in_playlist"
    if end:
        opts["playlistend"] = end
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def _iso_date(d):
    return f"{d[:4]}-{d[4:6]}-{d[6:8]}T00:00:00Z" if d and len(d) == 8 else None


def _iso_duration(sec):
    if not sec:
        return None
    sec = int(sec)
    h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
    return "PT" + (f"{h}H" if h else "") + (f"{m}M" if m else "") + f"{s}S"


def video_details(video_id):
    try:
        v = _extract(f"https://www.youtube.com/watch?v={video_id}")
    except Exception as e:
        return {"video_id": video_id, "error": str(e)[:200]}
    views = v.get("view_count") or 0
    likes = v.get("like_count") or 0
    comments = v.get("comment_count") or 0
    return {
        "video_id": video_id,
        "title": v.get("title"),
        "channel_title": v.get("channel"),
        "channel_id": v.get("channel_id"),
        "published_at": _iso_date(v.get("upload_date")),
        "description": (v.get("description") or "")[:200],
        "duration": _iso_duration(v.get("duration")),
        "views": views,
        "likes": likes,
        "comments": comments,
        "engagement_rate_pct": round((likes + comments) / views * 100, 2) if views else 0,
        "tags": (v.get("tags") or [])[:30],
        "thumbnail": v.get("thumbnail"),
    }


def _details_many(ids):
    with ThreadPoolExecutor(max_workers=5) as pool:
        return list(pool.map(video_details, ids))


def channel_url(raw):
    raw = raw.strip()
    if raw.startswith("http"):
        url = raw.rstrip("/")
        for suffix in ("/videos", "/shorts", "/streams", "/featured", "/about"):
            if url.endswith(suffix):
                url = url[: -len(suffix)]
        return url
    if raw.startswith("@"):
        return f"https://www.youtube.com/{raw}"
    if raw.startswith("UC") and len(raw) == 24:
        return f"https://www.youtube.com/channel/{raw}"
    return f"https://www.youtube.com/@{raw}"


def fetch_channel(raw, max_videos=10):
    base = channel_url(raw)
    info = _extract(base + "/videos", flat=True, end=max_videos)
    ids = [e["id"] for e in (info.get("entries") or []) if e.get("id")][:max_videos]
    videos = _details_many(ids)
    channel = {
        "channel_id": info.get("channel_id") or info.get("id"),
        "title": info.get("channel") or info.get("title"),
        "description": (info.get("description") or "")[:500],
        "custom_url": info.get("uploader_id"),
        "published_at": None,
        "country": None,
        "subscriber_count": info.get("channel_follower_count") or 0,
        "total_views": None,
        "video_count": None,
        "uploads_playlist": None,
        "keywords": ", ".join(info.get("tags") or []),
    }
    return {
        "channel": channel,
        "videos": videos,
        "fetched_at": datetime.now().isoformat(),
        "quota_consumed": 0,
        "source": "yt-dlp (keyless fallback; total_views/video_count unavailable)",
    }


def search(query, channel_id=None, max_results=10, order="relevance", days=None):
    n = min(max_results, 50)
    if channel_id and not query:
        info = _extract(channel_url(channel_id) + "/videos", flat=True, end=n)
    elif channel_id:
        info = _extract(channel_url(channel_id) + "/search?query=" + query, flat=True, end=n)
    else:
        prefix = "ytsearchdate" if order == "date" else "ytsearch"
        info = _extract(f"{prefix}{n}:{query}", flat=True)
    ids = [e["id"] for e in (info.get("entries") or []) if e.get("id")][:n]
    videos = [v for v in _details_many(ids) if "error" not in v]
    if days:
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
        videos = [v for v in videos if (v.get("published_at") or "") >= cutoff]
    return videos
