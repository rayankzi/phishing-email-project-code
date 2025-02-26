from functions.helpers import create_claude_req_file, create_openai_req_file
from functions.claude import create_claude_batch_req

def main():
    create_openai_req_file()
    print("Hello")


if __name__ == "__main__":
    main()
