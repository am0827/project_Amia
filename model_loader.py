from llama_cpp import Llama

def load_model():
    model_path = r"C:/Users/User/Desktop/mizuki_chatbot/models/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf"
    llm = Llama(
        model_path=model_path,
        n_ctx=1024  # 최대 컨텍스트 토큰 수를 1024로 설정
    )
    return llm
