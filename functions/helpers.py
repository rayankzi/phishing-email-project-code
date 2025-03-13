import json
import random
import re
import os
from constants import (
    SYSTEM_PROMPT,
    USER_PROMPT,
    CLAUDE_REQUEST_NUMBERS,
    GEMINI_REQUEST_NUMBERS,
    OPENAI_REQUEST_NUMBERS
)
from functions.scoring import get_email_scores


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


def generate_distinct_random_sets(count=50, start=1, end=1000):
    all_possible_numbers = set(range(start, end + 1))

    claude_numbers = random.sample(list(all_possible_numbers), count)
    remaining_numbers = all_possible_numbers - set(claude_numbers)

    gemini_numbers = random.sample(list(remaining_numbers), count)
    remaining_numbers -= set(gemini_numbers)

    openai_numbers = random.sample(list(remaining_numbers), count)

    data = {
        "openai": f"These are the numbers for OpenAI: {openai_numbers}",
        "claude": f"These are the numbers for Claude: {claude_numbers}",
        "gemini": f"These are the numbers for Gemini: {gemini_numbers}"
    }

    os.makedirs("files", exist_ok=True)
    file_path = os.path.join("files", "selected-numbers.json")

    with open(file_path, "w") as f:
        json.dump(data, f)

    print("Random numbers saved")

    return data


def get_filtered_claude_request():
    matched_lines = []
    id_set = {f"claude-req-{num}" for num in CLAUDE_REQUEST_NUMBERS}

    os.makedirs("files", exist_ok=True)
    data_file = os.path.join("files", "all-claude-responses.jsonl")
    output_file = os.path.join("files", "filtered-claude-responses-for-analysis.jsonl")

    with open(data_file, 'r', encoding='utf-8') as file:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for line in file:
                try:
                    data = json.loads(line)
                    if 'custom_id' in data and data['custom_id'] in id_set:
                        json.dump(data, out_file)
                        out_file.write('\n')
                        matched_lines.append(data)
                except json.JSONDecodeError:
                    print("Skipping invalid JSON line:", line.strip())

    print("Got filtered Claude requests")


def get_filtered_gemini_request():
    request_numbers = list(dict.fromkeys(GEMINI_REQUEST_NUMBERS))
    os.makedirs("files", exist_ok=True)

    data_file = os.path.join("files", "all-gemini-responses.jsonl")
    output_file = os.path.join("files", "filtered-gemini-responses-for-analysis.jsonl")

    matched_lines = []
    skipped_numbers = []

    try:
        with open(data_file, "r", encoding="utf-8") as file, \
                open(output_file, "w", encoding="utf-8") as out_file:

            all_lines = file.readlines()

            for num in request_numbers:
                found_match = False
                for line in all_lines:
                    try:
                        data = json.loads(line)
                        system_instruction = data["request"]["system_instruction"]["parts"][0]["text"]
                        match_string = (f"\nYou are request number {num}. "
                                        f"Make sure you specify that at the beginning of your response")
                        if match_string in system_instruction:
                            if data not in matched_lines:
                                json.dump(data, out_file)
                                out_file.write('\n')
                                matched_lines.append(data)
                                found_match = True
                                break

                    except json.JSONDecodeError:
                        print(f"Skipping invalid JSON line: {line.strip()}")

                # Track numbers that couldn't be found
                if not found_match:
                    skipped_numbers.append(num)

        # Print out detailed information
        print(f"Total requests filtered: {len(matched_lines)}")
        print(f"Skipped request numbers: {skipped_numbers}")

        # Raise an error if we didn't get exactly 50 matches
        if len(matched_lines) != 50:
            raise ValueError(f"Expected 50 matches, but found {len(matched_lines)}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_claude_emails_list():
    file_path = os.path.join("files", "claude", "filtered-claude-responses-for-analysis.jsonl")
    final_list = []

    with open(file_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

        for line in all_lines:
            obj = json.loads(line)
            final_list.append({
                "request_id": obj["custom_id"],
                "text": obj["result"]["message"]["content"][0]["text"]
            })

    return final_list


def get_gemini_emails_list():
    file_path = os.path.join("files", "gemini", "filtered-gemini-responses-for-analysis.jsonl")
    final_list = []

    with open(file_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

        for line in all_lines:
            obj = json.loads(line)
            system_instruction = obj["request"]["system_instruction"]["parts"][0]["text"]
            temp = re.findall(r'\d+', system_instruction.partition("You are request number")[2])
            request_id = list(map(int, temp))[0]

            final_list.append({
                "request_id": request_id,
                "text": obj["response"]["candidates"][0]["content"]["parts"][0]["text"]
            })

    return final_list


def get_filtered_openai_requests():
    matched_lines = []
    id_set = {f"openai-request-{num}" for num in OPENAI_REQUEST_NUMBERS}

    os.makedirs("files", exist_ok=True)
    output_file = os.path.join("files", "openai", "filtered-openai-responses-for-analysis.jsonl")

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for i in range(1, 11):
            data_file = os.path.join("files", "openai", "response-files", f"openai-batch-part-{i}-responses.jsonl")

            with open(data_file, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        data = json.loads(line)
                        if 'custom_id' in data and data['custom_id'] in id_set:
                            json.dump(data, out_file)
                            out_file.write('\n')
                            matched_lines.append(data)
                    except json.JSONDecodeError:
                        print("Skipping invalid JSON line:", line.strip())

    print("Got filtered OpenAI requests")


def get_openai_emails_list():
    file_path = os.path.join("files", "openai", "filtered-openai-responses-for-analysis.jsonl")
    final_list = []

    with open(file_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

        for line in all_lines:
            obj = json.loads(line)
            final_list.append({
                "request_id": obj["custom_id"],
                "text": obj["response"]["body"]["choices"][0]["message"]["content"]
            })

    return final_list


def create_analysis_constants_file():
    def get_bleu_scores(score_list):
        result = []
        for obj in score_list:
            result.append(obj["bleu_score"])

        return result

    def get_rouge_score(score_list):
        result = []
        for obj in score_list:
            result.append(obj["rouge1_score"])

        return result

    openai_email_list = get_openai_emails_list()
    openai_email_score_list = get_email_scores(openai_email_list)

    claude_email_list = get_claude_emails_list()
    claude_email_score_list = get_email_scores(claude_email_list)

    gemini_email_list = get_gemini_emails_list()
    gemini_email_score_list = get_email_scores(gemini_email_list)

    file_path = os.path.join("statistics", "analysis_materials.py")

    text = f"""
    openai_bleu_scores = {get_bleu_scores(openai_email_score_list)}
    claude_bleu_scores = {get_bleu_scores(claude_email_score_list)}
    gemini_bleu_scores = {get_bleu_scores(gemini_email_score_list)}

    openai_rouge_scores = {get_rouge_score(openai_email_score_list)}
    claude_rouge_scores = {get_rouge_score(claude_email_score_list)}
    gemini_rouge_scores = {get_rouge_score(gemini_email_score_list)}
    """

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
