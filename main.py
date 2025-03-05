from functions.claude import create_claude_batch_req
from functions.helpers import create_gemini_req_file, generate_random_numbers
from functions.gemini import create_gemini_batch_req
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


def main():
    generate_random_numbers()
    print("Hello")


if __name__ == "__main__":
    main()
