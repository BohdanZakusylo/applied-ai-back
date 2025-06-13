from fastapi import APIRouter, HTTPException, status, Depends
from app.models.auth import (
    UserRegister, 
    UserLogin, 
    Token, 
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
    return AuthResponse(message="User registered successfully")

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT token
    """
    authService = AuthService()
    
    # Authenticate user credentials
    user = await authService.authenticate_user(credentials.email, credentials.password)
    
    # Generate JWT access token
    access_token = await authService.create_access_token(user.id)

    #write token in tthe database
    authService.update_user_token(user_id=user.id, new_token=access_token)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600  # 1 hour
    )

@router.post("/logout", response_model=AuthResponse)
async def logout(current_user: str = Depends(get_current_user)):
    if(current_user):
        authService = AuthService()
        await authService.logout(current_user)
    return AuthResponse(message=f"User logged out successfully")

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