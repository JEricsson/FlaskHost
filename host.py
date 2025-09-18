from flask import Flask, render_template_string

app = Flask(__name__)

# Basic HTML template
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Web App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            text-align: center;
            margin-top: 50px;
        }
        h1 {
            color: #333;
        }
        .info {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Flask!</h1>
        <div class="info">
            <p>Your Flask web application is running successfully!</p>
            <p>This is a basic Flask server created with Python.</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page route"""
    return render_template_string(HOME_TEMPLATE)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Flask app is running"}

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)