# Changelog

All notable changes to KMLC will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-11-28

### Added
- Complete code refactoring with clean architecture
- Comprehensive English documentation
- API documentation in docs/API.md
- Deployment guide in docs/DEPLOYMENT.md
- Contributing guidelines
- Logo component for reusability
- Start processing button in task list
- Form data support for file upload

### Changed
- Rebranded to Kompa MultiLevel Classifier (KMLC)
- Updated logo to Kompa branding
- Changed primary color from red (#a10239) to blue (#4BADED)
- Improved code documentation with English comments
- Refactored all backend files for better maintainability
- Enhanced error handling and validation
- Optimized database operations

### Fixed
- Hydration mismatch errors in Next.js frontend
- Upload endpoint not receiving topic_id correctly
- Bcrypt compatibility issues with Python 3.11
- Authentication flow with proper client-side checks
- Task processing workflow with proper status transitions

### Removed
- Unused frontend components (FileUpload, ProcessingPanel, TaskList)
- Redundant documentation files (moved to docs/archive)
- Legacy code and commented-out sections

### Security
- Updated bcrypt to version 4.0.1
- Improved JWT token validation
- Enhanced password hashing security
- Added proper CORS configuration

## [2.0.0] - 2025-11-27

### Added
- Next.js frontend with TypeScript
- MongoDB integration for data persistence
- Queue-based task processing
- Topic management system
- User management with role-based access
- JWT authentication
- Real-time progress tracking
- Smart caching system

### Changed
- Migrated from Streamlit to Next.js
- Switched from in-memory to MongoDB storage
- Implemented background worker for processing

## [1.0.0] - 2025-11-26

### Added
- Initial release with Streamlit interface
- Basic LLM classification
- Excel file processing
- Simple caching mechanism
