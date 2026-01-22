# Zabbix AI Agent 🤖

An advanced, "Active" AI Agent fully integrated into **Zabbix 7.0+**. This agent transforms Zabbix from a monitoring tool into an intelligent operations partner.

![Zabbix AI Agent](https://pbs.twimg.com/media/Gb_j8uOWMAA_yv_.jpg) 
*(Example Screenshot)*

## 🚀 Features

### 1. 💬 Embedded AI Chat Interface
A floating chat interface living inside your Zabbix dashboard.
- **Multi-LLM Support**: Choose between **AWS Bedrock (Claude)**, **OpenAI (GPT-4)**, or **Google Gemini**.
- **SRE Persona**: The AI acts as a Senior Site Reliability Engineer, offering diagnostics, root cause analysis, and command suggestions.
- **Persistent History**: Chat history is saved locally so you don't lose context.

### 2. 🛠️ Active "Agentic" Capabilities
The AI isn't just a chatbot; it can **execute actions** in Zabbix:
- **Create Hosts**: "Create a new Linux host at 192.168.1.50". The AI will interview you for details (OS, Templates, Interface).
- **Acknowledge Problems**: "Ack the high CPU alert on DB-Server".
- **Schedule Maintenance**: "Put Web-01 in maintenance for 30 mins".
- **Enable/Disable Hosts**: "Disable monitoring for the testing server".

### 3. 🧠 Contextual Analysis
Right-click on **ANY** row in Zabbix (Latest Data, Problems, Hosts) and select:
**`🤖 Analizar con IA`**

The AI will treat the row content as context and provide an immediate analysis of the metrics or errors found.

### 4. 📊 Daily AI Summary
A dedicated dashboard page providing a synthesized report of your infrastructure's health, separating signal from noise.

---

## 📦 Installation

### Prerequisites
- Zabbix Server 6.0 or 7.0+ (Tested on 7.0 LTS).
- Python 3.10+.
- Node.js & npm (for building the frontend).
- A web server (Apache/Nginx) handling Zabbix.

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/zabbix-ai-agent.git
cd zabbix-ai-agent
```

### 2. Backend Setup (Python/FastAPI)
The backend acts as the bridge between the AI Providers and the Zabbix API.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Configuration**:
Create a `.env` file in `backend/` based on `.env.example`:
```ini
# Only if using Bedrock via direct keys (optional, can use Config UI)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# Zabbix Creds (Used by the agent to perform actions)
ZABBIX_URL=http://127.0.0.1/zabbix
ZABBIX_USER=Admin
ZABBIX_PASSWORD=zabbix
ZABBIX_VERIFY_SSL=False
```

**Run the Service**:
It is recommended to run this as a systemd service.
```bash
# Edit zabbix-ai-backend.service paths to match your install
sudo cp ../zabbix-ai-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now zabbix-ai-backend
```

### 3. Frontend Setup (React/Vite)
The frontend is the chat interface.

```bash
cd frontend
npm install
npm run build
```

This will generate the static files in `backend/static/app`, which the Python backend serves.

### 4. Zabbix Module Setup
This injects the JavaScript and UI elements into Zabbix.

1. Copy the `zabbix_module/zabbix_ai_agent` folder to your Zabbix server's `modules` directory (usually `/usr/share/zabbix/modules/`).
2. Go to **Administration -> General -> Modules** in Zabbix.
3. Click **Scan directory**.
4. Enable the **Zabbix AI Agent** module.

### 5. Web Server Proxy (Apache)
To avoid CORS issues, configure a proxy in Apache so `/ai-backend` points to the Python service running on port 8000.
**Ensure proxy modules are enabled:**
```bash
sudo a2enmod proxy proxy_http
sudo systemctl restart apache2
```

Create `/etc/apache2/conf-enabled/zabbix-ai-backend.conf`:
```apache
<Location "/ai-backend">
    ProxyPass http://localhost:8000
    ProxyPassReverse http://localhost:8000
</Location>
```
Restart Apache: `sudo systemctl restart apache2`.

---

## ⚙️ Configuration

1. Open Zabbix.
2. Open the AI Chat (bottom right).
3. Click the **Gear Icon (⚙️)** in the chat header.
4. Select your AI Provider (**Bedrock**, **OpenAI**, **Gemini**) and enter your API Keys.
5. Click **Save Configuration**.

---

## 🛡️ Architecture
- **Frontend**: React + Vite (Embedded via IFrame + Zabbix Modules).
- **Backend**: FastAPI (Python). Uses `pyzabbix` to talk to Zabbix and `boto3`/`openai`/`google-generativeai` for LLMs.
- **Integration**: JavaScript injected into Zabbix pages listens for right-clicks and creates context menus.

## 🤝 Contributing
Pull requests are welcome! Please open an issue to discuss proposed changes.

## 📄 License
MIT
