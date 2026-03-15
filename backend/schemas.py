from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ======================== AUTH SCHEMAS ========================

class UserRegister(BaseModel):
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    organization: Optional[str] = None
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    facility_code: Optional[str] = None
    full_name: str
    organization: Optional[str] = None
    phone: Optional[str] = None
    province: Optional[str] = None
    ward: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    facility_types: Optional[str] = None
    role: str
    is_active: bool
    is_locked: bool
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    organization: Optional[str] = None
    phone: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ======================== CATEGORY SCHEMAS ========================

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    max_score: int = 0
    weight: float = 1.0
    order_index: int = 0
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_score: Optional[int] = None
    weight: Optional[float] = None
    order_index: Optional[int] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ======================== OPTION SCHEMAS ========================

class OptionBase(BaseModel):
    option_key: str
    option_text: str
    score: int = 0
    risk_level: str = "safe"
    order_index: int = 0


class OptionCreate(OptionBase):
    pass


class OptionResponse(OptionBase):
    id: int

    class Config:
        from_attributes = True


# ======================== QUESTION SCHEMAS ========================

class QuestionBase(BaseModel):
    category_id: int
    question_text: str
    question_type: str = "single"
    facility_type: str = "all"
    is_conditional: bool = False
    condition_question_id: Optional[int] = None
    condition_answer: Optional[str] = None
    help_text: Optional[str] = None
    reference: Optional[str] = None
    order_index: int = 0
    is_active: bool = True


class QuestionCreate(QuestionBase):
    options: List[OptionCreate] = []


class QuestionUpdate(BaseModel):
    category_id: Optional[int] = None
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    facility_type: Optional[str] = None
    is_conditional: Optional[bool] = None
    condition_question_id: Optional[int] = None
    condition_answer: Optional[str] = None
    help_text: Optional[str] = None
    reference: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None
    options: Optional[List[OptionCreate]] = None


class QuestionResponse(QuestionBase):
    id: int
    options: List[OptionResponse] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryWithQuestions(CategoryResponse):
    questions: List[QuestionResponse] = []


# ======================== ASSESSMENT SCHEMAS ========================

class AssessmentStart(BaseModel):
    facility_name: str
    facility_type: Optional[str] = None
    facility_address: str = Field(..., min_length=5, description="Địa chỉ cơ sở (bắt buộc)")
    facility_area: Optional[float] = None
    worker_count: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AnswerSubmit(BaseModel):
    assessment_id: str
    question_id: int
    selected_option_id: int


class BulkAnswerSubmit(BaseModel):
    assessment_id: str
    answers: List[AnswerSubmit]


class AnswerResponse(BaseModel):
    id: int
    assessment_id: str
    question_id: int
    selected_option_id: Optional[int] = None
    score_obtained: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryScoreResponse(BaseModel):
    id: int
    category_id: int
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    category_color: Optional[str] = None
    score_obtained: int
    max_score: int
    percentage: float
    risk_level: str

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    id: int
    recommendation_text: str
    priority: str
    deadline_days: int
    legal_reference: Optional[str] = None
    question_text: Optional[str] = None
    category_name: Optional[str] = None

    class Config:
        from_attributes = True


class AssessmentResponse(BaseModel):
    id: str
    user_id: str
    facility_name: str
    facility_type: Optional[str] = None
    facility_address: Optional[str] = None
    facility_area: Optional[float] = None
    worker_count: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    total_score: int
    max_possible_score: int
    risk_level: str
    risk_percentage: float
    status: str
    ai_analysis: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssessmentDetail(AssessmentResponse):
    category_scores: List[CategoryScoreResponse] = []
    recommendations: List[RecommendationResponse] = []
    answers: List[AnswerResponse] = []


# ======================== ADMIN SCHEMAS ========================

class AdminStats(BaseModel):
    total_users: int
    total_assessments: int
    avg_risk_score: float
    high_risk_count: int
    assessments_this_month: int
    new_users_this_month: int


class AuditLogResponse(BaseModel):
    id: int
    admin_id: str
    admin_name: Optional[str] = None
    action: str
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role: str


class UserLockUpdate(BaseModel):
    is_locked: bool
