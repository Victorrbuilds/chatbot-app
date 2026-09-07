**Self-Learning Chatbot**

A Python-based chatbot that learns from its users in real time. Instead of relying on a fixed, already trained knowledge base, it grows its own, asking users to teach it whenever it encounters a question it can't answer, and remembering the answer for next time.

**How It Works**
User asks a question.
If the bot recognizes it → it responds immediately from its existing knowledge base.
If the bot doesn't recognize it → it asks the user to provide the correct answer.
The new question-answer pair is saved to a JSON file, which acts as the bot's persistent knowledge base.
Next time the same (or a similar) question is asked, the bot answers correctly — without needing to be retrained or reprogrammed.
This creates a simple human-in-the-loop learning cycle: the bot's accuracy improves the more it's used, driven entirely by real user interaction rather than a static dataset.

**Motivation**
Most beginner chatbot tutorials rely on hardcoded responses or a fixed training set. I wanted to build something that could genuinely grow smarter through use, closer to how a person builds up knowledge over time. Working on this project got me thinking a lot about how models learn from user input, and where that kind of open-ended learning process can go wrong (e.g. bad-faith or incorrect answers being taught to the bot)  which is part of what's pulled me toward AI/security research more broadly.

**Tech Stack**
Language: Python
Storage: JSON file used as a lightweight, persistent knowledge base (no external database required)

**Example Interaction**
```
You: What is the capital of Kenya?
Bot: I don't know that yet — can you teach me the answer?
You: Nairobi
Bot: Got it, thanks! I'll remember that.

You: What is the capital of Kenya?
Bot: Nairobi
```

**Current Limitations**
Matches questions using the best match pair score, finding the best match and answers gives answers.
No handling yet for phrasing variations of the same question (e.g. "capital of Kenya?" vs "What's Kenya's capital?")
Knowledge base is a single JSON file, not yet optimized for large-scale storage
Possible Future Improvements
Add fuzzy matching or basic NLP to recognize differently-phrased versions of the same question
Add a confidence threshold before falling back to "teach me" mode
Explore replacing the JSON knowledge base with a lightweight database as it scales
Add safeguards against incorrect or malicious "teaching" input
Running the Project
```bash
python main.py
```
---
Built as a personal project to explore how simple learning systems can be built from scratch in Python.
