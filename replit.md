# Secrétaire Médicale

## Overview

Secrétaire Médicale is a medical appointment management system designed to help patients book and manage their medical appointments with doctors. The application consists of an Angular frontend for the user interface and a Flask backend API for data management and authentication.

## System Architecture

### Frontend Architecture
- **Framework**: Angular 19 with standalone components
- **Styling**: Bootstrap 5 with custom CSS
- **State Management**: Angular services with RxJS observables
- **Routing**: Angular Router with route guards for authentication
- **Authentication**: JWT-based authentication with token storage

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (can be upgraded to PostgreSQL)
- **Authentication**: Flask-JWT-Extended for JWT token management
- **API Design**: RESTful API with Blueprint organization
- **Cross-Origin**: Flask-CORS for frontend-backend communication

## Key Components

### Frontend Components
1. **Authentication Components**
   - Login Component: User authentication
   - Register Component: Patient registration with comprehensive form
   - Auth Guard: Route protection for authenticated users

2. **Dashboard Components**
   - Dashboard Component: Overview of patient statistics and recent appointments
   - Appointments Component: List and manage existing appointments
   - Book Appointment Component: Create new appointments with doctor selection

3. **Services**
   - Auth Service: Handles authentication, token management, and user state
   - Appointment Service: Manages appointment CRUD operations and doctor data

### Backend Components
1. **Models** (SQLAlchemy)
   - Patient: User account information and medical details
   - Medecin (Doctor): Doctor profiles and specialties
   - RendezVous (Appointment): Appointment scheduling and status tracking

2. **API Blueprints**
   - Auth Blueprint: Registration, login, and authentication endpoints
   - Appointment Blueprint: Appointment management and doctor listing

3. **Database Layer**
   - SQLAlchemy ORM with declarative base
   - Automatic table creation and data initialization
   - Password hashing for security

## Data Flow

1. **User Registration/Login**
   - Frontend sends credentials to `/api/auth/login` or `/api/auth/register`
   - Backend validates and returns JWT tokens
   - Frontend stores tokens and updates authentication state

2. **Appointment Management**
   - Authenticated requests to `/api/appointments/` endpoints
   - JWT token validation on each request
   - CRUD operations on appointment data with doctor relationships

3. **Real-time Updates**
   - Angular services use RxJS observables for reactive data flow
   - Automatic UI updates when data changes
   - Error handling and user feedback throughout the application

## External Dependencies

### Frontend Dependencies
- Angular 19 framework and CLI tools
- Bootstrap 5 for responsive design
- Font Awesome for icons
- RxJS for reactive programming

### Backend Dependencies
- Flask web framework
- Flask-CORS for cross-origin requests
- Flask-JWT-Extended for authentication
- SQLAlchemy for database operations
- Marshmallow for data validation
- Werkzeug for password hashing

## Deployment Strategy

### Development Setup
- Angular development server on port 4200
- Flask development server on port 5000
- CORS configured for cross-origin communication
- SQLite database for local development

### Production Considerations
- Angular build output served by Flask static files
- Single server deployment with Flask serving both API and frontend
- Database upgrade path to PostgreSQL available
- Environment-based configuration for secrets

### Default Data
- Automatic creation of default doctor "Ahmed Samir" during database initialization
- Database setup script for initial configuration

## Changelog
- July 03, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.