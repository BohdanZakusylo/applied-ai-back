# ITH-85: Improve chat-bot security
# Security measures for chat interactions

import re
import time
from typing import Dict, List
from ..config.ai_config import AIConfig

class ChatSecurity:
    """
    Handles security measures for chat interactions
    """
    
    def __init__(self):
        # Blocked words and phrases for security
        self.blocked_words = [
            "injection", "sql", "script", "exec", "eval", 
            "javascript:", "data:", "vbscript:", "<script",
            "onload", "onerror", "onclick"
        ]
        
        # Rate limiting storage: {user_id: [timestamp1, timestamp2, ...]}
        self.rate_limits = {}
        self.max_requests = AIConfig.RATE_LIMIT_PER_MINUTE
        self.time_window = 60  # seconds
        self.max_message_length = AIConfig.MAX_MESSAGE_LENGTH
    
    def validate_user_input(self, user_id: str, message: str) -> bool:
        """
        Validate user input for security threats
        
        Args:
            user_id: User identifier
            message: User message to validate
            
        Returns:
            True if input is safe, False otherwise
        """
        try:
            # Check message length
            if len(message) > self.max_message_length:
                print(f"Message too long: {len(message)} > {self.max_message_length}")
                return False
            
            # Check for empty or whitespace-only messages
            if not message or not message.strip():
                print("Empty or whitespace-only message")
                return False
            
            # Check for blocked words/patterns
            message_lower = message.lower()
            for blocked_word in self.blocked_words:
                if blocked_word in message_lower:
                    print(f"Blocked word detected: {blocked_word}")
                    return False
            
            # Check for potential injection patterns
            if self._contains_injection_patterns(message):
                print("Potential injection pattern detected")
                return False
            
            # Check for excessive special characters (potential encoding attacks)
            special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s.,!?-]', message)) / len(message)
            if special_char_ratio > 0.3:  # More than 30% special characters
                print(f"Too many special characters: {special_char_ratio:.2%}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating user input: {e}")
            return False
    
    def check_rate_limit(self, user_id: str) -> bool:
        """
        Check if user is within rate limits
        
        Args:
            user_id: User identifier
            
        Returns:
            True if within limits, False if exceeded
        """
        try:
            current_time = time.time()
            
            # Initialize user rate limit tracking if not exists
            if user_id not in self.rate_limits:
                self.rate_limits[user_id] = []
            
            user_requests = self.rate_limits[user_id]
            
            # Remove old requests outside the time window
            user_requests[:] = [req_time for req_time in user_requests 
                               if current_time - req_time < self.time_window]
            
            # Check if user has exceeded rate limit
            if len(user_requests) >= self.max_requests:
                print(f"Rate limit exceeded for user {user_id}: {len(user_requests)}/{self.max_requests}")
                return False
            
            # Add current request
            user_requests.append(current_time)
            return True
            
        except Exception as e:
            print(f"Error checking rate limit: {e}")
            return True  # Default to allowing if error occurs
    
    def sanitize_response(self, response: str) -> str:
        """
        Sanitize AI response before sending to user
        
        Args:
            response: Generated AI response
            
        Returns:
            Sanitized response
        """
        try:
            if not response:
                return "I'm sorry, I couldn't generate a response."
            
            # Remove any potential HTML/JS content
            response = re.sub(r'<[^>]*>', '', response)
            
            # Remove potential script injection patterns
            response = re.sub(r'javascript:', '', response, flags=re.IGNORECASE)
            response = re.sub(r'data:', '', response, flags=re.IGNORECASE)
            response = re.sub(r'vbscript:', '', response, flags=re.IGNORECASE)
            
            # Remove excessive whitespace
            response = re.sub(r'\s+', ' ', response).strip()
            
            # Ensure response is not empty after sanitization
            if not response or not response.strip():
                return "I'm sorry, I couldn't generate a proper response."
            
            # Truncate if too long
            max_response_length = 2000
            if len(response) > max_response_length:
                response = response[:max_response_length] + "..."
            
            return response
            
        except Exception as e:
            print(f"Error sanitizing response: {e}")
            return "I'm sorry, there was an error processing the response."
    
    def _contains_injection_patterns(self, message: str) -> bool:
        """
        Check for common injection attack patterns
        
        Args:
            message: Message to check
            
        Returns:
            True if injection patterns found
        """
        try:
            # SQL injection patterns
            sql_patterns = [
                r"(?i)\b(union|select|insert|update|delete|drop|create|alter)\b.*\b(from|where|table)\b",
                r"(?i)(\-\-|\#|\/\*|\*\/)",
                r"(?i)\b(or|and)\s+\d+\s*=\s*\d+",
                r"(?i)\'\s*(or|and|union)",
            ]
            
            # Command injection patterns
            cmd_patterns = [
                r"(?i)(\;|\||\&\&|\|\|)\s*(cat|ls|dir|type|copy|del|rm|mv)",
                r"(?i)(\$\(|\`|\\x)",
            ]
            
            # XSS patterns
            xss_patterns = [
                r"(?i)<(script|iframe|object|embed|form)",
                r"(?i)(onload|onerror|onclick|onmouseover)\s*=",
                r"(?i)javascript\s*:",
            ]
            
            all_patterns = sql_patterns + cmd_patterns + xss_patterns
            
            for pattern in all_patterns:
                if re.search(pattern, message):
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error checking injection patterns: {e}")
            return False
    
    def get_rate_limit_status(self, user_id: str) -> Dict:
        """
        Get current rate limit status for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Rate limit status information
        """
        try:
            if user_id not in self.rate_limits:
                return {
                    "requests_made": 0,
                    "requests_remaining": self.max_requests,
                    "reset_time": time.time() + self.time_window
                }
            
            current_time = time.time()
            user_requests = self.rate_limits[user_id]
            
            # Count recent requests
            recent_requests = [req_time for req_time in user_requests 
                             if current_time - req_time < self.time_window]
            
            return {
                "requests_made": len(recent_requests),
                "requests_remaining": max(0, self.max_requests - len(recent_requests)),
                "reset_time": min(recent_requests) + self.time_window if recent_requests else current_time
            }
            
        except Exception as e:
            print(f"Error getting rate limit status: {e}")
            return {
                "requests_made": 0,
                "requests_remaining": self.max_requests,
                "reset_time": time.time() + self.time_window
            } 