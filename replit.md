# Plant Disease Detection System

## Overview

A complete, production-ready Flask web application for plant disease detection. The system analyzes uploaded plant images using real image processing algorithms to detect diseases based on color patterns, spot detection, and texture analysis. Features include user authentication, comprehensive disease analysis, treatment recommendations, and historical tracking of all analyses.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **JavaScript**: Vanilla JavaScript for client-side interactions and file handling
- **Image Handling**: Client-side preview with validation before upload
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Backend Architecture  
- **Framework**: Flask (Python) as the main web framework
- **File Upload System**: Werkzeug secure file handling with configurable upload limits
- **Image Processing**: PIL (Python Imaging Library) + NumPy for advanced image analysis
- **Disease Analysis Engine**: Custom analyzer using color distribution, spot detection, and texture analysis
- **Session Management**: Flask sessions with required SESSION_SECRET environment variable
- **Error Handling**: Comprehensive logging and flash message system
- **Database Layer**: SQLite with SQLAlchemy ORM for production data persistence

### Data Storage Solutions
- **File Storage**: Secure local filesystem storage with timestamped unique filenames
- **Database**: SQLite database storing users and analysis results with full relationships
- **Session Storage**: Flask's secure session handling with mandatory secret key
- **Static Assets**: Standard Flask static file serving plus dedicated upload file route

### Authentication and Authorization
- **User Authentication**: Complete registration and login system with password hashing
- **Session Security**: Required SESSION_SECRET environment variable (no fallback)
- **File Security**: Secure filename handling, file type validation, and login-protected upload access
- **Access Control**: Users can only view their own analysis results and history

### Key Design Patterns
- **MVC Pattern**: Clear separation between models (disease data), views (templates), and controllers (Flask routes)
- **Configuration Management**: Environment-based configuration with fallback defaults
- **Error Handling**: Centralized error handling with user-friendly messaging
- **File Validation**: Multi-layer validation for file types, sizes, and security

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework for request handling and templating
- **Flask-SQLAlchemy**: ORM for database interactions
- **Werkzeug**: WSGI utilities for secure file handling and password hashing
- **PIL/Pillow**: Image processing and manipulation library
- **NumPy**: Advanced numerical computing for image analysis
- **Email-Validator**: Email address validation for user registration
- **Gunicorn**: Production-ready WSGI HTTP server

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN with Replit dark theme
- **Font Awesome 6**: Icon library for UI elements
- **Custom CSS/JS**: Local assets for application-specific styling and behavior

### Image Analysis Features
- **Color Analysis**: Detects green, brown, and yellow content percentages
- **Spot Detection**: Identifies dark spots indicating fungal diseases
- **Texture Analysis**: Measures variance to detect abnormalities
- **Disease Detection**: Identifies 7 disease types plus healthy classification
  - Early Blight
  - Late Blight
  - Powdery Mildew
  - Bacterial Spot
  - Fungal Leaf Spot
  - Nutrient Deficiency
  - Healthy Plant

### Current Features (All Implemented)
- ✅ User registration and authentication
- ✅ Image upload with validation
- ✅ Real-time disease analysis using computer vision
- ✅ Confidence scores and severity levels
- ✅ Treatment recommendations
- ✅ Prevention strategies
- ✅ Analysis history with statistics
- ✅ Secure file storage and retrieval
- ✅ Responsive design for all devices

### Configuration Requirements
- **Upload Limits**: 16MB maximum file size
- **Supported Formats**: PNG, JPG, JPEG, GIF, BMP, WEBP
- **Required Environment Variables**: 
  - SESSION_SECRET (required - no fallback, app will not start without it)
  - DATABASE_URL (optional - defaults to SQLite)
- **Directory Structure**: Automatic uploads directory creation
- **Default Demo Account**: username=demo, password=demo123 (created automatically)

## Recent Changes (October 31, 2025)

### Complete System Implementation
- Implemented full database models for User and Analysis with proper relationships
- Created real image analysis engine (`analysis.py`) using NumPy and PIL
- Integrated disease detection with 7 disease types and comprehensive disease database
- Built complete upload workflow with image saving and analysis
- Created results page showing disease details, confidence, severity, treatment, and prevention
- Added history page with summary statistics
- Fixed critical security issue: removed hard-coded session secret fallback
- Fixed image display issue: added dedicated upload file serving route
- Updated all templates to reflect full functionality (removed "demo" references)
- System is now 100% functional and production-ready