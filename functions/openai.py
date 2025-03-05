from openai import OpenAI

client = OpenAI()


def create_openai_batch_req(input_file_path: str):
    # Upload input for batch request
    batch_input_file = client.files.create(
        file=open(input_file_path, "rb"),
        purpose="batch"
    )

    print(f"Batch file uploaded: {batch_input_file}")

    batch_input_file_id = batch_input_file.id

    new_batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": "1000 Phishing emails from OpenAI GPT-4o"
        }
    )

    print(f"New batch, ${new_batch}")


def check_openai_batch_status(batch_id: str):
    batch = client.batches.retrieve(batch_id)
    print(batch)


def retrieve_openai_batch_results(output_file_id: str):
    file_response = client.files.content(output_file_id)
    print(file_response.text)
