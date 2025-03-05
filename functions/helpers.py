import json
import random
import os
from functions.constants import SYSTEM_PROMPT, USER_PROMPT


def create_gemini_req_file():
    file_path = os.path.join("files", "gemini-req.jsonl")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        for i in range(1, 1001):
            data = {
                "request": {
                    "contents": [{"role": "user", "parts": [{"text": USER_PROMPT}]}],
                    "system_instruction": {
                        "parts": [{
                            "text": f"{SYSTEM_PROMPT}\nYou are request number {i}. "
                                    f"Make sure you specify that at the beginning of your response."
                        }]
                    }
                }
            }
            f.write(json.dumps(data, separators=(",", ":")) + "\n")

    print(f"File '{file_path}' has been created with 1000 lines.")


def create_openai_req_file():
    base_req = {
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": USER_PROMPT
                }
            ]
        }
    }

    os.makedirs("files", exist_ok=True)

    for i in range(1, 10):
        file_path = os.path.join("files", f"openai-req-${i}.jsonl")

        with open(file_path, "w") as f:
            for i in range(1, 100):
                request = base_req.copy()
                request["custom_id"] = f"openai-request-{i}"
                f.write(json.dumps(request) + "\n")


def generate_random_numbers(count=50, start=1, end=1000):
    claude_numbers = [random.randint(start, end) for _ in range(count)]
    gemini_numbers = [random.randint(start, end) for _ in range(count)]
    openai_numbers = [random.randint(start, end) for _ in range(count)]

    data = {
        "openai": f"These are the numbers for OpenAI: {openai_numbers}",
        "claude": f"These are the numbers for OpenAI: {claude_numbers}",
        "gemini": f"These are the numbers for OpenAI: {gemini_numbers}"
    }

    os.makedirs("files", exist_ok=True)
    file_path = os.path.join("files", f"selected-numbers.json")

    with open(file_path, "w") as f:
        json.dump(data, f)

    print("Random numbers saved")

