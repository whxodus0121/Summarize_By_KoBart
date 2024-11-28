from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from io import StringIO
import re

app = FastAPI()

tokenizer = PreTrainedTokenizerFast.from_pretrained("gogamza/kobart-summarization")
model = BartForConditionalGeneration.from_pretrained("gogamza/kobart-summarization")


def preprocess_text(text):
    processed_text = re.sub(r'[가-힣\w]+\s*:\s*', '', text)
    return processed_text

def split_text(text, chunk_size=200):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks


def summarize_chunk(chunk):
    input_ids = tokenizer.encode(chunk, return_tensors="pt", truncation=True, max_length=1024)
    summary_ids = model.generate(
        input_ids,
        min_length=20,
        max_length=100,
        no_repeat_ngram_size=2,
        num_beams=5,
        length_penalty=1.0,
        early_stopping=True,
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.post("/summarize")
async def summarize(file: UploadFile):
    try:
       
        if not file.filename.endswith(".txt"):
            raise HTTPException(status_code=400, detail="Only .txt files are supported")

       
        content = await file.read()
        text = content.decode("utf-8")

        
        preprocessed_text = preprocess_text(text)

        
        chunks = split_text(preprocessed_text, chunk_size=200)

        
        partial_summaries = [summarize_chunk(chunk) for chunk in chunks]

       
        combined_summaries = "\n".join(partial_summaries)

        
        file_like = StringIO()
        file_like.write(combined_summaries)
        file_like.seek(0)

        return StreamingResponse(
            file_like,
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=partial_summaries.txt"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Upload a .txt file to /summarize to get a summary."}
