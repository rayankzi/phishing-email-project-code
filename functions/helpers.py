import json
import os
from functions.constants import SYSTEM_PROMPT, USER_PROMPT


def create_claude_req_file():
    req_data = []

    for i in range(1, 1001):
        req_data.append({
            "custom_id": f"claude-request-{i}",
            "params": {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 1000,
                "system": [
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                "messages": [
                    {
                        "role": "user",
                        "content": USER_PROMPT
                    }
                ]
            }
        })

    write_to_file("claude-req.json", req_data)

    return req_data


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
    file_path = os.path.join("files", "openai-req.jsonl")

    with open(file_path, "w") as f:
        for i in range(1, 1001):
            request = base_req.copy()
            request["custom_id"] = f"openai-request-{i}"
            f.write(json.dumps(request) + "\n")


def write_to_file(file_name, data):
    output_dir = "files"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Data written to {file_name}")
