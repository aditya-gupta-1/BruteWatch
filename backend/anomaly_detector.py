import sqlite3
from datetime import datetime
import os
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Track failed attempts per IP
failed_attempts = defaultdict(list)

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'database.db')

# Email configuration (replace these values)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "adityag20044@gmail.com"
SENDER_PASSWORD = "jolw ugtd ginh ardf"
RECIPIENT_EMAIL = "adityag20044@example.com"

def init_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    description TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

def send_email_alert(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Email alert sent.")
    except Exception as e:
        print("❌ Failed to send email:", str(e))

def detect_anomalies(log_lines):
    for line in log_lines:
        if "LOGIN_FAILED" in line and "ip=" in line:
            ip = line.split("ip=")[1].strip()
            failed_attempts[ip].append(line.strip())

            if len(failed_attempts[ip]) == 3:
                message = f"3 or more failed logins detected from IP {ip}."
                store_incident("Brute-force Attempt", message)
                send_email_alert("🚨 Brute-force Attempt Detected", message)

def store_incident(incident_type, description):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO incidents (type, description, timestamp) VALUES (?, ?, ?)",
                (incident_type, description.strip(), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    print(f"✅ Stored incident: {description.strip()}")
