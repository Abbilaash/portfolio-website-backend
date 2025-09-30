# Portfolio Backend

Flask backend for the portfolio website contact form with SMTP email functionality.

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Email Settings

1. Copy `.env.example` to `.env`
2. Update the email configuration:
   - `SENDER_EMAIL`: Your Gmail address
   - `SENDER_PASSWORD`: Your Gmail App Password (not regular password)
   - `RECIPIENT_EMAIL`: Email where you want to receive messages

### 3. Gmail App Password Setup

For Gmail users:

1. Go to your Google Account settings
2. Security → 2-Step Verification
3. App passwords → Generate new app password
4. Use this app password in your `.env` file

### 4. Run the Server

```bash
python app.py
```

The server will run on `http://localhost:5000`

## API Endpoints

### POST /api/contact

Send a contact form message

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Hello, I'm interested in your work!"
}
```

### GET /api/health

Health check endpoint

### GET /

API information

## Environment Variables

- `SENDER_EMAIL`: Email address to send from
- `SENDER_PASSWORD`: Email password/app password
- `RECIPIENT_EMAIL`: Email address to receive messages

## Notes

- CORS is enabled for frontend communication
- All emails are sent via Gmail SMTP
- Error handling and logging included
- Basic input validation implemented
