import sys
import os
sys.path.append(r"C:/Users/User/Desktop/mizuki_chatbot/backend")

from fastapi import FastAPI
from pydantic import BaseModel
from model_loader import load_model

app = FastAPI(title="아키야마 미즈키 챗봇 API")

# 모델 로딩
llm = load_model()

# 프롬프트 파일 절대경로
PROMPT_PATH = r"C:/Users/User/Desktop/mizuki_chatbot/backend/prompt/mizuki_prompt.txt"

# 프롬프트 읽기
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    system_prompt = f.read()
 
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    prompt = f"{system_prompt}\n사용자: {req.message}\n미즈키:"

    # stop token 지정
    result = llm(
        prompt=prompt,
        max_tokens=256,
        temperature=0.6,
        stop=["사용자:", "미즈키:"]  # 여기서 stop token 지정
    )

    reply = result['choices'][0]['text'].strip()
    return {"reply": reply}

@app.get("/health")
def health():
    if llm is None:
        return JSONResponse({"status": "loading"})
    return {"status": "ready"}
