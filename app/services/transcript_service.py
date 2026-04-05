import re
import yt_dlp
import requests


def extract_video_id(url: str) -> str:
    """
    Extract video ID from different YouTube URL formats
    """
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?&]+)",
        r"embed/([^?&]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def clean_subtitle_text(text: str) -> str:
    """
    Clean subtitle XML/VTT text into readable format
    """
    # Remove XML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Remove timestamps
    text = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> .*", "", text)

    # Remove extra spaces/newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_transcript_from_url(url: str) -> dict:
    """
    Fetch transcript using yt-dlp (works in production)

    Returns:
        dict: {video_id, language, transcript} OR {error}
    """

    try:
        video_id = extract_video_id(url)

        if not video_id:
            return {"error": "Invalid YouTube URL"}

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            subtitles = info.get("subtitles") or info.get("automatic_captions")

            if not subtitles:
                return {"error": "No subtitles available for this video"}

            # Prefer English if available
            if "en" in subtitles:
                lang = "en"
            else:
                lang = list(subtitles.keys())[0]

            subtitle_url = subtitles[lang][0].get("url")

            if not subtitle_url:
                return {"error": "Subtitle URL not found"}

            # Fetch subtitle content
            res = requests.get(subtitle_url)

            if res.status_code != 200:
                return {"error": "Failed to download subtitles"}

            raw_text = res.text

            # Clean text
            clean_text = clean_subtitle_text(raw_text)

            return {
                "video_id": video_id,
                "language": lang,
                "transcript": clean_text
            }

    except Exception as e:
        return {"error": f"Transcript fetch failed: {str(e)}"}


def get_video_title(url: str) -> str:
    """
    Fetch video title using yt-dlp
    """
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("title", "")

    except Exception:
        return ""