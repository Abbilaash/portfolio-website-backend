from datetime import datetime

def get_email_template(name, email, message):
    """
    Generate HTML email template with Bootstrap styling
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portfolio Contact Form</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }}
            .content {{
                padding: 30px;
            }}
            .info-card {{
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
            .message-box {{
                background: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }}
            .footer {{
                background: #343a40;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 0 0 10px 10px;
                font-size: 14px;
            }}
            .btn-reply {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 25px;
                text-decoration: none;
                display: inline-block;
                margin: 15px 0;
                font-weight: 600;
            }}
            .btn-reply:hover {{
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            .timestamp {{
                color: #6c757d;
                font-size: 14px;
                margin-bottom: 15px;
            }}
            .contact-info {{
                display: flex;
                align-items: center;
                margin: 10px 0;
            }}
            .icon {{
                width: 20px;
                height: 20px;
                margin-right: 10px;
                color: #667eea;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <!-- Header -->
            <div class="header">
                <h1 class="mb-0">📬 New Portfolio Message</h1>
                <p class="mb-0">You've received a new contact form submission</p>
            </div>
            
            <!-- Content -->
            <div class="content">
                <div class="timestamp">
                    <strong>📅 Received:</strong> {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}
                </div>
                
                <!-- Contact Information -->
                <div class="info-card">
                    <h5 class="text-primary mb-3">👤 Contact Information</h5>
                    <div class="contact-info">
                        <span class="icon">👤</span>
                        <strong>Name:</strong> &nbsp; {name}
                    </div>
                    <div class="contact-info">
                        <span class="icon">✉️</span>
                        <strong>Email:</strong> &nbsp; 
                        <a href="mailto:{email}" style="color: #667eea; text-decoration: none;">{email}</a>
                    </div>
                </div>
                
                <!-- Message -->
                <div class="message-box">
                    <h5 class="text-dark mb-3">💬 Message</h5>
                    <div style="line-height: 1.6; color: #495057;">
                        {message.replace(chr(10), '<br>')}
                    </div>
                </div>
                
                <!-- Action Button -->
                <div class="text-center">
                    <a href="mailto:{email}?subject=Re: Portfolio Contact&body=Hi {name},%0A%0AThank you for reaching out through my portfolio. " 
                       class="btn-reply">
                        📧 Reply to {name}
                    </a>
                </div>
                
                <!-- Additional Info -->
                <div class="mt-4">
                    <div class="alert alert-info" style="border-left: 4px solid #0dcaf0;">
                        <strong>💡 Quick Actions:</strong>
                        <ul class="mb-0 mt-2">
                            <li>Click the reply button above to respond directly</li>
                            <li>Add <strong>{email}</strong> to your contacts</li>
                            <li>This message was sent through your portfolio contact form</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <p class="mb-2"><strong>🌐 Portfolio Contact System</strong></p>
                <p class="mb-0">This email was automatically generated from your portfolio website contact form.</p>
                <small>© 2024 Portfolio Backend | Quantum Developer</small>
            </div>
        </div>
    </body>
    </html>
    """