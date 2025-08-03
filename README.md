# VigilantEye - Drug Detection Telegram Bot 🚨
A Telegram Bot that detects drug-related content in Telegram channels using keyword-based analysis and machine learning. Integrated with a Flask-powered admin dashboard for real-time tracking, this project aims to assist law enforcement in monitoring illegal activities on Telegram.

# 🔍 Features
- Telegram Bot for Drug Detection
- Scans Telegram channels for drug-related keywords.
- Uses ML classification for descriptive text.
- Fetches channel profile pictures.
- Logs findings with detected keywords, probability score & timestamps.
- Google Cloud Storage Integration
- Uploads & stores images in GCS Buckets.
- Flask Web Dashboard
- Admin login authentication.
- Displays scanned channels/messages.
- Visual interface for investigation data.
- ML Model Fine-Tuning Script (BERT-based)

# 🛠 Tech Stack
- Python
- TeleBot (pyTelegramBotAPI)
- Flask
- Google Cloud Storage
- Transformers (HuggingFace BERT)
- Tailwind CSS (Web UI)

# 📂 Project Structure
csharp
Copy
Edit
VigilantEye-DrugDetectionBot/
│
├── bot/                    # Telegram Bot Code
│   ├── bot_main.py
│   ├── ml_model.py
│   ├── extract_words.py
│   └── __init__.py
│
├── web/                    # Flask Web Dashboard
│   ├── app.py
│   ├── static/
│   │   └── main.js
│   └── templates/
│       ├── login.html
│       └── dashboard.html
│
├── model_training/         # BERT Fine-tuning Script
│   └── fine_tune.py
│
├── requirements.txt
├── .gitignore
└── README.md

# 🚀 Setup Instructions
1. Clone the Repository:

bash : 
git clone https://github.com/MahinHaqqani/VigilantEye-Drug-Detection-Bot-.git
cd VigilantEye-Drug-Detection-Bot-

2. Install Python Dependencies:

bash : 
pip install -r requirements.txt

3. Configure Environment Variables (.env file):

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/gcp-key.json
GCS_BUCKET_NAME=your-gcs-bucket-name
SECRET_KEY=your_flask_secret_key

4. Run the Telegram Bot:

bash : 
cd bot
python bot_main.py

5. Run the Flask Dashboard:

bash :
cd web
python app.py

# 🤝 Contributions
Pull requests are welcome.



