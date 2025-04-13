"""Security utilities for the CV Parser application.

This module provides security-related functionality including rate limiting,
security headers, input sanitization, request validation, and CORS configuration.
"""

import time
from functools import wraps
from typing import Dict, Optional, Callable, Any, Union
from flask import Request, Response, make_response
import re
from datetime import datetime, timedelta
import logging
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

# Security configuration
RATE_LIMIT_WINDOW = 60  # 1 minute
MAX_REQUESTS = 100  # requests per window
ALLOWED_ORIGINS = [
    'https://cv-branding-buddy.web.app',
    'https://cv-branding-buddy.firebaseapp.com',
    'http://localhost:3000'  # For local development
]

# In-memory rate limiting store (consider using Redis for production)
rate_limit_store: Dict[str, Dict[str, Union[int, float]]] = {}

def rate_limit() -> Callable:
    """Rate limiting decorator for Cloud Functions.
    
    Limits requests to MAX_REQUESTS per RATE_LIMIT_WINDOW seconds per client IP.
    Uses an in-memory store that should be replaced with Redis in production.
    
    Returns:
        Callable: Decorator function that implements rate limiting
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request: Request, *args: Any, **kwargs: Any) -> Response:
            client_id = request.headers.get('X-Forwarded-For', 'unknown')
            current_time = time.time()
            
            # Clean up expired entries
            rate_limit_store.update({
                k: v for k, v in rate_limit_store.items()
                if current_time - v['timestamp'] < RATE_LIMIT_WINDOW
            })
            
            # Check and update rate limit
            if client_id in rate_limit_store:
                client_data = rate_limit_store[client_id]
                if (client_data['count'] >= MAX_REQUESTS and 
                    current_time - client_data['timestamp'] < RATE_LIMIT_WINDOW):
                    logger.warning(f"Rate limit exceeded for client {client_id}")
                    return make_response(
                        {'error': 'Rate limit exceeded. Please try again later.'},
                        429
                    )
                elif current_time - client_data['timestamp'] >= RATE_LIMIT_WINDOW:
                    client_data['count'] = 0
                    client_data['timestamp'] = current_time
                client_data['count'] += 1
            else:
                rate_limit_store[client_id] = {
                    'count': 1,
                    'timestamp': current_time
                }
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def add_security_headers(response: Response) -> Response:
    """Add security headers to the response.
    
    Implements security best practices including HSTS, CSP, and other
    security-related headers.
    
    Args:
        response: Flask Response object to add headers to
        
    Returns:
        Response: Response with security headers added
    """
    security_headers = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'",
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
    }
    
    for header, value in security_headers.items():
        response.headers[header] = value
    
    return response

def sanitize_input(text: Optional[str]) -> Optional[str]:
    """Sanitize input text to prevent injection attacks.
    
    Removes potentially dangerous characters and control sequences
    while preserving legitimate content.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Optional[str]: Sanitized text or None if input was None
    """
    if not text:
        return text
    
    # Remove potentially dangerous characters and control sequences
    text = re.sub(r'[<>]', '', text)  # Remove HTML-like tags
    text = text.replace('\0', '')  # Remove null bytes
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    
    return text

def validate_request_headers(request: Request) -> Optional[Response]:
    """Validate request headers for security requirements.
    
    Checks for required security headers and content type validation
    for POST/PUT requests.
    
    Args:
        request: Flask Request object to validate
        
    Returns:
        Optional[Response]: Error response if validation fails, None if successful
    """
    # Content-Type validation for POST/PUT
    if request.method in ['POST', 'PUT']:
        content_type = request.headers.get('Content-Type', '')
        if not content_type.startswith('application/json'):
            return make_response(
                {'error': 'Invalid Content-Type. Must be application/json'},
                415
            )
    
    # Required headers check
    required_headers = ['X-Request-ID']
    missing_headers = [h for h in required_headers if h not in request.headers]
    if missing_headers:
        return make_response(
            {'error': f'Missing required headers: {", ".join(missing_headers)}'},
            400
        )
    
    return None

def validate_json_schema(request: Request, schema: Dict[str, Any]) -> Optional[Response]:
    """Validate JSON request body against a schema.
    
    Uses jsonschema library to validate request data against
    the provided JSON schema.
    
    Args:
        request: Flask Request object containing JSON data
        schema: JSON schema to validate against
        
    Returns:
        Optional[Response]: Error response if validation fails, None if successful
    """
    try:
        if not request.is_json:
            return make_response(
                {'error': 'Request must be JSON'},
                400
            )
        
        data = request.get_json()
        validate(instance=data, schema=schema)
        return None
        
    except ValidationError as e:
        logger.error(f"JSON schema validation error: {str(e)}")
        return make_response(
            {'error': f'Invalid JSON format: {str(e)}'},
            400
        )
    except Exception as e:
        logger.error(f"JSON validation error: {str(e)}")
        return make_response(
            {'error': 'Invalid JSON format'},
            400
        )

def setup_cors(request: Request) -> Response:
    """Configure CORS headers based on the request origin.
    
    Implements CORS policy with allowed origins and methods.
    Returns appropriate CORS headers for preflight and actual requests.
    
    Args:
        request: Flask Request object to get origin from
        
    Returns:
        Response: Response with CORS headers
    """
    origin = request.headers.get('Origin')
    if not origin:
        return make_response()
    
    response = make_response()
    
    if origin in ALLOWED_ORIGINS:
        response.headers.update({
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Request-ID',
            'Access-Control-Max-Age': '3600'
        })
    
    return response 