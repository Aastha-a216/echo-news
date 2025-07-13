import customtkinter as ctk
import requests
import pyttsx3
from fpdf import FPDF
from datetime import datetime
import threading

# ---------- Config ----------
API_KEY = "e4f8d019969f4344961cbcbbfeb3c57f" # Replace with your NewsAPI key
TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"
CATEGORIES = ["general", "technology", "business", "sports", "science", "health", "entertainment"]
COUNTRY = "us"

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

# ---------- Setup ----------
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)
current_mode = "light"
latest_news = []

# ---------- Functions ----------

def get_news(category, language):
    """Fetch news from NewsAPI. 
    If language is English, use top-headlines with country + category.
    Otherwise, use everything endpoint with language filter and query='news'."""
    try:
        if language == "en":
            # Use top-headlines endpoint for English
            params = {
                "country": COUNTRY,
                "category": category,
                "apiKey": API_KEY,
                "pageSize": 5,
            }
            res = requests.get(TOP_HEADLINES_URL, params=params)
        else:
            # Use everything endpoint for other languages with simple query 'news'
            params = {
                "q": "news",
                "language": language,
                "apiKey": API_KEY,
                "pageSize": 5,
                "sortBy": "relevancy"
            }
            res = requests.get(EVERYTHING_URL, params=params)

        data = res.json()
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            if not articles:
                return [f"⚠️ No news found for selected options."]
            return [a["title"] for a in articles]
        else:
            return [f"⚠️ {data.get('message', 'Error fetching news')}"]
    except Exception as e:
        return [f"⚠️ Error: {e}"]

def match_voice(lang_code):
    """Try to find a voice matching the language code; fallback to default."""
    voices = engine.getProperty('voices')
    lang_code = lang_code.lower()
    for v in voices:
        # v.languages can be bytes or string list, decode if needed
        langs = []
        for lang in v.languages:
            if isinstance(lang, bytes):
                langs.append(lang.decode().lower())
            else:
                langs.append(str(lang).lower())
        # Match exact or partial language code in voice languages
        if any(lang_code in l for l in langs):
            engine.setProperty('voice', v.id)
            return
    # fallback
    engine.setProperty('voice', voices[0].id)

def read_news_thread():
    """Run reading news in a separate thread to avoid blocking UI."""
    read_button.configure(state="disabled")
    headlines = get_news(category_option.get(), LANGUAGES[language_option.get()])

    news_box.configure(state="normal")
    news_box.delete("1.0", "end")
    global latest_news
    latest_news = []
    for i, h in enumerate(headlines, 1):
        line = f"{i}. {h}\n\n"
        news_box.insert("end", line)
        latest_news.append(line)
    news_box.configure(state="disabled")

    match_voice(LANGUAGES[language_option.get()])

    for h in headlines:
        engine.say(h)
    engine.runAndWait()
    read_button.configure(state="normal")

def read_news():
    """Start news reading in a thread to keep UI responsive."""
    threading.Thread(target=read_news_thread, daemon=True).start()

def export_to_pdf():
    if not latest_news:
        return
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="EchoNews Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    for line in latest_news:
        pdf.multi_cell(0, 10, txt=line)
    pdf.output("echonews_report.pdf")

def toggle_mode():
    global current_mode
    current_mode = "dark" if current_mode == "light" else "light"
    ctk.set_appearance_mode(current_mode)
    mode_switch.configure(text="🌗 Dark" if current_mode == "light" else "☀️ Light")

# ---------- UI Setup ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📰 EchoNews - Multilingual AI Voice News Reader")
app.geometry("760x600")
app.resizable(False, False)

header_font = ctk.CTkFont(family="Segoe UI", size=26, weight="bold")
text_font = ctk.CTkFont(family="Segoe UI", size=14)

# Header
header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(pady=(15, 5), fill="x", padx=20)

title_label = ctk.CTkLabel(header_frame, text="EchoNews", font=header_font)
title_label.pack(side="left")

mode_switch = ctk.CTkButton(header_frame, text="🌗 Dark", command=toggle_mode, width=90)
mode_switch.pack(side="right")

# Category + Language
selector_frame = ctk.CTkFrame(app, fg_color="transparent")
selector_frame.pack(pady=(5, 5))

category_option = ctk.CTkOptionMenu(selector_frame, values=CATEGORIES, font=text_font, width=250)
category_option.set(CATEGORIES[0])
category_option.pack(side="left", padx=10)

language_option = ctk.CTkOptionMenu(selector_frame, values=list(LANGUAGES.keys()), font=text_font, width=200)
language_option.set("English")
language_option.pack(side="left", padx=10)

# Buttons
read_button = ctk.CTkButton(app, text="🎧 Read Top 5 Headlines", font=text_font, command=read_news, width=300)
read_button.pack(pady=(10, 10))

news_box = ctk.CTkTextbox(app, width=720, height=280, font=text_font, wrap="word")
news_box.pack(pady=10)
news_box.configure(state="disabled")

pdf_button = ctk.CTkButton(app, text="📄 Export to PDF", font=text_font, command=export_to_pdf, width=300)
pdf_button.pack(pady=(5, 15))

footer = ctk.CTkLabel(app, text="EchoNews • Built with ❤ by Aastha", font=("Segoe UI", 11, "italic"))
footer.pack(side="bottom", pady=5)

app.mainloop()
