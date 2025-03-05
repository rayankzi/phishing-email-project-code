import os
import time
import vertexai
from dotenv import load_dotenv
from vertexai.batch_prediction import (
    BatchPredictionJob
)

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
vertexai.init(
    project=PROJECT_ID,
    location="us-central1"
)


def create_gemini_batch_req():
    input_uri = \
        ("gs://request_storage_bucket/gemini-req."
         "jsonl")
    output_uri = \
        ("gs://request_storage_bucket/gemini-res."
         "jsonl")

    batch_prediction_job = BatchPredictionJob.submit(
        source_model="gemini-2.0-flash-001",
        input_dataset=input_uri,
        output_uri_prefix=output_uri,
    )

    # Check job status
    print(f"Job resource name: "
          f"{batch_prediction_job.resource_name}")
    print(f"Model resource name with the job: "
          f"{batch_prediction_job.model_name}")
    print(f"Job state: "
          f"{batch_prediction_job.state.name}")

    # Refresh the job until complete
    while not batch_prediction_job.has_ended:
        time.sleep(5)
        batch_prediction_job.refresh()

    # Check if the job succeeds
    if batch_prediction_job.has_succeeded:
        print("Job succeeded!")
    else:
        print(f"Job failed: "
              f"{batch_prediction_job.error}")

    # Check the location of the output
    print(f"Job output location: "
          f"{batch_prediction_job.output_location}")
