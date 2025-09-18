# Flask Web App

## Overview

This is a minimal Flask web application built with Python that serves as a basic web server. The application provides a simple welcome page and health check endpoint, designed for quick deployment and easy extension. It's structured as a lightweight starting point for web development projects using Flask framework.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Inline HTML Templates**: Uses Flask's `render_template_string` to serve HTML directly from Python strings
- **Embedded CSS**: Basic styling included within HTML templates for self-contained pages
- **Responsive Design**: Mobile-friendly viewport configuration with centered layout

### Backend Architecture
- **Flask Framework**: Lightweight Python web framework for handling HTTP requests
- **Single-file Application**: Entire application logic contained in `host.py` for simplicity
- **Route-based Structure**: Uses Flask decorators to define URL endpoints
- **Development Configuration**: Runs in debug mode with auto-reload and detailed error reporting

### Server Configuration
- **Host Binding**: Configured to bind to `0.0.0.0:5000` for external access
- **Debug Mode**: Enabled for development with automatic restart on code changes
- **Static Content**: No separate static file serving (CSS embedded in templates)

### Application Structure
- **Minimal Dependencies**: Only requires Flask framework
- **Single Entry Point**: `host.py` serves as both application definition and server launcher
- **Template Management**: HTML templates defined as Python string constants

## External Dependencies

### Python Packages
- **Flask 2.3.3**: Core web framework for handling HTTP requests and responses

### Runtime Requirements
- **Python 3.11+**: Required Python version for compatibility
- **pip**: Package installer for dependency management

### Development Tools
- **Built-in Flask Development Server**: Used for local development and testing
- **No Database**: Currently no persistent data storage configured
- **No External APIs**: Self-contained application with no third-party service integrations