from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User
from schemas import RegisterSchema, LoginSchema, EditProfileSchema
from auth import hash_password, verify_password, create_token
from recommender import recommend_jobs_from_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Recommendation System")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Register
@app.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        experience=data.experience,
        education=data.education,
        skills=",".join(data.skills)
    )
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

# ✅ Login
@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": user.id})
    return {"access_token": token}

# ✅ Dashboard (Recommended Jobs)
@app.get("/dashboard/{user_id}")
def dashboard(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    return recommend_jobs_from_db(user, db)

# ✅ Edit Profile
@app.put("/edit-profile/{user_id}")
def edit_profile(user_id: int, data: EditProfileSchema, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    user.experience = data.experience
    user.education = data.education
    user.skills = ",".join(data.skills)
    db.commit()
    return {"message": "Profile updated"}
