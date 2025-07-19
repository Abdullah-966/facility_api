import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS') == 'True',
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL') == 'True',
)

mail = Mail(app)

@app.route('/api/send-facility-provider', methods=['POST'])
def send_facility_provider():
    data = request.get_json(force=True)
    providers = data.get('providers')
    recipient = data.get('email')
    if not providers or not recipient:
        return jsonify({'error': 'Missing providers list or email'}), 400

    # Format provider list
    body = "Facility Providers:\n\n"
    body += "\n".join(f"- {p['name']}: {p['details']}" for p in providers)

    msg = Message(subject="Facility Providers",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[recipient],
                  body=body)
    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
