# ⚡ Discord ID Resolver Pro

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord.py"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
</p>

<p align="center">
  <b>Convert raw Discord IDs into real user identities. Fast. Secure. Unlimited.</b>
</p>

---

## 📸 Preview

<p align="center">
  <img src="Discord_Username_SearchByID.webp" alt="Discord ID Resolver Pro - Main Screen" width="700"/>
</p>

---

## ✨ Features

- 🔍 **Bulk ID Resolution** — Process multiple Discord IDs at once, just paste them line by line
- 👤 **User Profile Retrieval** — Fetch username, display name, avatar, and account creation date
- 📊 **Interactive Data Table** — View results in a clean, sortable table with avatar previews
- 📥 **CSV Export** — Download resolved data as a CSV file for further analysis
- 🎨 **Modern UI** — Sleek dark theme with glassmorphism effects and smooth animations
- ⚡ **Rate Limit Safe** — Built-in delay mechanism to respect Discord API limits

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A Discord Bot Token (with proper intents enabled)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Discord-Username_SearchByID.git
   cd Discord-Username_SearchByID
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Discord Bot Token**
   
   Create a file at `.streamlit/secrets.toml` with the following content:
   ```toml
   [discord]
   token = "YOUR_DISCORD_BOT_TOKEN_HERE"
   ```

   > [!IMPORTANT]
   > Make sure your Discord Bot has the **Server Members Intent** enabled in the Discord Developer Portal.

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## 📖 Usage

1. Launch the application using `streamlit run app.py`
2. Paste Discord User IDs into the text area (one per line)
3. Click **INICIAR** to start the resolution process
4. View results in the interactive table
5. Download the data as CSV if needed

### Example Input
```
262745192195624256
892347238442389400
123456789012345678
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web interface & interactivity |
| **Discord.py** | Discord API integration |
| **Pandas** | Data manipulation & CSV export |
| **Python** | Core programming language |

---

## 📁 Project Structure

```
Discord-Username_SearchByID/
├── .streamlit/
│   └── secrets.toml       # Discord bot token (not tracked by git)
├── app.py                 # Main application (Pro version)
├── id_lookup.py           # Single ID lookup utility
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

---

## ⚠️ Disclaimer

This tool is intended for educational and legitimate purposes only. Always respect Discord's [Terms of Service](https://discord.com/terms) and [Developer Policy](https://discord.com/developers/docs/policies-and-agreements/developer-policy) when using this application.

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <i>Powered by Streamlit & Discord API</i>
</p>
