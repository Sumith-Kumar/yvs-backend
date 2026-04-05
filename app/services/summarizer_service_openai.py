# from openai import OpenAI
# import os

# # Initialize client safely
# def get_client():
#     from openai import OpenAI
#     import os

#     api_key = os.getenv("OPENAI_API_KEY")

#     if not api_key:
#         raise ValueError("OPENAI_API_KEY not found")

#     return OpenAI(api_key=api_key)


# def split_text(text: str, chunk_size: int = 2000) -> list:
#     """
#     Splits text into chunks to avoid token limits
#     """
#     words = text.split()
#     return [
#         " ".join(words[i:i + chunk_size])
#         for i in range(0, len(words), chunk_size)
#     ]


# def call_openai(messages, max_tokens=200):
#     try:
#         client = get_client()

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages,
#             max_tokens=max_tokens
#         )

#         return response.choices[0].message.content.strip()

#     except Exception as e:
#         return f"OpenAI Error: {str(e)}"


# def summarize_chunk(text: str) -> str:
#     """
#     Summarizes a single chunk
#     """
#     messages = [
#         {
#             "role": "system",
#             "content": "You are an expert at summarizing YouTube videos clearly and concisely."
#         },
#         {
#             "role": "user",
#             "content": f"""
# Summarize this transcript chunk into:
# - 2-3 short sentences
# - Simple and clear language
# - Keep only important information

# {text}
# """
#         }
#     ]

#     return call_openai(messages, max_tokens=200)


# def summarize_long_text(text: str) -> str:
#     """
#     Handles long transcripts using chunking
#     """
#     chunks = split_text(text)
#     summaries = []

#     for chunk in chunks:
#         summary = summarize_chunk(chunk)
#         summaries.append(summary)

#     # Combine summaries into final summary
#     combined = " ".join(summaries)

#     final_messages = [
#         {
#             "role": "system",
#             "content": "You combine multiple summaries into one clear final summary."
#         },
#         {
#             "role": "user",
#             "content": f"""
# Combine the following summaries into a single concise summary:

# {combined}
# """
#         }
#     ]

#     return call_openai(final_messages, max_tokens=300)


# def summarize_structured(text: str, language: str = None) -> str:
#     """
#     Best output: structured + readable summary
#     """
#     lang_note = f"The transcript is in {language}. Translate to English before summarizing." if language and language != "en" else ""

#     messages = [
#         {
#             "role": "system",
#             "content": "You summarize YouTube videos in a structured and easy-to-read format."
#         },
#         {
#             "role": "user",
#             "content": f"""
# {lang_note}

# Summarize the following transcript into:

# 1. Short Summary (3-4 lines)
# 2. Key Points (bullet points)
# 3. Important Insights

# Make it clear, concise, and useful.

# Transcript:
# {text}
# """
#         }
#     ]

#     return call_openai(messages, max_tokens=500)