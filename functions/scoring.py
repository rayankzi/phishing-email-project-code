import json
import os
from constants import HUMAN_WRITTEN_EMAIL
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer


def get_email_scores(email_list):
    ref = HUMAN_WRITTEN_EMAIL.split()
    score_list = []
    rouge1_scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

    for email in email_list:
        hyp = email["text"].split()
        bleu_score = sentence_bleu([ref], hyp)
        rouge_scores = rouge1_scorer.score(HUMAN_WRITTEN_EMAIL, email["text"])
        score_list.append({
            "request_id": email["request_id"],
            "bleu_score": bleu_score,
            "rouge1_score": rouge_scores["rouge1"].fmeasure
        })

    return score_list


def write_score_results_to_file(model_type, score_list):
    os.makedirs("files", exist_ok=True)
    file_path = os.path.join("files", f"{model_type}-score-file.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(score_list, f)

    print(f"{model_type} scoring data saved")
