from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import StringIO
import openai
import re

app = FastAPI()

openai.api_key = "api_key"


MAX_TOKENS_LIMIT = 4000

def count_tokens(text: str) -> int:
    return len(text) // 2

def split_text_by_sentences(text: str, max_tokens: int) -> list:
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_tokens:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_chunk_with_chatgpt(chunk: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 회의록을 요약하는 도우미입니다. 주어진 텍스트를 간결하고 명확한 한국어 요약문으로 작성하세요."},
            {"role": "user", "content": f"다음 회의록을 요약해 주세요:\n{chunk}"}
        ],
        temperature=0.5,  # 0.0~2.0 까지 입력 가능 / 수치가 낮을 수록 간결하고 안정적인 요약, 높을 수록 결과가 더 다양하고 창의적
        max_tokens=350,   # 요약본의 최대 출력 텍스트 길이
        frequency_penalty=0.2,  # -2.0 ~ 2.0 까지 입력 가능 / 반복될 가능성을 조절
        presence_penalty=0.1,   # -2.0 ~ 2.0 까지 입력 가능 / 새로운 정보나 단어를 생성 가능성 조절
        #top_p=0.9  # 0.0~1.0 까지 입력 가능 / 샘플링에서 확률의 누적 합계를 기반으로 선택
    )
    return response["choices"][0]["message"]["content"].strip()


@app.post("/summarize")
async def summarize(file: UploadFile):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    content = await file.read()
    text = content.decode("utf-8")

    token_count = count_tokens(text)

    if token_count > MAX_TOKENS_LIMIT:
        chunk_size = (MAX_TOKENS_LIMIT - 500) * 2
        chunks = split_text_by_sentences(text, chunk_size)
        partial_summaries = [summarize_chunk_with_chatgpt(chunk) for chunk in chunks]
        combined_summaries = "\n".join(partial_summaries)
    else:
        combined_summaries = summarize_chunk_with_chatgpt(text)

    file_like = StringIO()
    file_like.write(combined_summaries)
    file_like.seek(0)

    return StreamingResponse(
        file_like,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=summary.txt"},
    )

@app.get("/")
async def root():
    return {"message": "Upload a .txt file to /summarize to get a summary."}