# 📰 EchoNews - Multilingual AI Voice News Reader
---
## 📱 Overview

**EchoNews** is a modern, AI-powered mobile news application built using **Flutter**, inspired by the original desktop app in Python. It fetches live news, speaks it out loud using text-to-speech, supports multiple languages, and can export news to PDF — all with a beautiful UI.
---
## ✨ Features

- 🌐 **Multilingual news** (English, Hindi, French, Spanish, German)
- 📰 **Top 5 latest headlines** in various categories (general, technology, business, sports, science, health, entertainment)
- 🎧 **Text-to-speech** to read news aloud
- 📄 **Export news to PDF**
- 🌗 **Dark and light modes**
- 💙 Custom branding and logo support
---

## 🚀 Getting Started

### Prerequisites

- Flutter SDK (3.x recommended)
- Dart SDK (comes with Flutter)
- Android Studio or VS Code
- A NewsAPI key (get it free from [NewsAPI.org](https://newsapi.org))

---

### Installation

1️⃣ **Clone the repository**

```bash
git clone https://github.com/your-username/echonews-flutter.git
cd echonews-flutter
2️⃣ Add your NewsAPI key

In lib/main.dart, replace:

final String apiKey = 'YOUR_NEWSAPI_KEY';
with your actual API key.

3️⃣ Add your logo

Place your logo image in assets/logo.png.

Update pubspec.yaml:

yaml
flutter:
  assets:
    - assets/logo.png
Then run:
flutter pub get

4️⃣ Run the app
flutter run

📄 Export PDF
Click Export PDF button in the app.

Generated PDF will be saved in your device’s storage folder (e.g., Downloads or app folder).

