from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

# Создаем все таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость для получения сессии базы данных


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/students/", response_model=list[schemas.Student])
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students


# CRUD для студентов
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(name=student.name, surname=student.surname)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.patch("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, updated_student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    for var, value in vars(updated_student).items():
        if value is not None:
            setattr(student, var, value)
    db.commit()
    db.refresh(student)
    return student


@app.delete("/students/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return student


# CRUD для оценок
@app.post("/score/", response_model=schemas.Score)
def create_score(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    db_score = models.Score(**score.dict())
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


@app.get("/score/{score_id}", response_model=schemas.Score)
def read_score(score_id: int, db: Session = Depends(get_db)):
    score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return score


@app.patch("/score/{score_id}", response_model=schemas.Score)
def update_score(score_id: int, updated_score: schemas.ScoreUpdate, db: Session = Depends(get_db)):
    score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    for var, value in vars(updated_score).items():
        if value is not None:
            setattr(score, var, value)
    db.commit()
    db.refresh(score)
    return score


@app.delete("/score/{score_id}", response_model=schemas.Score)
def delete_score(score_id: int, db: Session = Depends(get_db)):
    score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    db.delete(score)
    db.commit()
    return score
