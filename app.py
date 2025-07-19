import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Mail Configuration
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
    try:
        data = request.get_json(force=True)
        providers = data.get('providers', [])
        event_title = data.get('event_title', 'No Title')
        venue = data.get('venue', 'No Venue')

        if not providers:
            return jsonify({'error': 'No providers received'}), 400

        # Track results
        results = []

        for provider in providers:
            name = provider.get('providerName')
            email = provider.get('providerEmail')
            facility = provider.get('facilityName')

            if not email or not name or not facility:
                results.append({'email': email, 'status': 'skipped - missing data'})
                continue

            body = (
                f"Dear {name},\n\n"
                f"You have been assigned as the facility provider for:\n\n"
                f"Event: {event_title}\n"
                f"Venue: {venue}\n"
                f"Facility: {facility}\n\n"
                f"Please make necessary arrangements.\n\n"
                f"Thank you!"
            )

            try:
                msg = Message(subject=f"Facility Assignment - {event_title}",
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[email],
                              body=body)
                mail.send(msg)
                results.append({'email': email, 'status': 'sent'})
            except Exception as e:
                results.append({'email': email, 'status': f'error - {str(e)}'})

        return jsonify({'results': results}), 200

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
