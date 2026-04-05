from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def split_text(text: str, chunk_size: int = 3000) -> list:
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def call_llm(prompt: str, max_tokens=300):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You summarize YouTube videos clearly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Groq Error: {str(e)}"


def summarize_chunk(text: str, title: str) -> str:
    prompt = f"""
Summarize this transcript chunk:
- 4-5 sentences
- Keep key information only

video_title: {title}
{text}
"""
    return call_llm(prompt)


def summarize_long_text(text: str, title: str) -> str:
    chunks = split_text(text)
    summaries = [summarize_chunk(chunk, title) for chunk in chunks]

    combined = " ".join(summaries)

    final_prompt = f"""
Combine these into one clear summary:

{combined}
"""
    return call_llm(final_prompt)


def summarize_structured(text: str, language: str = None) -> str:
    lang_note = ""
    if language and language != "en":
        lang_note = f"The transcript is in {language}. Translate to English first."

    prompt = f"""
{lang_note}

Summarize this YouTube video into:

1. Short Summary (3-4 lines)
2. Key Points (bullet points)
3. Important Insights

{text}
"""

    return call_llm(prompt, max_tokens=500)