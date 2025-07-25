from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

GMAIL_USER = "abdullahtariq.nns.966@gmail.com"
GMAIL_APP_PASSWORD = "lywt fzjj xwfy mqfo"  # Keep this secure!

@app.route('/send-facility-email/', methods=['POST'])
def send_facility_email():
    try:
        data = request.get_json(force=True)
        print("📨 Received payload:", data)

        event_title = data.get('event_title')
        venue = data.get('venue')
        providers = data.get('providers')

        if not event_title or not venue or not isinstance(providers, list) or providers.isEmpty:
            return jsonify({'status': 'error', 'message': 'Missing or invalid fields'}), 400

        subject = f"Facility Assignment - {event_title}"

        results = []
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)

            for p in providers:
                to = p.get('providerEmail')
                name = p.get('providerName')
                facility = p.get('facilityName')

                if not to or not name or not facility:
                    results.append({'email': to, 'status': 'skipped - missing info'})
                    continue

                body = (
                    f"Dear {name},\n\n"
                    f"You have been assigned the facility:\n"
                    f"- Facility: {facility}\n"
                    f"- Event: {event_title}\n"
                    f"- Venue: {venue}\n\n"
                    "Please make the necessary arrangements.\n\nThank you!"
                )
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = GMAIL_USER
                msg["To"] = to
                msg.set_content(body)

                try:
                    server.send_message(msg)
                    results.append({'email': to, 'status': 'sent'})
                except Exception as ex:
                    results.append({'email': to, 'status': f'error – {ex}'})

        return jsonify({'status': 'success', 'results': results}), 200

    except Exception as e:
        print("🔥 Internal error:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def home():
    return "✅ Flask SMTP API is live!"

if __name__ == '__main__':
    app.run(debug=True)
