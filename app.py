from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

GMAIL_USER = "abdullahtariq.nns.966@gmail.com"
GMAIL_APP_PASSWORD = "lywt fzjj xwfy mqfo"  # Use a Gmail App Password

@app.route('/')
def home():
    return '✅ Flask SMTP API is live!'

@app.route('/send-facility-email/', methods=['POST'])
def send_facility_email():
    try:
        data = request.get_json(force=True)
        print("📨 Received payload:", data)

        recipients = data.get('recipients')
        facilities = data.get('facilities')  # Now expecting a list of facilities
        event = data.get('event')

        if not recipients or not isinstance(recipients, list) or not facilities or not isinstance(facilities, list) or not event:
            return jsonify({'status': 'error', 'message': 'Missing or invalid fields'}), 400

        subject = f"Facilities Approved for {event}"
        facilities_str = ', '.join(facilities)
        body = f'The following facilities have been approved for event "{event}": {facilities_str}. Please prepare accordingly.'

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)

            for to in recipients:
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = GMAIL_USER
                msg["To"] = to
                msg.set_content(body)
                try:
                    server.send_message(msg)
                    print(f"✅ Email sent to {to}")
                except Exception as e:
                    print(f"❌ Failed to send to {to}: {e}")

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print("🔥 Exception occurred:", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)