from langchain_openai import ChatOpenAI
from tiktoken import encoding_for_model

model = "gpt-4o-mini"

def load_model(openai_api_key):
    return ChatOpenAI(
        model_name=model,
        openai_api_key=openai_api_key,
        temperature=0.01,
        max_tokens=4096,
        top_p=0.9
    )

def count_tokens(text, model=model):
    encoder = encoding_for_model(model)
    return len(encoder.encode(text))