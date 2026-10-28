import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime,
    ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship, backref
from database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(200), unique=True, nullable=False, index=True)
    facility_code = Column(String(20), unique=True, nullable=True, index=True)
    password_hash = Column(String(200), nullable=False)
    full_name = Column(Text, nullable=False)
    organization = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    province = Column(String(100), nullable=True)
    ward = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    facility_types = Column(String(500), nullable=True)  # comma-separated
    management_team = Column(String(300), nullable=True, index=True)   # đội quản lý (từ danh sách cơ sở)
    facility_type_label = Column(String(300), nullable=True)           # loại hình gốc trong danh sách
    land_area = Column(Float, nullable=True)                           # tổng diện tích khu đất (m2)
    built_area = Column(Float, nullable=True)                          # tổng diện tích xây dựng (m2)
    workers_office = Column(Integer, nullable=True)                    # người làm việc trong giờ hành chính
    workers_after = Column(Integer, nullable=True)                     # người làm việc ngoài giờ hành chính
    role = Column(String(20), default="user")  # user, admin, superadmin
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assessments = relationship("Assessment", back_populates="user")
    audit_logs = relationship("AdminAuditLog", back_populates="admin")


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    max_score = Column(Integer, default=0)
    weight = Column(Float, default=1.0)
    order_index = Column(Integer, default=0)
    icon = Column(String(50), nullable=True)
    color = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", back_populates="category")
    category_scores = relationship("CategoryScore", back_populates="category")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), default="single")  # single, multiple, scale
    facility_type = Column(String(50), default="all")
    is_conditional = Column(Boolean, default=False)
    condition_question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    condition_answer = Column(String(10), nullable=True)
    help_text = Column(Text, nullable=True)
    reference = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("QuestionCategory", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("AssessmentAnswer", back_populates="question")


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option_key = Column(String(5), nullable=False)
    option_text = Column(Text, nullable=False)
    score = Column(Integer, nullable=False, default=0)
    risk_level = Column(String(20), default="safe")  # safe, low, medium, high, critical
    order_index = Column(Integer, default=0)

    question = relationship("Question", back_populates="options")
    recommendations = relationship("Recommendation", back_populates="question_option")
    selected_in_answers = relationship("AssessmentAnswer", back_populates="selected_option")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    facility_name = Column(String(200), nullable=False)
    facility_type = Column(String(50), nullable=True)
    facility_address = Column(Text, nullable=True)
    facility_area = Column(Float, nullable=True)
    worker_count = Column(Integer, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    total_score = Column(Integer, default=0)
    max_possible_score = Column(Integer, default=0)
    risk_level = Column(String(20), default="low")
    risk_percentage = Column(Float, default=0.0)
    status = Column(String(20), default="in_progress")  # in_progress, completed, archived
    is_demo = Column(Boolean, default=False)  # Flag dữ liệu mẫu, dễ xóa hàng loạt
    ai_analysis = Column(Text, nullable=True)
    mitigation_data = Column(Text, nullable=True)
    tracking_code = Column(String(16), nullable=True, index=True)  # mã theo dõi cho người khảo sát không tài khoản
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessments")
    answers = relationship("AssessmentAnswer", back_populates="assessment", cascade="all, delete-orphan")
    category_scores = relationship("CategoryScore", back_populates="assessment", cascade="all, delete-orphan")
    image_analyses = relationship("ImageAnalysis", back_populates="assessment", cascade="all, delete-orphan")
    improvement_plans = relationship("ImprovementPlan", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String(36), ForeignKey("assessments.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("question_options.id"), nullable=True)
    score_obtained = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    selected_option = relationship("QuestionOption", back_populates="selected_in_answers")


class CategoryScore(Base):
    __tablename__ = "category_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String(36), ForeignKey("assessments.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=False)
    score_obtained = Column(Integer, default=0)
    max_score = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)
    risk_level = Column(String(20), default="low")

    assessment = relationship("Assessment", back_populates="category_scores")
    category = relationship("QuestionCategory", back_populates="category_scores")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_option_id = Column(Integer, ForeignKey("question_options.id"), nullable=False)
    recommendation_text = Column(Text, nullable=False)
    priority = Column(String(20), default="medium")  # urgent, high, medium, low
    deadline_days = Column(Integer, default=30)
    legal_reference = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    question_option = relationship("QuestionOption", back_populates="recommendations")


class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    target_type = Column(String(50), nullable=True)
    target_id = Column(String(100), nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    admin = relationship("User", back_populates="audit_logs")


class QuestionTemplate(Base):
    __tablename__ = "question_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    template_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    template_data = Column(Text, nullable=True)  # JSON
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ImageAnalysis(Base):
    __tablename__ = "image_analyses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    assessment_id = Column(String(36), ForeignKey("assessments.id"), nullable=True)
    image_filename = Column(String(500), nullable=False)
    analysis_result = Column(Text, nullable=True)  # JSON from Gemini Vision
    overall_risk = Column(String(20), default="unknown")
    hazards_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="image_analyses")
    assessment = relationship("Assessment", back_populates="image_analyses")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    notification_type = Column(String(50), nullable=False)  # high_risk, reminder, improvement
    title = Column(String(300), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String(500), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref=backref("notifications", cascade="all, delete-orphan"))


class ImprovementPlan(Base):
    __tablename__ = "improvement_plans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    assessment_id = Column(String(36), ForeignKey("assessments.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(300), nullable=False)
    status = Column(String(20), default="active")  # active, completed, cancelled
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    progress = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="improvement_plans")
    user = relationship("User", backref="improvement_plans")
    tasks = relationship("ImprovementTask", back_populates="plan", cascade="all, delete-orphan")


class ImprovementTask(Base):
    __tablename__ = "improvement_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(String(36), ForeignKey("improvement_plans.id"), nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), default="medium")  # urgent, high, medium, low
    status = Column(String(20), default="pending")  # pending, in_progress, completed
    deadline_days = Column(Integer, default=30)
    evidence_file = Column(String(500), nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    plan = relationship("ImprovementPlan", back_populates="tasks")


class FireReport(Base):
    __tablename__ = "fire_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    phone = Column(String(20), nullable=False)
    location_address = Column(String(500), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    fire_type = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    status = Column(String(30), default="received")  # received, verified, dispatching, resolved, false_alarm
    created_at = Column(DateTime, default=datetime.utcnow)



class KbQuestion(Base):
    """Câu hỏi khó của người dân hỏi Trợ lý Chi, và đáp án chuẩn do cán bộ duyệt.

    status: pending (chưa có đáp án), approved (đáp án đã duyệt, được ưu tiên trả lời), rejected (bỏ qua).
    """
    __tablename__ = "kb_questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question = Column(Text, nullable=False)
    question_key = Column(String(500), index=True)          # khóa chuẩn hóa để gộp các câu hỏi giống nhau
    answer = Column(Text, nullable=True)
    status = Column(String(20), default="pending", index=True)
    times_asked = Column(Integer, default=1)
    source = Column(String(20), default="chat")             # chat (bot chưa đủ căn cứ) hoặc admin (cán bộ nhập)
    last_asked_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    answered_at = Column(DateTime, nullable=True)
    answered_by = Column(String(36), nullable=True)


class LawCandidate(Base):
    """Văn bản, bài viết mới về PCCC tìm được trên mạng, chờ cán bộ rà soát trước khi đưa vào kho."""
    __tablename__ = "law_candidates"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    url = Column(String(900), nullable=False, unique=True, index=True)
    title = Column(String(500), nullable=False)
    snippet = Column(Text, nullable=True)
    source = Column(String(120), nullable=True)
    published = Column(String(30), nullable=True)
    found_at = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(20), default="new", index=True)       # new, ingested, ignored
    relevant = Column(Boolean, nullable=True)
    kind = Column(String(60), nullable=True)
    summary = Column(Text, nullable=True)
    hint = Column(String(300), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    kho_doc_id = Column(String(120), nullable=True)


class Feedback(Base):
    """Hòm thư góp ý, phản ánh bất cập hoặc kiến nghị an toàn PCCC từ người dân/cơ sở."""
    __tablename__ = "feedbacks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    feedback_code = Column(String(20), unique=True, nullable=False, index=True)  # Mã tra cứu: GY261026-ABCD
    sender_name = Column(String(150), nullable=True)                              # Họ tên hoặc ẩn danh
    phone = Column(String(20), nullable=True, index=True)
    email = Column(String(200), nullable=True)
    facility_name = Column(String(250), nullable=True)                          # Tên cơ sở / đơn vị
    address = Column(String(300), nullable=True)                                # Phường/Xã, địa chỉ
    category = Column(String(60), default="Góp ý chung", index=True)            # Phân loại góp ý
    title = Column(String(300), nullable=False)                                 # Tiêu đề
    content = Column(Text, nullable=False)                                      # Nội dung phản ánh
    attachment_url = Column(String(500), nullable=True)                         # Link ảnh/tệp đính kèm
    attachment_name = Column(String(255), nullable=True)                        # Tên gốc của tệp
    status = Column(String(30), default="pending", index=True)                  # pending, processing, resolved, rejected
    admin_response = Column(Text, nullable=True)                                # Phản hồi của cán bộ/BQT
    responder_name = Column(String(100), nullable=True)                         # Tên cán bộ phản hồi
    responded_at = Column(DateTime, nullable=True)                              # Thời gian phản hồi
    ip_address = Column(String(60), nullable=True)
    user_id = Column(String(36), nullable=True)                                 # ID user nếu đã đăng nhập
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

