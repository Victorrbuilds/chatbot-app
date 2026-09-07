import json
import os
from difflib import SequenceMatcher

KB_FILE = "knowledge_base.json"
SIMILARITY_THRESHOLD = 0.75

STOP_WORDS = {
    "what", "is", "are", "the", "a", "an", "of", "to", "do", "does",
    "how", "can", "you", "i", "in", "on", "for", "your", "my"
}


def normalize(text):
    words = [w for w in text.lower().strip().split() if w not in STOP_WORDS]
    return " ".join(words) if words else text.lower().strip()


def load_knowledge_base(path=KB_FILE):
    if not os.path.exists(path):
        return {"qa_pairs": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_knowledge_base(kb, path=KB_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)


def similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def find_best_match(user_question, kb):
    best_pair = None
    best_score = 0.0

    for pair in kb.get("qa_pairs", []):
        score = similarity(user_question, pair["question"])
        if score > best_score:
            best_score = score
            best_pair = pair

    return best_pair, best_score


def teach_bot(user_question, kb):
    print("Bot: I don't know the answer to that yet. Can you teach me? (type the answer)")
    answer = input("Your answer: ").strip()

    if answer:
        kb["qa_pairs"].append({"question": user_question, "answer": answer})
        save_knowledge_base(kb)
        print("Bot: Thanks! I've learned that.")
    else:
        print("Bot: No answer given, so I won't save anything.")


def chat():
    kb = load_knowledge_base()
    print("Bot: Hi! Ask me anything. Type 'quit' to exit.")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("Bot: Goodbye!")
            break

        best_pair, score = find_best_match(user_input, kb)

        if best_pair and score >= SIMILARITY_THRESHOLD:
            print(f"Bot: {best_pair['answer']}")
        else:
            teach_bot(user_input, kb)


if __name__ == "__main__":
    chat()
