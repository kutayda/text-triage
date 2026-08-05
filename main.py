"""
Day 0 — provider-swappable LLM hello world.
Run:  uv run main.py gemini   |   uv run main.py groq
"""

import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError

load_dotenv()

# All these providers expose an OpenAI-compatible endpoint,
# so one client works for all — we just swap base_url + model + key.
PROVIDERS = {
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "api_key_env": "GEMINI_API_KEY",
        "model": "gemini-2.5-flash",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "model": "llama-3.3-70b-versatile",
    },
}


def get_client(provider: str) -> tuple[OpenAI, str]:
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unknown provider: {provider}. Options: {list(PROVIDERS)}")
    cfg = PROVIDERS[provider]
    api_key = os.environ.get(cfg["api_key_env"])
    if not api_key:
        raise RuntimeError(f"{cfg['api_key_env']} not found in .env")
    client = OpenAI(base_url=cfg["base_url"], api_key=api_key)
    return client, cfg["model"]


def ask(provider: str, prompt: str, max_retries: int = 3) -> str:
    client, model = get_client(provider)
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a concise, helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            return resp.choices[0].message.content
        except RateLimitError as e:
            print(f"[rate limit] {e}")
            wait = 2 ** attempt
            print(f"waiting {wait}s and retrying...")
            time.sleep(wait)
        except APIError as e:
            print(f"[api error] {e}")
            raise
    raise RuntimeError("Max retries exceeded")


if __name__ == "__main__":
    provider = sys.argv[1] if len(sys.argv) > 1 else "gemini"
    answer = ask(provider, "Merhaba! Tek cümleyle kendini tanıt.")
    print(f"[{provider}] {answer}")
