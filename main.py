import os
from functions.scoring import get_best_entry
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def main():
    print(get_best_entry(os.path.join("files", "openai", "openai-score-file.json")))
    print(get_best_entry(os.path.join("files", "gemini", "gemini-score-file.json")))
    print(get_best_entry(os.path.join("files", "claude", "claude-score-file.json")))


if __name__ == "__main__":
    main()
# absl,  rouge_score, nltk
