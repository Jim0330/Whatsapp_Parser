import os
import re
import spacy
import requests
import pdfplumber
import docx2txt
import phonenumbers  
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from nameparser import HumanName
from google_sheets import append_row
from google_drive import upload_to_drive

# ---------------------- ENV SETUP ----------------------
load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
HEADING_WORDS = {"resume", "curriculum", "vitae", "professional", "summary", "objective", "profile", "experience", "education", "skills"}


# ---------------------- HELPERS ----------------------
def extract_phone_numbers(text):
    """Use Google's phonenumbers library to extract valid mobile numbers."""
    numbers = []
    for match in phonenumbers.PhoneNumberMatcher(text, "IN"):  # 'IN' = India default
        num = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
        numbers.append(num)
    return list(set(numbers))  # remove duplicates


def extract_basic(text):
    """Extract full name, email, and phone robustly."""
    emails = EMAIL_RE.findall(text)
    phones = extract_phone_numbers(text)
    name = None

    # 1️ Explicit "Name:" or "Full Name:"
    match = re.search(r'(?i)(?:full\s*name|name)\s*[:\-]\s*([A-Za-z][A-Za-z\s\-]+)', text)
    if match:
        name = match.group(1).strip()

    # 2️ Try top few lines — name usually appears early
    if not name or len(name.split()) < 2:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines[:10]:
            if any(word in line.lower() for word in HEADING_WORDS):
                continue
            if EMAIL_RE.search(line) or extract_phone_numbers(line):
                continue
            if not any(char.isdigit() for char in line):
                parsed = HumanName(line)
                if parsed.first and parsed.last:
                    name = str(parsed)
                    break
                elif len(line.split()) <= 3:
                    name = line
                    break

    # 3️ Fallback: spaCy PERSON entities
    if not name:
        doc = nlp(text)
        names = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
        if names:
            name = next((n for n in names if len(n.split()) >= 2), names[0])

    # 4️ Fallback: email-based
    if (not name or len(name.split()) < 2) and emails:
        local = re.sub(r'[\d\._\-]+', ' ', emails[0].split("@")[0])
        name = " ".join(w.capitalize() for w in local.split())

    return (name or "Unknown").strip(), emails, phones

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text


def extract_text_from_docx(file_path):
    return docx2txt.process(file_path).strip()


# ---------------------- ROUTES ----------------------
@app.route("/")
def home():
    return "WhatsApp Resume Parser is running!"


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    from_number = request.values.get("From", "")
    body = request.values.get("Body", "").strip()
    media_url = request.values.get("MediaUrl0")
    media_type = request.values.get("MediaContentType0")

    text_content = body
    drive_link = ""

    if media_url:
        print(f"Received file: {media_url} ({media_type})")
        file_path = None
        if "pdf" in media_type:
            file_path = "resume.pdf"
        elif "docx" in media_type or "word" in media_type:
            file_path = "resume.docx"

        if file_path:
            r = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
            if r.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(r.content)
                print("File downloaded successfully ")
            else:
                print("Failed to download file:", r.status_code)
                return Response(str(MessagingResponse().message("Failed to download your resume. Please try again.")), mimetype="application/xml")

            try:
                drive_link = upload_to_drive(file_path, DRIVE_FOLDER_ID)
            except Exception as e:
                print("Drive upload error:", e)

            if file_path.endswith(".pdf"):
                text_content = extract_text_from_pdf(file_path)
            elif file_path.endswith(".docx"):
                text_content = extract_text_from_docx(file_path)

    # Extract structured info
    name, emails, phones = extract_basic(text_content)
    print("EXTRACTED ->", name, emails, phones)

    # Save to Google Sheet
    row = [from_number, name, ",".join(emails), ",".join(phones), text_content[:200], drive_link]
    try:
        append_row(SPREADSHEET_ID, row)
    except Exception as e:
        print("Sheet error:", e)

    # WhatsApp reply
    resp = MessagingResponse()
    msg = f"Got your resume!\nName: {name}\nEmail: {','.join(emails) or 'N/A'}\nPhone: {','.join(phones) or 'N/A'}\nSaved to Drive 📂"
    resp.message(msg)
    return Response(str(resp), mimetype="application/xml")


if __name__ == "__main__":
    app.run(port=5000, debug=True)

