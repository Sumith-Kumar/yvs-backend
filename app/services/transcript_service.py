from youtube_transcript_api import YouTubeTranscriptApi
import re
import yt_dlp

def extract_video_id(url: str) -> str:
    """
    Extract video ID from different YouTube URL formats
    """
    patterns = [
        r"v=([^&]+)",           # youtube.com/watch?v=ID
        r"youtu\.be/([^?&]+)",  # youtu.be/ID
        r"embed/([^?&]+)"       # youtube.com/embed/ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_transcript_from_url(url: str, preferred_languages=None) -> dict:
    """
    Fetch transcript from YouTube URL

    Args:
        url (str): YouTube video URL
        preferred_languages (list): Optional language preference (default ['en'])

    Returns:
        dict: {video_id, language, transcript} OR {error}
    """

    if preferred_languages is None:
        preferred_languages = ['en']

    try:
        video_id = extract_video_id(url)

        if not video_id:
            return {"error": "Invalid YouTube URL"}

        api = YouTubeTranscriptApi()

        # Get all available transcripts
        transcript_list = api.list(video_id)

        # Try preferred languages first
        transcript = None
        try:
            transcript = transcript_list.find_transcript(preferred_languages)
        except:
            # fallback → first available transcript
            transcripts = list(transcript_list)
            if not transcripts:
                return {"error": "No transcripts available for this video"}
            transcript = transcripts[0]

        # Fetch transcript data
        data = transcript.fetch()

        # Combine into single string
        full_text = " ".join([item.text for item in data])

        return {
            "video_id": video_id,
            "language": transcript.language_code,
            "transcript": full_text
        }

    except Exception as e:
        return {"error": f"Transcript fetch failed: {str(e)}"}
    
def get_video_title(url):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("title", "")

    except Exception as e:
        return ""