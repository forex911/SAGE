# ⚡ SAGE AI

A production-grade AI-powered screenshot analysis tool. Upload any screenshot — error messages, code, terminal output, UI screens — and get **structured, in-depth AI explanations and solutions** in seconds.

Built with **Streamlit** + **Groq Vision API** (Llama 4 Scout).

---

## ✨ Features

- 📤 **Drag-and-drop image upload** (PNG, JPG, WEBP, GIF)
- 🤖 **AI Vision analysis** via Groq's Llama 4 Scout model (free tier)
- 📋 **Structured 10-section output**: Content Type, Summary, Analysis, Errors, Root Cause, Solutions, Improved Code, UI/UX Feedback, Beginner Explanation, Confidence Level
- 📊 **Formatted & Raw views** with tabbed output display
- 📜 **Session history** — revisit past analyses from the sidebar
- 📈 **Session stats** — track your analysis count
- ⬇️ **Export analysis** as `.txt` or `.md`
- 🎨 **Premium dark UI** with glassmorphism, micro-animations, and ambient effects
- ⏱ **Response time tracking** per analysis
- 📏 **Auto image resizing** for large files
- 🔐 **API key via UI** — never stored to disk

---

## 🛠️ Tech Stack

| Layer     | Technology                                |
|-----------|-------------------------------------------|
| Frontend  | Streamlit (custom CSS design system)      |
| AI Model  | Groq Vision · Llama 4 Scout 17B          |
| Image     | Pillow (PIL)                              |
| HTTP      | httpx (direct API calls, no SDK)          |
| Language  | Python 3.9+                               |

---

## 📁 Project Structure

```
SAGE/
├── app.py              # Main Streamlit UI (production-grade)
├── vision.py           # Groq Vision API integration (HTTP)
├── prompts.py          # System prompt for the AI
├── utils.py            # Helper functions (base64, resize, etc.)
├── uploads/            # Temporary storage for uploaded images
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .gitignore
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/forex911/sage.git
cd sage
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your Groq API Key (Free)

1. Visit [console.groq.com](https://console.groq.com)
2. Create a free account and generate an API key
3. Copy ot — you'll paste it into the app sidebar

> No `.env` file needed. The API key is entered directly in the Streamlit UI.

### 5. Run the app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 💡 How to Use

1. **Open** the app at `http://localhost:8501`
2. **Paste your Groq API key** in the sidebar
3. **Upload a screenshot** by drag-and-drop or file browser
4. Click **"⚡ RUN ANALYSIS"**
5. View the **formatted or raw** analysis output
6. **Download** as `.txt` or `.md`
7. Check **session history** in the sidebar for past analyses

---

## 🖼️ Example Use Cases

| Screenshot Type   | What You Get                                       |
|-------------------|-----------------------------------------------------|
| Python traceback  | Error type, root cause, fix with corrected code     |
| Terminal output   | Command breakdown, what went wrong, next steps      |
| React error       | Component issue, stack trace explanation, fix        |
| UI design         | UX feedback, accessibility issues, suggestions      |
| SQL query         | Query logic, performance issues, optimised version  |
| VS Code / IDE     | Config issues, extension problems, fixes            |

---

## ⚠️ Notes

- **Cost**: Groq free tier — $0.00 per analysis
- **Image size**: Files > 4 MB are automatically resized
- **Privacy**: Images saved locally in `uploads/` only
- **Rate limits**: Groq has rate limits on the free tier; wait and retry if hit

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| `AuthenticationError` | Ensure key starts with `gsk_` and is valid |
| `Model not found` | Model may be temporarily unavailable on Groq |
| Blank output | Try a sharper, higher-resolution screenshot |
| App won't start | Run `pip install -r requirements.txt` again |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Credits

- [Groq](https://groq.com) for the ultra-fast Vision API
- [Meta AI](https://ai.meta.com) for the Llama 4 Scout model
- [Streamlit](https://streamlit.io) for the rapid UI framework
- [Pillow](https://pillow.readthedocs.io) for image processing
