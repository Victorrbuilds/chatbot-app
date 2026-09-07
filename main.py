import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
KB_FILE = Path("knowledge_base.json")
SIMILARITY_THRESHOLD = 0.35

class LearningChatbot:
    def __init__(self, kb_file=KB_FILE):
        self.kb_file = kb_file
        self.knowledge_base = self.load_kb()
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.questions = []
        self.answers = []
        self.matrix = None
        self.rebuild_index()

    def load_kb(self):
        if self.kb_file.exists():
            with open(self.kb_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_kb(self):
        with open(self.kb_file, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)

    def rebuild_index(self):
        self.questions = [item["question"] for item in self.knowledge_base]
        self.answers = [item["answer"] for item in self.knowledge_base]
        self.matrix = self.vectorizer.fit_transform(self.questions) if self.questions else None

    def teach(self, question, answer):
        self.knowledge_base.append({"question": question.strip(), "answer": answer.strip()})
        self.save_kb()
        self.rebuild_index()
        return "Thanks, I learned that."

    def find_best_answer(self, user_question):
        if not self.knowledge_base or self.matrix is None:
            return None, 0.0

        query_vec = self.vectorizer.transform([user_question])
        scores = cosine_similarity(query_vec, self.matrix).flatten()
        best_index = scores.argmax()
        return self.answers[best_index], float(scores[best_index])

botbrain = LearningChatbot()
TEACH_MODE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi, I am a learning chatbot.\n"
        "Ask me anything.\n"
        "If I do not know, I will ask you to teach me."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id in TEACH_MODE:
        original_question = TEACH_MODE.pop(user_id)
        response = botbrain.teach(original_question, text)
        await update.message.reply_text(response)
        return

    answer, score = botbrain.find_best_answer(text)

    if answer and score >= SIMILARITY_THRESHOLD:
        await update.message.reply_text(answer)
    else:
        TEACH_MODE[user_id] = text
        await update.message.reply_text(
            "I do not know that yet.\n"
            "Please send me the correct answer, and I will learn it."
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()