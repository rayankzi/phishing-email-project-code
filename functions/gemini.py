import time
from google import genai
from google.genai import types
from functions.constants import SYSTEM_PROMPT, USER_PROMPT
from functions.helpers import write_to_file

client = genai.Client(api_key="GEMINI_API_KEY")


def perform_gemini_request(index: int):
    print(f"Sending request ${index}")

    response = client.models.generate_content(
        model="gemini-1.5-pro",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        ),
        contents=[USER_PROMPT]
    )

    return response.text


def perform_gemini_batch_request():
    results = []

    for i in range(1, 1001):
        response = perform_gemini_request(i)
        results.append({
            "request_id": f"gemini-request-${i}",
            response: response
        })

        time.sleep(1)

    write_to_file("gemini-responses.json", results)
