
# ⚾ MLB Betting Model

A Python-based console application that scrapes live MLB player prop lines from sportsbooks, evaluates expected value (EV), and automates positive EV bets syncing to Google Sheets. Designed for bettors who want a data-driven edge.

---

## 📊 Features

- ✅ **Live EV prop scanning** (only shows EV > 0)
- ✅ **Google Sheets syncing** for daily tracking
- ✅ **Email alerts** on sync failure or success
- ✅ **Bankroll & ROI tracking** with CSV log
- ✅ **Cross-platform** (Windows & Mac)

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Neemato/mlb-betting-model.git
cd mlb-betting-model
```

### 2. Create Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your `credentials.json` File

Place your **Google Sheets API key** (from your GCP project) into the root of the folder as `credentials.json`. This file is `.gitignore`-protected.

---

## 🚀 Running the Model

```bash
python daily_runner.py
```

This script:
- Runs your prop model
- Filters for EV > 0 props
- Syncs to Google Sheets
- Logs results to CSV
- Sends email status updates

---

## 📅 Automate with Scheduler (Optional)

### Windows Task Scheduler
- Schedule `daily_runner.py` to run daily

### Mac/Linux (cron)
```bash
crontab -e
0 9 * * * /path/to/venv/bin/python /path/to/mlb-betting-model/daily_runner.py
```

---

## 🔐 Security & Best Practices

- Never push `credentials.json` to GitHub
- Use environment variables or `config.yaml` for email credentials
- Review GitHub's [Secret Scanning Protection](https://docs.github.com/en/code-security)

---

## 🙌 Credits & License

Created by **Neemato** — with guidance from ChatGPT & the sports analytics community.  
MIT License.
