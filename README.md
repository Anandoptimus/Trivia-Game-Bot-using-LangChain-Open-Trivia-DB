# 🎮 Trivia Game Bot using LangChain & Open Trivia DB

This is a conversational Trivia Game Bot built using **LangChain**, **OpenAI Chat Models**, and the **Open Trivia Database (OpenTDB)**. The bot asks fun multiple-choice questions, checks your answers, and keeps the game going!

---

## 🚀 Features

- 🤖 Powered by LangChain's function-calling and tool integrations
- 📚 Uses OpenTDB API to fetch real trivia questions
- 🧠 Maintains chat history using conversation memory
- 🎯 Validates answers strictly in `"option) answer"` format
- 🔁 Supports replay: you can keep playing as long as you want

---

## 🧩 Tech Stack

- Python
- [LangChain](https://www.langchain.com/)
- [OpenAI GPT-3.5 Turbo](https://platform.openai.com/)
- [Open Trivia Database API](https://opentdb.com/)

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/trivia-game-bot.git
   cd trivia-game-bot
   ```

2. **Create and activate a virtual environment**
   python -m venv venv
   venv\Scripts\activate on Windows

3. **Install dependencies**
   pip install -r requirements.txt
   
4. **Set your OpenAI API key**
   set OPENAI_API_KEY=your-api-key


## 🧠 How It Works
- The get_trivia_questions tool fetches a multiple-choice question from OpenTDB.
- The LangChain agent prompts the user to answer in "option) answer" format.
- The response is validated and feedback is given.
- Memory stores previous questions and responses for continuity.

## 📁 Project Structure
```
  trivia-game-bot/
  ├── main.py               # Core LangChain logic
  ├── requirements.txt      # Python dependencies
  └── README.md             # Project info
```

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 👏 Acknowledgements
- Open Trivia DB
- LangChain
- OpenAI
