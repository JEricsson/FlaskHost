# Flask Web App

A simple Python web application built with Flask.

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask server:
   ```bash
   python host.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

### Available Endpoints

- `/` - Home page with welcome message
- `/health` - Health check endpoint (returns JSON status)

### Development

The application runs in debug mode by default, which means:
- The server will automatically restart when you make changes to the code
- Detailed error messages will be displayed in the browser
- The server binds to `0.0.0.0:5000` to allow external access

### File Structure

```
.
├── host.py          # Main Flask application
├── requirements.txt # Python dependencies
└── README.md       # This file
```

## Notes

- The server is configured to run on port 5000
- Debug mode is enabled for development
- The application includes basic HTML styling for a clean interface