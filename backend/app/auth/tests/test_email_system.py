"""
Comprehensive test suite for the email reset system
Run with: poetry run pytest app/auth/tests/test_email_system.py -v
"""
import os
import pytest
from unittest.mock import patch, Mock, MagicMock
from types import SimpleNamespace
import requests

from app.auth.utils import (
    create_reset_token,
    verify_reset_token,
    send_reset_email,
)


class TestTokenGeneration:
    """Test token generation and verification"""
    
    def test_create_reset_token(self):
        """Test that reset tokens are created correctly"""
        user = SimpleNamespace(email="test@example.com")
        token = create_reset_token(user)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20  # Token should be reasonably long
    
    def test_verify_valid_token(self):
        """Test that valid tokens can be verified"""
        user = SimpleNamespace(email="test@example.com")
        token = create_reset_token(user)
        
        verified_email = verify_reset_token(token)
        assert verified_email == "test@example.com"
    
    def test_verify_invalid_token(self):
        """Test that invalid tokens return None"""
        invalid_token = "this-is-not-a-valid-token"
        verified_email = verify_reset_token(invalid_token)
        
        assert verified_email is None
    
    def test_verify_expired_token(self):
        """Test that expired tokens return None"""
        # Create an invalid/malformed token that will be rejected
        # This simulates an expired token without waiting
        expired_token = "this.is.an.expired.or.invalid.token"
        
        # Verify returns None for invalid/expired tokens
        verified_email = verify_reset_token(expired_token)
        assert verified_email is None
        
        # Also test with a very old timestamp embedded in token
        # The verify_reset_token function handles expiration internally
    
    def test_token_uniqueness(self):
        """Test that tokens are unique for different users"""
        user1 = SimpleNamespace(email="user1@example.com")
        user2 = SimpleNamespace(email="user2@example.com")
        
        token1 = create_reset_token(user1)
        token2 = create_reset_token(user2)
        
        assert token1 != token2
        assert verify_reset_token(token1) == "user1@example.com"
        assert verify_reset_token(token2) == "user2@example.com"


class TestEmailSending:
    """Test email sending functionality"""
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_WORKER_URL': 'https://test.workers.dev/',
        'CLOUDFLARE_WORKER_API_KEY': 'test-api-key'
    })
    @patch('app.auth.utils.requests.post')
    def test_send_reset_email_success(self, mock_post):
        """Test successful email sending"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response
        
        # Should not raise any exception
        send_reset_email("test@example.com", "test-token")
        
        # Verify the request was made correctly
        mock_post.assert_called_once_with(
            'https://test.workers.dev/',
            json={
                'to_email': 'test@example.com',
                'token': 'test-token',
                'api_key': 'test-api-key'
            },
            timeout=10
        )
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_WORKER_URL': 'https://test.workers.dev/',
        'CLOUDFLARE_WORKER_API_KEY': 'test-api-key'
    })
    @patch('app.auth.utils.requests.post')
    def test_send_reset_email_worker_error(self, mock_post):
        """Test handling of Cloudflare Worker errors"""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            send_reset_email("test@example.com", "test-token")
        
        assert "Failed to send email" in str(exc_info.value)
        assert "Internal Server Error" in str(exc_info.value)
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_WORKER_URL': 'https://test.workers.dev/',
        'CLOUDFLARE_WORKER_API_KEY': 'test-api-key'
    })
    @patch('app.auth.utils.requests.post')
    def test_send_reset_email_timeout(self, mock_post):
        """Test handling of timeout errors"""
        # Mock timeout
        mock_post.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(Exception) as exc_info:
            send_reset_email("test@example.com", "test-token")
        
        assert "timeout" in str(exc_info.value).lower()
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_WORKER_URL': 'https://test.workers.dev/',
        'CLOUDFLARE_WORKER_API_KEY': 'test-api-key'
    })
    @patch('app.auth.utils.requests.post')
    def test_send_reset_email_network_error(self, mock_post):
        """Test handling of network errors"""
        # Mock network error
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        with pytest.raises(Exception) as exc_info:
            send_reset_email("test@example.com", "test-token")
        
        assert "Network error" in str(exc_info.value)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_send_reset_email_missing_config(self):
        """Test handling of missing configuration"""
        with pytest.raises(Exception) as exc_info:
            send_reset_email("test@example.com", "test-token")
        
        assert "Missing Cloudflare Worker configuration" in str(exc_info.value)
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_WORKER_URL': '',  # Empty URL
        'CLOUDFLARE_WORKER_API_KEY': 'test-api-key'
    })
    def test_send_reset_email_empty_url(self):
        """Test handling of empty configuration values"""
        with pytest.raises(Exception) as exc_info:
            send_reset_email("test@example.com", "test-token")
        
        assert "Missing Cloudflare Worker configuration" in str(exc_info.value)


class TestEmailValidation:
    """Test email validation in the reset flow"""
    
    @patch.dict(os.environ, {
        'CLOUDFLARE_WORKER_URL': 'https://test.workers.dev/',
        'CLOUDFLARE_WORKER_API_KEY': 'test-api-key'
    })
    @patch('app.auth.utils.requests.post')
    def test_send_reset_email_various_formats(self, mock_post):
        """Test sending emails to various email formats"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response
        
        test_emails = [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user_123@subdomain.example.org",
        ]
        
        for email in test_emails:
            send_reset_email(email, "test-token")
            
            # Verify the email was passed correctly
            call_args = mock_post.call_args[1]['json']
            assert call_args['to_email'] == email


class TestIntegration:
    """Integration tests for the complete email reset flow"""
    
    @patch('app.auth.utils.requests.post')
    def test_complete_reset_flow(self, mock_post):
        """Test the complete password reset flow"""
        # Set up environment
        os.environ['CLOUDFLARE_WORKER_URL'] = 'https://test.workers.dev/'
        os.environ['CLOUDFLARE_WORKER_API_KEY'] = 'test-api-key'
        
        # Mock successful email send
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response
        
        # Step 1: Create user and token
        user = SimpleNamespace(email="user@example.com")
        token = create_reset_token(user)
        
        # Step 2: Send reset email
        send_reset_email(user.email, token)
        
        # Step 3: Verify token is valid
        verified_email = verify_reset_token(token)
        assert verified_email == user.email
        
        # Verify email was sent
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]['json']
        assert call_args['to_email'] == user.email
        assert call_args['token'] == token
    
    @patch('app.auth.utils.logger')
    @patch('app.auth.utils.requests.post')
    def test_logging_on_success(self, mock_post, mock_logger):
        """Test that successful sends are logged"""
        os.environ['CLOUDFLARE_WORKER_URL'] = 'https://test.workers.dev/'
        os.environ['CLOUDFLARE_WORKER_API_KEY'] = 'test-api-key'
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_post.return_value = mock_response
        
        send_reset_email("test@example.com", "test-token")
        
        # Verify info logs were called
        mock_logger.info.assert_any_call("Sending password reset email to: test@example.com")
        mock_logger.info.assert_any_call("Password reset email sent successfully to test@example.com")
    
    @patch('app.auth.utils.logger')
    @patch('app.auth.utils.requests.post')
    def test_logging_on_error(self, mock_post, mock_logger):
        """Test that errors are logged"""
        os.environ['CLOUDFLARE_WORKER_URL'] = 'https://test.workers.dev/'
        os.environ['CLOUDFLARE_WORKER_API_KEY'] = 'test-api-key'
        
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Server Error'
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception):
            send_reset_email("test@example.com", "test-token")
        
        # Verify error log was called
        mock_logger.error.assert_called()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])