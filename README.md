# KAUTILYA — AI-Powered Data Analysis Agent
### Groq LLaMA3 | Voice Enabled | Auto Visualizations | Streamlit

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-FF6F00?style=for-the-badge&logo=groq&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![GenAI](https://img.shields.io/badge/Generative_AI-Agentic-412991?style=for-the-badge)
![Voice](https://img.shields.io/badge/Voice-Hindi%20%7C%20English-00C853?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-00C853?style=for-the-badge)

> 🤖 An **Agentic AI** system named after ancient Indian strategist **Chanakya (Kautilya)**.
> Upload any CSV/Excel file, ask questions in **text or voice** (Hindi/English),
> and get instant **AI-powered data insights** with automatic visualizations.
> Powered by **Groq's LLaMA3** — the fastest AI inference available.

---

## 🌐 Project Demo

> Run locally using the steps below. Voice feature fully enabled on local setup!

---

## 📌 Project Overview

KAUTILYA is a domain-specific **Generative AI + Agentic AI** application built for
data analysis. Unlike generic chatbots, KAUTILYA:
- Accepts **real business data** (CSV/Excel) — data never leaves your system
- Maintains **conversation context** across multiple questions
- **Autonomously analyzes** data and generates actionable recommendations
- Supports **voice interaction** in Hindi and English
- Generates **automatic visualizations** based on data type

---

## ✨ Key Features

| Feature | Details |
|---------|---------|
| **AI Brain** | Groq LLaMA3 70B — transformer-based LLM |
| **Voice Input** | Hindi & English via Google Speech API |
| **Voice Output** | Google Text-to-Speech (gTTS) |
| **Auto Analysis** | Complete dataset analysis in one click |
| **Visualizations** | Distribution, Correlation, Categories, Missing Values |
| **Data Explorer** | Preview, Statistics, Column Info |
| **Security** | API key stored in .env — never exposed |
| **Sample Datasets** | E-Commerce Orders, Superstore Sales |

---

## 🤖 What Makes This Agentic AI?
```
Traditional Chatbot    = Answers predefined questions
KAUTILYA (Agentic AI)  = Autonomously:
                         → Loads and understands any dataset
                         → Maintains conversation memory
                         → Generates insights without instructions
                         → Recommends next steps proactively
```

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| **Groq + LLaMA3** | AI inference — fastest LLM API available |
| **Streamlit** | Web application framework |
| **SpeechRecognition** | Voice input — Hindi & English |
| **gTTS** | Google Text-to-Speech voice output |
| **pygame** | Audio playback |
| **python-dotenv** | Secure API key management |
| **Pandas** | Data manipulation |
| **Matplotlib & Seaborn** | Statistical visualizations |
| **Plotly** | Interactive charts |

---

## 🚀 How to Run Locally

### 1. Clone Repository
```bash
git clone https://github.com/DeveshShukla23/KAUTILYA-AI-Data-Analysis-Agent.git
cd KAUTILYA-AI-Data-Analysis-Agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup API Key
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```
> Get your free API key at: [console.groq.com](https://console.groq.com)

### 4. Run the App
```bash
streamlit run agent.py
```

---

## 📂 Project Structure
```
KAUTILYA-AI-Data-Analysis-Agent/
│
├── agent.py                    # Main application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Excludes .env file
│
└── sample_data/
    ├── Order Details.csv       # E-Commerce dataset
    ├── Sample - Superstore.csv # Retail sales dataset
    └── NIFTY50_all.csv         # ⚠️ Not included (exceeds GitHub 25MB limit)
```

> ⚠️ **Note:** NIFTY50 dataset is not included in this repository due to
> GitHub's 25MB file size limit. Download it from
> [Kaggle — NIFTY50 Stock Market Data](https://www.kaggle.com/datasets/rohanrao/nifty50-stock-market-data)
> and place it in the `sample_data/` folder.

---

## 💡 How to Use
```
1. Run the app locally
2. Select data source from sidebar:
   → Upload your own CSV/Excel file
   → Or use provided sample datasets
3. Ask questions in text or voice
4. Click "Auto Analyze Dataset"
   for complete instant analysis
5. Explore visualizations in
   "Auto Visualizations" tab
```

---

## 🔐 Security Note
```
API Key is stored in .env file
.env is listed in .gitignore
= API key is NEVER pushed to GitHub
= Safe for public repositories
```

---

## 🔮 Future Improvements

- Real-time database connectivity
- Automated ML model training on uploaded data
- PDF report generation
- Multi-step agent planning using LangChain
- Hindi/Hinglish full language support
- Streamlit Cloud deployment with mic workaround

---

## 📊 Sample Datasets Included

| Dataset | Rows | Domain |
|---------|------|--------|
| Order Details | 500 | E-Commerce |
| Sample Superstore | 9994 | Retail Sales |
| NIFTY50 (Download separately) | 235,192 | Stock Market |

---

## 👨‍💻 Author

**Devesh Shukla**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/devesh-shukla23)
[![GitHub](https://img.shields.io/badge/GitHub-DeveshShukla23-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DeveshShukla23)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:shukladevesh40@gmail.com)
