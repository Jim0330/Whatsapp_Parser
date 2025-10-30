# Whatsapp_Parser

## Overview
This project is a Flask-based Resume Extraction System that automates the process of identifying and extracting essential details such as name, email, and phone number from resumes sent via WhatsApp.

It integrates Twilio’s WhatsApp API and Google APIs to handle end-to-end automation:
- Users upload resumes directly through WhatsApp.
- The system extracts information using Regex and NLP (spaCy).
- Extracted data is stored in Google Sheets, and files are saved in Google Drive.
- The extracted details are also sent back to the user as a WhatsApp confirmation message.

---

## Features
- Upload resumes directly through WhatsApp  
- Extracts name, email ID, and phone number using Regex and NLP  
- Supports PDF and DOCX resume formats  
- Saves structured data to Google Sheets  
- Uploads original files automatically to Google Drive  
- Sends extracted information instantly to users via Twilio WhatsApp API  

---

## Tools and Technologies
| Component | Technology |
|------------|-------------|
| Language | Python |
| Framework | Flask |
| Text Extraction | pdfplumber, docx2txt |
| NLP & Regex | spaCy, Regular Expressions |
| Phone Number Parsing | phonenumbers |
| Messaging | Twilio WhatsApp API |
| Cloud Integration | Google Drive API, Google Sheets API |
| Environment Management | python-dotenv |

---

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/whatsapp_resume_parser.git
cd whatsapp_resume_parser
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
.\.venv\Scripts\activate      # For Windows
# OR
source .venv/bin/activate     # For Mac/Linux
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Configuration Files
Ensure the following configuration files are present in the project directory:
- `credentials.json` → Google API credentials  
- `service_account.json` → Service account key for Sheets/Drive  
- `.env` → Environment variables for Twilio and Google API setup  

Example `.env` file:
```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
GOOGLE_SHEET_ID=your_google_sheet_id
```

---

## Running the Application

### Step 1: Start the Flask App
```bash
python app.py
```

### Step 2: Connect via ngrok
In a new terminal window, run:
```bash
ngrok http 5000
```

Copy the generated forwarding URL (for example: `https://abcd1234.ngrok.io`) and paste it into your Twilio Sandbox under Webhook Configuration for receiving messages.

### Step 3: Send a Resume via WhatsApp
1. Open your Twilio WhatsApp sandbox chat.  
2. Send a PDF or DOCX resume file.  
3. The Flask backend will:
   - Extract name, email ID, and phone number.  
   - Save the extracted details in Google Sheets.  
   - Upload the original resume to Google Drive.  
   - Send a confirmation message back to the user via WhatsApp.

---

## Output and Results
- Resume data extracted automatically.  
- Structured data stored in Google Sheets.  
- Original resume saved in Google Drive.  
- Real-time confirmation message sent to the user via WhatsApp.  

---

## Demo Screenshots
![twilio](https://github.com/user-attachments/assets/d10d7489-229f-4453-90d7-72d7be22ed95)
Figure 1: Resume uploaded via WhatsApp  


<img width="1702" height="437" alt="googlesheets" src="https://github.com/user-attachments/assets/28be823b-c5c7-4c7b-ab41-8e21d3f9d29b" />
Figure 2: Extracted details stored automatically in Google Sheets  

---

## Author
**Ashitha P**  
Email: [pallathashitha@gmail.com](mailto:pallathashitha@gmail.com)  
Developed as part of an intelligent automation workflow using NLP, Flask, Twilio, and Google Cloud APIs.  
````

