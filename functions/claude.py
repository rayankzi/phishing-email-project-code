import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from functions.constants import SYSTEM_PROMPT, USER_PROMPT
from functions.helpers import write_to_file

client = anthropic.Anthropic()


def create_claude_batch_req():
    request_list = []

    for i in range(1, 1001):
        request_list.append(
            Request(
                custom_id=f"claude-req-{i}",
                params=MessageCreateParamsNonStreaming(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    system=[
                        {
                            "type": "text",
                            "text": SYSTEM_PROMPT,
                            "cache_control": {"type": "ephemeral"}
                        }
                    ],
                    messages=[{
                        "role": "user",
                        "content": USER_PROMPT,
                    }]
                )
            )
        )

    message_batch = client.messages.batches.create(requests=request_list)
    write_to_file("claude-req-info.json", message_batch)


def check_claude_batch_status(batch_id: str):
    message_batch = client.messages.batches.retrieve(batch_id)
    print(f"Batch {message_batch.id} processing status is {message_batch.processing_status}")


def get_claude_batch_results(batch_id: str):
    for result in client.messages.batches.results(batch_id):
        match result.result.type:
            case "succeeded":
                print(f"Success! {result.custom_id}")
            case "errored":
                if result.result.error.type == "invalid_request":
                    # Request body must be fixed before re-sending request
                    print(f"Validation error {result.custom_id}")
                else:
                    # Request can be retried directly
                    print(f"Server error {result.custom_id}")
            case "expired":
                print(f"Request expired {result.custom_id}")
