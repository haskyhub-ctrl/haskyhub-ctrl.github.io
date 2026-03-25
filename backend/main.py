import os
import sys
from dotenv import load_dotenv

load_dotenv()  # Load .env file for API keys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import engine, Base, SessionLocal, migrate_db
from models import (
    User, QuestionCategory, Question, QuestionOption, Recommendation
)
from middleware.auth_middleware import hash_password

# Import routers
from routers import auth, survey, questions, assessments, admin, ai_analysis, export, aggregate, import_users, image_analysis, notifications, improvement


def seed_database():
    """Seed the database with initial data if empty."""
    from seed_data import (
        COMMON_CATEGORIES, ALL_COMMON_QUESTIONS, FACILITY_TYPES
    )
    from seed_data_specific import ALL_SPECIFIC_CATEGORIES
    from seed_recommendations import generate_recommendations_for_option

    db = SessionLocal()
    try:
        if db.query(QuestionCategory).count() > 0:
            return
        
        print("🔥 Seeding database with initial data...")
        
        # Create superadmin
        admin_user = User(
            email="admin@fras.vn",
            password_hash=hash_password("admin123"),
            full_name="Quản trị viên",
            organization="FRAS System",
            role="superadmin",
        )
        db.add(admin_user)
        db.flush()
        
        # ==================== COMMON CATEGORIES (Groups 1-8) ====================
        cat_objects = []
        for cat_data in COMMON_CATEGORIES:
            cat = QuestionCategory(
                name=cat_data["name"],
                description=cat_data["description"],
                icon=cat_data["icon"],
                color=cat_data["color"],
                order_index=cat_data["order_index"],
                max_score=cat_data["max_score"],
                weight=1.0,
            )
            db.add(cat)
            db.flush()
            cat_objects.append(cat)
        
        # ==================== COMMON QUESTIONS ====================
        question_count = 0
        for cat_idx, questions in ALL_COMMON_QUESTIONS:
            cat = cat_objects[cat_idx]
            for q_idx, q_data in enumerate(questions):
                question_count += 1
                q = Question(
                    category_id=cat.id,
                    question_text=q_data["text"],
                    question_type="single",
                    facility_type="all",
                    order_index=question_count,
                    created_by=admin_user.id,
                )
                db.add(q)
                db.flush()
                
                for i, opt in enumerate(q_data["options"]):
                    db_opt = QuestionOption(
                        question_id=q.id,
                        option_key=opt["key"],
                        option_text=opt["text"],
                        score=opt["score"],
                        risk_level=opt["risk"],
                        order_index=i + 1,
                    )
                    db.add(db_opt)
                    db.flush()
                    
                    # Generate recommendations for risky options
                    if opt["score"] >= 2:
                        generate_recommendations_for_option(db, db_opt, opt, cat_data["name"])
        
        # ==================== SPECIFIC CATEGORIES (Groups A-L) ====================
        specific_order = len(COMMON_CATEGORIES) + 1
        for spec_cat_data in ALL_SPECIFIC_CATEGORIES:
            spec_cat = QuestionCategory(
                name=spec_cat_data["name"],
                description=spec_cat_data["description"],
                icon=spec_cat_data["icon"],
                color=spec_cat_data["color"],
                order_index=specific_order,
                weight=1.0,
            )
            db.add(spec_cat)
            db.flush()
            specific_order += 1
            
            max_score = 0
            for q_idx, q_data in enumerate(spec_cat_data["questions"]):
                question_count += 1
                q = Question(
                    category_id=spec_cat.id,
                    question_text=q_data["text"],
                    question_type="single",
                    facility_type=spec_cat_data["facility_type"],
                    order_index=question_count,
                    created_by=admin_user.id,
                )
                db.add(q)
                db.flush()
                
                q_max = 0
                for i, opt in enumerate(q_data["options"]):
                    db_opt = QuestionOption(
                        question_id=q.id,
                        option_key=opt["key"],
                        option_text=opt["text"],
                        score=opt["score"],
                        risk_level=opt["risk"],
                        order_index=i + 1,
                    )
                    db.add(db_opt)
                    db.flush()
                    q_max = max(q_max, opt["score"])
                    
                    # Generate recommendations for risky options
                    if opt["score"] >= 2:
                        generate_recommendations_for_option(db, db_opt, opt, spec_cat_data["name"])
                max_score += q_max
            
            spec_cat.max_score = max_score
        
        db.commit()
        print(f"✅ Seeded {question_count} questions ({len(COMMON_CATEGORIES)} common + {len(ALL_SPECIFIC_CATEGORIES)} specific categories)")
        print(f"✅ Admin account: admin@fras.vn / admin123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Seed error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    # Migrate: add new columns to existing tables
    migrate_db()
    seed_database()
    yield
    # Shutdown


app = FastAPI(
    title="FRAS - Hệ thống Đánh giá Nguy cơ Cháy Nổ",
    description="FireRisk Assessment System API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(survey.router)
app.include_router(questions.router)
app.include_router(assessments.router)
app.include_router(admin.router)
app.include_router(ai_analysis.router)
app.include_router(export.router)
app.include_router(aggregate.router)
app.include_router(import_users.router)
app.include_router(image_analysis.router)
app.include_router(notifications.router)
app.include_router(improvement.router)

# Serve uploaded files
uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
    
    img_dir = os.path.join(frontend_dir, "img")
    if os.path.exists(img_dir):
        app.mount("/img", StaticFiles(directory=img_dir), name="img")
    
    admin_dir = os.path.join(frontend_dir, "admin")
    if os.path.exists(admin_dir):
        app.mount("/admin", StaticFiles(directory=admin_dir, html=True), name="admin")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

    @app.get("/{page}.html")
    async def serve_page(page: str):
        file_path = os.path.join(frontend_dir, f"{page}.html")
        if os.path.exists(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dir, "index.html"))


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "FRAS", "version": "1.0.0"}
