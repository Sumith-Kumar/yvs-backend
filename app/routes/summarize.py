from flask import Blueprint, request, jsonify
from app.services.transcript_service import get_transcript_from_url, get_video_title
from app.services.summarizer_service import summarize_long_text

summarize_bp = Blueprint("summarize", __name__)

@summarize_bp.route("/summarize", methods=["POST"])
def summarize():
    url = request.json.get("url")

    transcript_data = get_transcript_from_url(url)
    video_title = get_video_title(url)

    if "error" in transcript_data:
        return jsonify(transcript_data)

    summary = summarize_long_text(transcript_data["transcript"], video_title)

    return jsonify({
        "summary": summary,
        "language": transcript_data.get("language"),
        "transcript": transcript_data.get("transcript")  # ✅ added
    })