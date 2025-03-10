from dotenv import load_dotenv
from functions.scoring import get_email_scores, write_score_results_to_file
from functions.helpers import get_claude_emails_list, get_gemini_emails_list

# Load environment variables from the .env file
load_dotenv()


def main():
    # print()
    claude_emails = get_claude_emails_list()
    gemini_emails = get_gemini_emails_list()

    claude_scores = get_email_scores(claude_emails)
    gemini_scores = get_email_scores(gemini_emails)

    write_score_results_to_file("claude", claude_scores)
    write_score_results_to_file("gemini", gemini_scores)


if __name__ == "__main__":
    main()
# absl,  rouge_score, nltk
