from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# ===================== 你的阿里云 KEY =====================
DASHSCOPE_API_KEY = "sk-59ba94bfec5349f59597dcc1f05d7fee"
# ==========================================================

app = FastAPI()

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 接口（必须放在最前面，绝对不被覆盖）
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        client = OpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        completion = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": req.message}]
        )
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

# 【关键修复】只匹配 / 不影响 /chat
@app.get("/", include_in_schema=False)
async def index():
    return FileResponse("./static/index.html")

# 静态资源
app.mount("/static", StaticFiles(directory="static"), name="static")