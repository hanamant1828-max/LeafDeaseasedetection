# Plant Disease Detection System

## Overview

A Flask-based web application demonstrating a plant disease detection system frontend. The application provides a complete user interface for uploading plant images with a modern, responsive design using Bootstrap. Currently serves as a frontend demonstration with machine learning integration planned for future development.

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
- **Image Processing**: PIL (Python Imaging Library) for image manipulation and validation
- **Session Management**: Flask sessions with configurable secret keys
- **Error Handling**: Comprehensive logging and flash message system
- **Mock Data Layer**: In-memory disease database for demonstration purposes

### Data Storage Solutions
- **File Storage**: Local filesystem storage in uploads directory (demo only - files not permanently stored)
- **Disease Database**: Removed for frontend-only demonstration
- **Session Storage**: Flask's built-in session handling
- **Static Assets**: Standard Flask static file serving

### Authentication and Authorization
- **Current State**: No authentication system implemented
- **Session Security**: Configurable secret key for session management
- **File Security**: Secure filename handling and file type validation

### Key Design Patterns
- **MVC Pattern**: Clear separation between models (disease data), views (templates), and controllers (Flask routes)
- **Configuration Management**: Environment-based configuration with fallback defaults
- **Error Handling**: Centralized error handling with user-friendly messaging
- **File Validation**: Multi-layer validation for file types, sizes, and security

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework for request handling and templating
- **Werkzeug**: WSGI utilities for secure file handling
- **PIL/Pillow**: Image processing and manipulation library

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN with Replit dark theme
- **Font Awesome 6**: Icon library for UI elements
- **Custom CSS/JS**: Local assets for application-specific styling and behavior

### Development Dependencies
- **Python Standard Library**: os, logging, random, json modules
- **Environment Variables**: For configuration management (SESSION_SECRET)

### Future Integration Considerations
- **Machine Learning Models**: Architecture prepared for ML model integration
- **Database Systems**: Structure allows for easy database integration (currently using mock data)
- **Cloud Storage**: File handling system can be extended for cloud storage solutions
- **API Services**: Backend architecture supports external API integrations for disease detection

### Configuration Requirements
- **Upload Limits**: 16MB maximum file size
- **Supported Formats**: PNG, JPG, JPEG, GIF, BMP, WEBP
- **Environment Variables**: SESSION_SECRET for production deployment
- **Directory Structure**: Automatic uploads directory creation