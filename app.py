from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime
import logging
import dotenv

dotenv.load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Google Sheets configuration
GOOGLE_SHEET_CONFIG = {
    'web_app_url': os.getenv('GOOGLE_SHEET_WEB_APP_URL')  # Google Apps Script URL
}

def add_to_google_sheet(name, email, message):
    """
    Add contact form data to Google Sheet using Google Apps Script
    """
    try:
        # Debug: Check Google Sheets configuration
        logger.info("=== GOOGLE SHEETS CONFIGURATION DEBUG ===")
        logger.info(f"Web App URL Set: {'Yes' if GOOGLE_SHEET_CONFIG['web_app_url'] else 'No'}")
        logger.info(f"Web App URL: {GOOGLE_SHEET_CONFIG['web_app_url']}")
        
        # Validate configuration
        if not GOOGLE_SHEET_CONFIG['web_app_url']:
            logger.error("GOOGLE_SHEET_WEB_APP_URL not set in environment variables")
            return False
        
        if 'YOUR_SCRIPT_ID' in GOOGLE_SHEET_CONFIG['web_app_url']:
            logger.error("GOOGLE_SHEET_WEB_APP_URL still contains placeholder. Please update with actual web app URL.")
            return False
        
        logger.info("Starting Google Sheets data submission process...")
        
        # Prepare the data to send to Google Apps Script
        payload = {
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Payload: {payload}")
        logger.info("Attempting to send data to Google Apps Script...")
        
        # Send the data to the Google Apps Script
        response = requests.post(GOOGLE_SHEET_CONFIG['web_app_url'], json=payload, timeout=30)
        
        logger.info(f"Google Apps Script response status code: {response.status_code}")
        logger.info(f"Google Apps Script response text: {response.text}")
        
        # Try to parse the JSON response for more details
        try:
            response_data = response.json()
            logger.info(f"Parsed response data: {response_data}")
            if 'data' in response_data:
                logger.info(f"Response includes data: {response_data['data']}")
        except Exception as json_error:
            logger.warning(f"Could not parse response as JSON: {json_error}")
        
        # Check if the request was successful
        if response.status_code == 200:
            logger.info(f"Data added to Google Sheet successfully from {email}")
            return True
        elif response.status_code == 401:
            logger.error("Unauthorized access to Google Apps Script. This usually means:")
            logger.error("1. The web app URL is incorrect")
            logger.error("2. The Google Apps Script is not deployed as a web app")
            logger.error("3. The web app permissions are set incorrectly")
            logger.error("4. The script ID in the URL doesn't exist")
            return False
        elif response.status_code == 404:
            logger.error("Google Apps Script web app not found. Check if the URL is correct and the script is deployed.")
            return False
        elif response.status_code == 403:
            logger.error("Access denied to Google Apps Script. Check deployment permissions.")
            return False
        elif response.status_code == 500:
            logger.error("Google Apps Script internal error. Check the script for errors.")
            return False
        else:
            logger.error(f"Failed to add data to Google Sheet. Status code: {response.status_code}")
            logger.error(f"Response: {response.text[:500]}...")  # Truncate long responses
            return False
        
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error when connecting to Google Apps Script: {str(e)}")
        return False
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error when connecting to Google Apps Script: {str(e)}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error when connecting to Google Apps Script: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Failed to add data to Google Sheet: {str(e)}")
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
        
        # Add data to Google Sheet
        if add_to_google_sheet(name, email, message):
            return jsonify({
                'success': True,
                'message': 'Message submitted successfully! Your data has been recorded.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to submit message. Please try again or contact me directly.'
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

@app.route('/api/test-sheet-debug', methods=['GET'])
def test_sheet_debug():
    """
    Test Google Sheets connection with detailed debugging
    """
    try:
        # Prepare test data
        payload = {
            'name': 'Debug Test User',
            'email': 'debug@test.com',
            'message': 'This is a debug test message',
            'timestamp': datetime.now().isoformat()
        }
        
        # Send request
        response = requests.post(GOOGLE_SHEET_CONFIG['web_app_url'], json=payload, timeout=30)
        
        # Parse response
        try:
            response_data = response.json()
        except:
            response_data = {"error": "Could not parse JSON", "raw_text": response.text}
        
        return jsonify({
            'success': response.status_code == 200,
            'status_code': response.status_code,
            'response_data': response_data,
            'payload_sent': payload,
            'url_used': GOOGLE_SHEET_CONFIG['web_app_url']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@app.route('/api/test-sheet', methods=['GET'])
def test_sheet():
    """
    Test Google Sheets connection
    """
    try:
        result = add_to_google_sheet("Test User", "test@example.com", "This is a test message")
        if result:
            return jsonify({
                'success': True,
                'message': 'Google Sheets connection successful!'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Google Sheets connection failed. Check logs for details.'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error testing Google Sheets: {str(e)}'
        }), 500

@app.route('/api/config-check', methods=['GET'])
def config_check():
    """
    Check Google Sheets configuration status
    """
    config_status = {
        'google_sheet_url_set': bool(GOOGLE_SHEET_CONFIG['web_app_url']),
        'web_app_url': GOOGLE_SHEET_CONFIG['web_app_url'] if GOOGLE_SHEET_CONFIG['web_app_url'] else 'Not set'
    }
    
    all_configured = bool(GOOGLE_SHEET_CONFIG['web_app_url'])
    
    return jsonify({
        'configured': all_configured,
        'config': config_status,
        'message': 'Google Sheets configuration is complete' if all_configured else 'Google Sheets configuration incomplete'
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    Root endpoint
    """
    return jsonify({
        'message': 'Portfolio Backend API - Google Sheets Integration',
        'version': '2.0.0',
        'endpoints': {
            'contact': '/api/contact (POST)',
            'health': '/api/health (GET)',
            'config-check': '/api/config-check (GET)',
            'test-sheet': '/api/test-sheet (GET)',
            'test-sheet-debug': '/api/test-sheet-debug (GET)'
        }
    }), 200

if __name__ == '__main__':
    # Check for environment variables
    if 'GOOGLE_SHEET_WEB_APP_URL' in os.environ:
        GOOGLE_SHEET_CONFIG['web_app_url'] = os.environ['GOOGLE_SHEET_WEB_APP_URL']
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
