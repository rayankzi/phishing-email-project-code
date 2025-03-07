from dotenv import load_dotenv
from functions.helpers import get_filtered_claude_request, get_filtered_gemini_request
from functions.constants import GEMINI_REQUEST_NUMBERS, OPENAI_REQUEST_NUMBERS, CLAUDE_REQUEST_NUMBERS

# Load environment variables from the .env file
load_dotenv()


def main():
    get_filtered_claude_request()
    get_filtered_gemini_request()
    print("Hello")


if __name__ == "__main__":
    main()
