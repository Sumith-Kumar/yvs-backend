# import requests


# def split_text(text: str, chunk_size: int = 2000) -> list:
#     words = text.split()
#     return [
#         " ".join(words[i:i + chunk_size])
#         for i in range(0, len(words), chunk_size)
#     ]


# def call_llm(prompt: str) -> str:
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "mistral",
#                 "prompt": prompt,
#                 "stream": False
#             }
#         )

#         return response.json()["response"]

#     except Exception as e:
#         return f"Ollama Error: {str(e)}"


# def summarize_chunk(text: str) -> str:
#     prompt = f"""
# Summarize this YouTube transcript chunk clearly:
# - 2-3 sentences
# - Keep important points only

# {text}
# """
#     return call_llm(prompt)


# def summarize_long_text(text: str) -> str:
#     chunks = split_text(text)
#     summaries = []

#     for chunk in chunks:
#         summaries.append(summarize_chunk(chunk))

#     combined = " ".join(summaries)

#     final_prompt = f"""
# Combine these summaries into a single clear summary:

# {combined}
# """
#     return call_llm(final_prompt)


# def summarize_structured(text: str, language: str = None) -> str:
#     lang_note = ""
#     if language and language != "en":
#         lang_note = f"The transcript is in {language}. Translate to English before summarizing."

#     prompt = f"""
# {lang_note}

# Summarize this YouTube video into:

# 1. Short Summary (3-4 lines)
# 2. Key Points (bullet points)
# 3. Important Insights

# {text}
# """

#     return call_llm(prompt)