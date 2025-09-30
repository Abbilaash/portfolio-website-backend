from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import logging
import dotenv
from email_template import get_email_template

dotenv.load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 465,  # SSL port
    'sender_email': os.getenv('SMTP_MAIL_ID'),  # Updated to match your env variable
    'sender_password': os.getenv('SMTP_MAIL_PASSWORD'),  # Updated to match your env variable
    'recipient_email': os.getenv('RECIPIENT_EMAIL')
}

def send_email(name, email, message):
    """
    Send email using SMTP SSL with HTML template
    """
    try:
        # Debug: Check email configuration
        logger.info("=== EMAIL CONFIGURATION DEBUG ===")
        logger.info(f"SMTP Server: {EMAIL_CONFIG['smtp_server']}")
        logger.info(f"SMTP Port: {EMAIL_CONFIG['smtp_port']}")
        logger.info(f"Sender Email: {EMAIL_CONFIG['sender_email']}")
        logger.info(f"Recipient Email: {EMAIL_CONFIG['recipient_email']}")
        logger.info(f"Password Set: {'Yes' if EMAIL_CONFIG['sender_password'] else 'No'}")
        
        # Validate email configuration
        if not EMAIL_CONFIG['sender_email']:
            logger.error("SMTP_MAIL_ID (sender email) not set in environment variables")
            return False
        
        if not EMAIL_CONFIG['sender_password']:
            logger.error("SMTP_MAIL_PASSWORD not set in environment variables")
            return False
        
        if not EMAIL_CONFIG['recipient_email']:
            logger.error("RECIPIENT_EMAIL not set in environment variables")
            return False
        
        logger.info("Starting email sending process...")
        
        # Create message container
        msg = MIMEMultipart()
        msg['Subject'] = f"Portfolio Contact Form - Message from {name}"
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['recipient_email']
        
        # Get HTML email template
        html_content = get_email_template(name, email, message)
        msg.attach(MIMEText(html_content, 'html'))
        
        logger.info("Attempting to connect to Gmail SMTP SSL server...")
        
        # Send email using SSL connection (like your sample)
        server = smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        logger.info("Connected to SMTP SSL server successfully")
        
        logger.info("Attempting to login...")
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        logger.info("Login successful")
        
        logger.info("Sending email...")
        server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['recipient_email'], msg.as_string())
        logger.info("Email sent successfully")
        
        server.quit()
        logger.info(f"Email sent successfully from {email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication Error: {str(e)}")
        logger.error("This usually means:")
        logger.error("1. Incorrect email or password")
        logger.error("2. 2-Factor Authentication is enabled but App Password not used")
        logger.error("3. 'Less secure app access' is disabled (for older Gmail accounts)")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP Error: {str(e)}")
        return False
    except ConnectionRefusedError as e:
        logger.error(f"Connection Refused Error: {str(e)}")
        logger.error("This usually means:")
        logger.error("1. Firewall is blocking the connection")
        logger.error("2. Antivirus software is blocking SMTP")
        logger.error("3. ISP is blocking port 465")
        logger.error("4. Network connectivity issues")
        return False
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        return False

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        # Validate fields
        if not name or not email or not message:
            return jsonify({
                'success': False,
                'message': 'All fields (name, email, message) are required'
            }), 400
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'message': 'Please provide a valid email address'
            }), 400
        
        # Send email
        if send_email(name, email, message):
            return jsonify({
                'success': True,
                'message': 'Message sent successfully! I\'ll get back to you soon.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send message. Please try again or contact me directly.'
            }), 500
            
    except Exception as e:
        logger.error(f"Error in contact endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/email-config-check', methods=['GET'])
def email_config_check():
    """
    Check email configuration status
    """
    config_status = {
        'smtp_server': EMAIL_CONFIG['smtp_server'],
        'smtp_port': EMAIL_CONFIG['smtp_port'],
        'sender_email_set': bool(EMAIL_CONFIG['sender_email']),
        'sender_password_set': bool(EMAIL_CONFIG['sender_password']),
        'recipient_email_set': bool(EMAIL_CONFIG['recipient_email']),
        'sender_email': EMAIL_CONFIG['sender_email'] if EMAIL_CONFIG['sender_email'] else 'Not set',
        'recipient_email': EMAIL_CONFIG['recipient_email'] if EMAIL_CONFIG['recipient_email'] else 'Not set'
    }
    
    all_configured = all([
        EMAIL_CONFIG['sender_email'],
        EMAIL_CONFIG['sender_password'],
        EMAIL_CONFIG['recipient_email']
    ])
    
    return jsonify({
        'configured': all_configured,
        'config': config_status,
        'message': 'Email configuration is complete' if all_configured else 'Email configuration incomplete'
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    Root endpoint
    """
    return jsonify({
        'message': 'Portfolio Backend API',
        'version': '1.0.0',
        'endpoints': {
            'contact': '/api/contact (POST)',
            'health': '/api/health (GET)'
        }
    }), 200

if __name__ == '__main__':
    # Check for environment variables (keeping both old and new variable names for compatibility)
    if 'SMTP_MAIL_ID' in os.environ:
        EMAIL_CONFIG['sender_email'] = os.environ['SMTP_MAIL_ID']
    elif 'SENDER_EMAIL' in os.environ:
        EMAIL_CONFIG['sender_email'] = os.environ['SENDER_EMAIL']
    
    if 'SMTP_MAIL_PASSWORD' in os.environ:
        EMAIL_CONFIG['sender_password'] = os.environ['SMTP_MAIL_PASSWORD']
    elif 'SENDER_PASSWORD' in os.environ:
        EMAIL_CONFIG['sender_password'] = os.environ['SENDER_PASSWORD']
    
    if 'RECIPIENT_EMAIL' in os.environ:
        EMAIL_CONFIG['recipient_email'] = os.environ['RECIPIENT_EMAIL']
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
