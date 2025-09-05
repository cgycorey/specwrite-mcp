# SpecWrite-MCP Templates and Examples

This document provides detailed templates and examples for each role's specifications based on BDD (Behavior-Driven Development) methodologies.

## Table of Contents
1. [Product Manager Templates](#product-manager-templates)
2. [Architect Templates](#architect-templates)
3. [Developer Templates](#developer-templates)
4. [Tester Templates](#tester-templates)
5. [Complete Workflow Example](#complete-workflow-example)

---

## Product Manager Templates (Requirements Analysis Phase)

### Product Specification Template

```markdown
# Product Specification: User Authentication System

## Business Value
Enable secure user access to the platform, protecting user data while providing a seamless login experience. This will increase user engagement and trust in the platform.

## User Stories
- As a new user, I want to register for an account so that I can access the platform
- As a returning user, I want to login with my credentials so that I can access my account
- As a user, I want to reset my password so that I can regain access to my account
- As a security-conscious user, I want to enable two-factor authentication so that my account is more secure

## Acceptance Criteria
### User Registration
- Given I am on the registration page, when I enter valid email and password, then my account should be created
- Given I am registering, when I enter an email that already exists, then I should see an error message
- Given I am registering, when I enter a weak password, then I should see password strength requirements

### User Login
- Given I am on the login page, when I enter valid credentials, then I should be redirected to my dashboard
- Given I am logging in, when I enter invalid credentials, then I should see an error message
- Given I have enabled 2FA, when I login, then I should be prompted for my 2FA code

## Success Metrics
- User registration conversion rate > 80%
- Login success rate > 95%
- Account security incidents < 0.1%
- User satisfaction score > 4.5/5

## Dependencies
- Email service for verification and password reset
- SMS service for 2FA (optional)
- Security audit and penetration testing
```

### Requirements Review Template

```markdown
# Requirements Review: Security Assessment

## Review Scope
- Authentication system security requirements
- Data protection and privacy requirements
- Compliance requirements (GDPR, CCPA)

## Security Requirements
- Passwords must be hashed using bcrypt with salt
- JWT tokens must expire after 1 hour
- Rate limiting must be implemented on authentication endpoints
- All authentication attempts must be logged
- Session cookies must be secure and HTTP-only

## Compliance Requirements
- User data must be encrypted at rest and in transit
- Users must be able to request data deletion
- Privacy policy must be easily accessible
- Consent must be obtained for data processing

## Identified Risks
- **High**: Brute force attacks on login endpoints
- **Medium**: Session hijacking through token theft
- **Low**: Information disclosure through error messages

## Recommendations
- Implement account lockout after 5 failed attempts
- Use refresh tokens for long-lived sessions
- Add IP-based anomaly detection
- Implement regular security audits
```

---

## Architect Templates (Technical Design Phase)

### System Architecture Template

```markdown
# Technical Design: Authentication Microservice

## Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │    │   API Gateway    │    │   Auth Service   │
│                 │◄──►│                 │◄──►│                 │
│ - React Native  │    │ - Rate Limiting │    │ - JWT Generation│
│ - Web App       │    │ - Load Balancer │    │ - User Validation│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │   PostgreSQL    │
                                              │                 │
                                              │ - User Profiles  │
                                              │ - Sessions      │
                                              │ - Audit Logs    │
                                              └─────────────────┘
```

## API Design

### POST /api/auth/register
- **Description**: Register a new user account
- **Request**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "firstName": "John",
    "lastName": "Doe"
  }
  ```
- **Response** (201):
  ```json
  {
    "id": "uuid",
    "email": "user@example.com",
    "accessToken": "jwt-token",
    "refreshToken": "refresh-token",
    "expiresIn": 3600
  }
  ```
- **Authentication**: None required
- **Rate Limit**: 5 requests per minute per IP

### POST /api/auth/login
- **Description**: Authenticate user and return JWT tokens
- **Request**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response** (200):
  ```json
  {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe"
    },
    "accessToken": "jwt-token",
    "refreshToken": "refresh-token",
    "expiresIn": 3600
  }
  ```

## Database Schema

### users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### user_sessions Table
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    access_token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Indexes
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_refresh_token ON user_sessions(refresh_token_hash);
```

## Technology Stack
- **Backend**: Python 3.12+ with FastAPI
- **Database**: PostgreSQL 15+
- **Cache**: Redis for session management
- **Security**: bcrypt for password hashing, PyJWT for tokens
- **Monitoring**: Prometheus and Grafana
- **Logging**: Structured logging with ELK stack

## Non-Functional Requirements
- **Performance**: < 500ms response time for authentication endpoints
- **Security**: OAuth 2.0 compliant, JWT tokens with RS256 signing
- **Scalability**: Handle 10,000 concurrent authentication requests
- **Availability**: 99.9% uptime with automatic failover
- **Compliance**: GDPR, CCPA, and SOC 2 compliant
```

---

## Developer Templates (Development & Implementation Phase)

### Feature Implementation Template

```markdown
# Feature Implementation: User Registration API

## Code Structure

### src/auth/schemas.py
```python
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserRegistration(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    first_name: constr(min_length=1, max_length=100)
    last_name: constr(min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    email_verified: bool
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    user: UserResponse
```

### src/auth/services.py
```python
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import jwt
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    async def register_user(self, user_data: UserRegistration) -> UserResponse:
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            User.email == user_data.email
        ).first()
        
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password
        password_hash = bcrypt.hashpw(
            user_data.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Create user
        user = User(
            email=user_data.email,
            password_hash=password_hash,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Generate tokens
        access_token = self._generate_access_token(user.id)
        refresh_token = self._generate_refresh_token()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=3600,
            user=UserResponse.from_orm(user)
        )
    
    def _generate_access_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "type": "access"
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    def _generate_refresh_token(self) -> str:
        return secrets.token_urlsafe(32)
```

### src/auth/routes.py
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import UserRegistration
from .services import AuthService
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    user_data: UserRegistration,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - Validates email format and password strength
    - Hashes password using bcrypt
    - Returns JWT access and refresh tokens
    """
    try:
        auth_service = AuthService(db)
        return await auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Unit Tests

### tests/auth/test_services.py
```python
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from auth.services import AuthService
from auth.schemas import UserRegistration

class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        mock_db = Mock(spec=Session)
        return AuthService(mock_db)
    
    @pytest.fixture
    def user_data(self):
        return UserRegistration(
            email="test@example.com",
            password="SecurePassword123!",
            first_name="John",
            last_name="Doe"
        )
    
    def test_register_user_success(self, auth_service, user_data):
        # Mock database queries
        auth_service.db.query.return_value.filter.return_value.first.return_value = None
        
        with patch('auth.services.bcrypt') as mock_bcrypt:
            mock_bcrypt.hashpw.return_value = b"hashed_password"
            
            result = auth_service.register_user(user_data)
            
            assert result.user.email == user_data.email
            assert result.user.first_name == user_data.first_name
            assert "access_token" in result
            assert "refresh_token" in result
    
    def test_register_user_existing_email(self, auth_service, user_data):
        # Mock existing user
        mock_user = Mock()
        auth_service.db.query.return_value.filter.return_value.first.return_value = mock_user
        
        with pytest.raises(ValueError) as exc_info:
            auth_service.register_user(user_data)
        
        assert "already exists" in str(exc_info.value)
```

## Integration Points

### Database Integration
- PostgreSQL connection pool with SQLAlchemy
- Database migrations with Alembic
- Connection retry logic for resilience

### External Services
- Email service for verification emails
- Redis for session management
- Monitoring service for metrics collection

### Error Handling
- Database connection failures
- Email service outages
- Invalid input validation
- JWT token validation failures

## Performance Considerations

### Database Optimization
- Index on email column for fast lookups
- Connection pooling to reduce overhead
- Query optimization with proper joins

### Security Considerations
- Password hashing with bcrypt (cost factor 12)
- JWT token expiration (1 hour access, 30 days refresh)
- Rate limiting to prevent brute force attacks
- Input validation and sanitization

### Memory Management
- Efficient password hashing to prevent memory exhaustion
- Connection pooling to manage database connections
- Proper cleanup of resources
```

---

## Tester Templates (Testing & Validation Phase)

### Test Plan Template

```markdown
# Test Plan: Authentication System

## Test Scope

### In Scope
- User registration functionality
- User login functionality
- Password reset functionality
- JWT token management
- Security features (rate limiting, password validation)
- API endpoint responses and error handling

### Out of Scope
- User profile management
- Email template rendering
- Frontend user interface
- Performance testing beyond baseline
- Security penetration testing

## Test Strategy

### Unit Tests (Target: 95% coverage)
**Components to Test:**
- AuthService.register_user()
- AuthService.login_user()
- AuthService.validate_token()
- Password hashing and validation
- JWT token generation and validation
- Input validation schemas
- Database operations

**Tools:** pytest, pytest-cov, unittest.mock

### Integration Tests (Target: 90% coverage)
**Components to Test:**
- API endpoint integration with database
- Email service integration
- Redis session management
- Error handling across service boundaries
- Data flow between components

**Tools**: Testcontainers, pytest-asyncio, requests

### System Tests (Target: 85% coverage)
**Components to Test:**
- End-to-end user registration flow
- Complete login and session management
- Password reset workflow
- Security measures (rate limiting, etc.)
- API contract compliance

**Tools**: Postman, Selenium, JMeter

## Test Cases

### User Registration Tests

#### TC-REG-001: Successful User Registration
- **Priority**: High
- **Preconditions**: 
  - Database is accessible
  - Email service is operational
- **Steps**:
  1. Send POST request to /api/auth/register with valid data
  2. Verify response status code is 201
  3. Verify user record exists in database
  4. Verify password is hashed correctly
  5. Verify JWT tokens are returned
- **Expected Results**: 
  - User account created successfully
  - Password properly hashed
  - Valid JWT tokens returned
- **Acceptance Criteria**: All verification steps pass

#### TC-REG-002: Duplicate Email Registration
- **Priority**: High
- **Preconditions**: User with email exists in database
- **Steps**:
  1. Send POST request to /api/auth/register with existing email
  2. Verify response status code is 400
  3. Verify error message is appropriate
  4. Verify no new user record created
- **Expected Results**: Registration rejected with proper error message
- **Acceptance Criteria**: Error response returned, no duplicate user created

#### TC-REG-003: Weak Password Validation
- **Priority**: Medium
- **Preconditions**: None
- **Steps**:
  1. Send registration request with weak password ("123456")
  2. Verify response status code is 422
  3. Verify validation error message
- **Expected Results**: Registration rejected with password strength error
- **Acceptance Criteria**: Password validation error returned

### Security Tests

#### TC-SEC-001: SQL Injection Prevention
- **Priority**: Critical
- **Preconditions**: None
- **Steps**:
  1. Send registration request with SQL injection in email field
  2. Verify request is rejected with validation error
  3. Check database logs for suspicious queries
- **Expected Results**: Request rejected, no SQL injection successful
- **Acceptance Criteria**: Input validation prevents SQL injection

#### TC-SEC-002: Rate Limiting Effectiveness
- **Priority**: High
- **Preconditions**: Rate limiting configured (5 requests/minute)
- **Steps**:
  1. Send 6 registration requests within 1 minute from same IP
  2. Verify 6th request returns 429 status code
  3. Wait for rate limit window to expire
  4. Send another request and verify success
- **Expected Results**: Rate limiting properly blocks excessive requests
- **Acceptance Criteria**: 429 response after limit reached, requests succeed after window

## Test Environment

### Development Environment
- **Application**: Local Docker container
- **Database**: PostgreSQL 15 in Docker
- **Dependencies**: Redis, Mailhog (email testing)
- **Test Data**: Seeded with test users and scenarios

### Staging Environment
- **Application**: Kubernetes cluster
- **Database**: PostgreSQL RDS
- **Dependencies**: AWS ElastiCache, SES
- **Test Data**: Anonymized production data subset

### Production Environment
- **Application**: Production Kubernetes cluster
- **Database**: Production PostgreSQL RDS
- **Dependencies**: Production services
- **Test Data**: Limited to smoke tests only

## Test Data Requirements

### User Registration Test Data
```json
{
  "valid_user": {
    "email": "test@example.com",
    "password": "SecurePassword123!",
    "first_name": "Test",
    "last_name": "User"
  },
  "invalid_emails": [
    "invalid-email",
    "@example.com",
    "test@",
    "test.example.com"
  ],
  "weak_passwords": [
    "123456",
    "password",
    "qwerty",
    "11111111"
  ]
}
```

## Exit Criteria

### Must-Have Criteria
- [ ] All critical and high priority test cases pass
- [ ] Unit test coverage ≥ 95%
- [ ] Integration test coverage ≥ 90%
- [ ] No security vulnerabilities identified
- [ ] Performance requirements met (< 500ms response time)
- [ ] All acceptance criteria satisfied

### Nice-to-Have Criteria
- [ ] System test coverage ≥ 85%
- [ ] Documentation updated
- [ ] Test automation pipeline established
- [ ] Performance benchmarks established

## Quality Gates

### Code Quality
- SonarQube quality gate passed
- No critical security vulnerabilities
- Code duplication < 5%

### Test Quality
- All automated tests passing
- Test flakiness rate < 2%
- Test execution time < 10 minutes

### Release Criteria
- All exit criteria met
- Stakeholder approval obtained
- Deployment pipeline validated
- Rollback plan documented
```

---

## Complete Workflow Example

### Phase 1: Product Manager

```python
# Create product specification
create_spec(
    title="E-commerce Platform - User Authentication",
    description="Complete user authentication system for e-commerce platform",
    content="""
# Product Specification: User Authentication

## Business Value
Enable secure user access to the e-commerce platform, protecting user accounts and payment information while providing seamless shopping experience.

## User Stories
- As a shopper, I want to register for an account so that I can save my cart and order history
- As a returning customer, I want to login quickly so that I can resume shopping
- As a security-conscious user, I want to enable two-factor authentication so that my account is protected
- As a mobile user, I want to login with biometrics so that I can access my account easily

## Acceptance Criteria
- User registration with email verification
- Secure password storage and validation
- JWT-based authentication with refresh tokens
- Session management with automatic logout
- Two-factor authentication support
- Rate limiting to prevent brute force attacks
"""
)

# Review security requirements
review_requirements(
    title="Security Requirements Review",
    description="Review authentication security requirements for compliance",
    content="""
# Requirements Review: Security Assessment

## Security Requirements
- PCI DSS compliance for payment processing
- GDPR compliance for user data protection
- OAuth 2.0 implementation for third-party logins
- Regular security audits and penetration testing
- Encryption of sensitive data at rest and in transit
"""
)
```

### Phase 2: Architect

```python
# Design system architecture
design_system(
    title="Authentication System Architecture",
    description="Microservices architecture for user authentication",
    content="""
# Technical Design: Authentication Microservice

## Architecture Overview
[Detailed architecture diagram showing microservices, load balancers, databases]

## API Design
- POST /api/auth/register - User registration
- POST /api/auth/login - User authentication  
- POST /api/auth/refresh - Token refresh
- POST /api/auth/logout - Session termination
- POST /api/auth/2fa/enable - Enable 2FA
- POST /api/auth/2fa/verify - Verify 2FA code

## Database Schema
- Users table with profile information
- Sessions table for active sessions
- Audit logs for security events
- 2FA configurations table

## Security Measures
- JWT tokens with RS256 signing
- Rate limiting on authentication endpoints
- IP-based anomaly detection
- Password strength validation
"""
)

# Create technical specifications
create_technical_spec(
    title="JWT Implementation Specification",
    description="Detailed JWT token implementation",
    content="""
# Technical Specification: JWT Implementation

## Token Structure
- Access tokens: 1-hour expiration
- Refresh tokens: 30-day expiration
- Claims: user_id, email, roles, permissions
- Signing algorithm: RS256

## Security Considerations
- Token revocation mechanism
- Refresh token rotation
- CSRF protection
- Secure storage requirements
"""
)
```

### Phase 3: Developer

```python
# Implement core features
implement_feature(
    title="User Registration Endpoint",
    description="Implement POST /api/auth/register endpoint",
    content="""
# Feature Implementation: User Registration

## Code Structure
- src/auth/schemas.py - Pydantic models
- src/auth/services.py - Business logic
- src/auth/routes.py - API endpoints
- src/auth/repositories.py - Database operations

## Key Components
- Email validation with regex
- Password strength validation
- Bcrypt password hashing
- JWT token generation
- Database transaction management
"""
)

# Write security code
write_code(
    title="Password Security Module",
    description="Implement password hashing and validation",
    content="""
# Security Implementation: Password Management

## Features
- Bcrypt hashing with salt generation
- Password strength validation
- Rate limiting for login attempts
- Account lockout mechanism
- Password reset functionality

## Security Measures
- Constant-time comparison for password verification
- Secure random salt generation
- Protection against timing attacks
"""
)

# Create comprehensive tests
create_tests(
    title="Authentication Test Suite",
    description="Unit and integration tests for auth system",
    content="""
# Test Suite: Authentication System

## Unit Tests
- User registration success/failure scenarios
- Password hashing and validation
- JWT token generation and validation
- Input validation and error handling

## Integration Tests
- API endpoint functionality
- Database integration
- Email service integration
- Session management

## Security Tests
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting effectiveness
"""
)
```

### Phase 4: Tester

```python
# Create comprehensive test plan
create_test_plan(
    title="Authentication System Test Plan",
    description="Complete testing strategy for auth system",
    content="""
# Test Plan: Authentication System

## Test Strategy
- Unit tests: 95% code coverage
- Integration tests: API and database integration
- Security tests: Penetration testing and vulnerability assessment
- Performance tests: Load testing and stress testing
- UAT: User acceptance testing with stakeholders

## Test Cases
- Functional testing of all authentication flows
- Security testing of all endpoints
- Performance testing under load
- Usability testing of user interfaces
- Compliance testing for regulations

## Quality Gates
- All critical bugs resolved
- Security vulnerabilities addressed
- Performance requirements met
- User acceptance obtained
"""
)

# Execute comprehensive tests
execute_tests(
    title="Execute Authentication Test Suite",
    description="Run full test suite for authentication system",
    content="""
# Test Execution Results

## Test Results Summary
- Unit Tests: 156/156 passed (100%)
- Integration Tests: 89/92 passed (96.7%)
- Security Tests: 24/24 passed (100%)
- Performance Tests: All benchmarks met

## Issues Identified
- 3 minor integration test failures
- 2 performance optimization opportunities
- 1 documentation update required

## Resolution Status
- All issues addressed and resolved
- Performance optimizations implemented
- Documentation updated
"""
)

# Generate final test reports
generate_test_reports(
    title="Authentication System Quality Report",
    description="Comprehensive quality assessment report",
    content="""
# Quality Report: Authentication System

## Quality Metrics
- Code Quality: 9.2/10 (SonarQube)
- Test Coverage: 95.2%
- Security Score: A (no vulnerabilities)
- Performance: 98% of SLA met
- Reliability: 99.9% uptime

## Compliance Status
- PCI DSS: Compliant
- GDPR: Compliant
- SOC 2: Compliant
- OWASP Top 10: Mitigated

## Release Recommendation
✅ Approved for production deployment
"""
)
```

This workflow demonstrates how each role contributes to the four-stage development process, with clear outputs and format requirements for each stage.