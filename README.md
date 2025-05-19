# 🎉 Fun AI Playground

![Streamlit](https://img.shields.io/badge/Streamlit-✨%20Fun--AI--Playground-blue)
![Python](https://img.shields.io/badge/Python-3.12-green)
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)

A playful Streamlit app that lets you interact with AI-powered features:

* **📝 Text Summarizer**: Generate concise summaries from any input text.
* **🤣 Joke Generator**: Get fresh, family-friendly jokes on demand.
* **🌸 Haiku Writer**: Craft beautiful haiku poems on a topic of your choice.
* **🎲 Tic Tac Toe vs AI**: Challenge a simple AI in a classic 3×3 board game.

---

## 🚀 Features

1. **Intuitive UI**: Clean, modern design with sidebar navigation and responsive layout.
2. **Real-time Interactions**: Instant feedback on your inputs, including game moves.
3. **Session Memory**: Avoids repeating jokes within the same session.
4. **Custom Styling**: Distinct feature boxes, output highlights, and themed haiku containers.
5. **AI Integration**: Uses OpenAI GPT-4o (or GPT-3.5-turbo) for natural language tasks.

---

## 📸 Screenshots

<p align="center">
  <img src="https://via.placeholder.com/800x400?text=Fun+AI+Playground+Dashboard" alt="App Screenshot" width="80%">
</p>

---

## 🛠️ Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-org/fun-ai-playground.git
   cd fun-ai-playground
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Streamlit secrets**:

   * Create a file at `~/.streamlit/secrets.toml` with:

     ```toml
     [openai]
     api_key = "YOUR_OPENAI_API_KEY"
     ```

5. **Run the app**:

   ```bash
   streamlit run fun_streamlit_app.py
   ```

---

## ⚙️ Usage

1. Open the app in your browser (usually at `http://localhost:8501`).
2. Select an activity from the sidebar.
3. Follow on-screen prompts:

   * **Summarizer**: Paste text and click **Summarize**.
   * **Joke Generator**: Click **Tell me a joke!**.
   * **Haiku Writer**: Enter a topic and click **Generate Haiku**.
   * **Tic Tac Toe**: Click a square to place your **X**, then watch the AI move **O**.
   * **Reset Game** resets the board for a new match.

---

## 📚 Requirements

* Python 3.8+
* `streamlit`
* `openai`

Install with:

```bash
pip install streamlit openai
```

---

## 📝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to:

* Fork the repo
* Create a new branch for your feature/fix
* Submit a pull request

Please follow [Contributor Covenant](https://www.contributor-covenant.org/) guidelines.

---

## 🔒 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
  Built with ❤️ by [Your Name]
</div>
