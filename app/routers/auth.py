from fastapi import APIRouter, HTTPException, status, Depends
from app.models.auth import (
    UserRegister, 
    UserLogin, 
    Token, 
    TokenRefresh, 
    ForgotPassword, 
    ResetPassword, 
    AuthResponse
)
from app.dependencies import get_current_user
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    authService = AuthService();
    await authService.register_user(
        user_data.email, user_data.password, user_data.name, user_data.insurance_provider, user_data.general_practitioner, user_data.medical_information
    )
    return AuthResponse(message="User registered successfully", user_id="placeholder-user-id")

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT token
    """
    # TODO: Implement login logic
    # - Validate credentials against database
    # - Generate JWT access token
    # - Return token with expiration
    return Token(
        access_token="placeholder-jwt-token",
        token_type="bearer",
        expires_in=1800
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh):
    """
    Refresh an expired JWT token
    """
    # TODO: Implement token refresh logic
    # - Validate refresh token
    # - Generate new access token
    return Token(
        access_token="new-placeholder-jwt-token",
        token_type="bearer",
        expires_in=1800
    )

@router.post("/logout", response_model=AuthResponse)
async def logout(current_user: str = Depends(get_current_user)):
    """
    Logout user and invalidate token
    """
    # TODO: Implement logout logic
    # - Add token to blacklist
    # - Clear any server-side session data
    return AuthResponse(message=f"User {current_user} logged out successfully")

@router.post("/forgot-password", response_model=AuthResponse)
async def forgot_password(email_data: ForgotPassword):
    """
    Request password reset code
    """
    authService = AuthService()
    await authService.request_password_reset(email_data.email)
    return AuthResponse(message="Password reset code sent to your email")

@router.post("/reset-password", response_model=AuthResponse)
async def reset_password(reset_data: ResetPassword):
    """
    Reset password using verification code
    """
    authService = AuthService()
    await authService.reset_password_with_code(
        reset_data.email, 
        reset_data.code, 
        reset_data.new_password
    )
    return AuthResponse(message="Password reset successfully") 