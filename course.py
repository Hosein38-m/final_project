"""
FastAPI application for managing courses and masters.

This application provides endpoints to perform CRUD operations on courses (lessons) and masters.
It includes validation checks for creating and updating courses and masters.

Endpoints:
- GET /getcsr/{CID}: Retrieve course information by course ID.
- POST /Creatcsr: Create a new course.
- PATCH /uptcsr/{CID}: Update an existing course.
- DELETE /Delcsr/{CID}: Delete a course by course ID.

Dependencies:
- FastAPI: Web framework for building APIs with Python.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) for Python.
- uvicorn: ASGI server implementation, used to run the FastAPI application.
"""
import re
import time
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from dtool import schemas, crud, model, validators
from db import engine, SessionLocal


app = FastAPI()
router = APIRouter()

model.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Provides a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/getcsr/{CID}", response_model= schemas.Lesson, tags= ["Course"], summary= "Get Course", description="Getting course information")
def get_csr(CID: int, db: session = Depends(get_db)):
    """
    Retrieve course information by course ID (CID).
    Args:
        CID (int): Course ID.
        db (session): Database session dependency.
    Returns:
        schemas.Lesson: Course information.
    """
    get_ls = crud.get_lsn(db, CID)
    return get_ls


@app.post("/creatcsr", response_model= schemas.Lesson, tags= ["Course"], summary= "Create Course", description="Create a course ")
def course(ln: schemas.Lesson, db: session = Depends(get_db)):
    """
    Create a new course with validation checks.
    Args:
        ln (schemas.Lesson): Course information.
        db (session): Database session dependency.
    Returns:
        schemas.Lesson: Created course.
    """
    errors = {}
    db_std = db.query(model.Lesson).filter(model.Lesson.CID == ln.CID).first()
    if db_std :
        raise HTTPException(status_code= 400, detail="courseID already exists ,courseID must be unique")
    if len(str(ln.CID)) != 5 :
        errors["CID"] = "CID must be 5 digits"
    if len(ln.CName) > 25 or  not validators.check_farsi_name(ln.CName):
        errors["CName"] = "The maximum length of the string should be 25 and all characters should be Farsi"
    if not validators.college_trust(ln.Department):
        errors["Department"] = "name college is wrong"
    if not re.match(r"[1-5]", ln.Credit):
        errors["credit"] = "The number of units must be between 1 and 4"
    if errors:
        raise HTTPException(status_code = 400, detail={"detail": "Validation error", "errors": errors})
    else:
        db_user = crud.create_lesson(db, ln)
        return db_user

@router.patch("/uptcsr/{CID}", response_model=schemas.UpdateLesson, tags= ["Course"], summary= "Update Course", description= "Update a course")
def upt_cour(CID: int, ln : schemas.UpdateLesson, db: session = Depends(get_db)):
    """
    Update existing course information.
    Args:
        CID (int): Course ID.
        ln (schemas.UpdateLesson): Updated course information.
        db (session): Database session dependency.
    Returns:
        schemas.UpdateLesson: Updated course information.
    """
    cour_que = db.query(model.Lesson).filter(CID == model.Lesson.CID).first()
    if cour_que is None:
        raise HTTPException( status_code= 400, detail= "CID is not found")
    errors = {}
    update_data = ln.model_dump(exclude_unset= True)
    if "CName" in update_data and (len(ln.CName) > 25 or  not validators.check_farsi_name(ln.CName)):
        errors["CName"] = "The maximum length of the string should be 25 and all characters should be Farsi"
    if "Department" in update_data and not validators.college_trust(ln.Department):
        errors["Department"] = "name college is wrong"
    if "Credit" in update_data and (not re.match(r"[1-5]", ln.Credit)):
        errors["credit"] = "The number of units must be between 1 and 4"
    if errors :
        raise HTTPException(status_code=400, detail={"detail": "Validation error", "errors": errors})
    result = crud.update_course(db, CID, update_data)
    return result

app.include_router(router)

@app.delete("/Delcsr/{CID}", tags= ["Course"], summary= "Delete Course", description= "Delete a course")
def del_lsn(CID: int, db: session = Depends(get_db)):
    """
    Delete a course by course ID (CID).
    Args:
        CID (int): Course ID.
        db (session): Database session dependency.
    Returns:
        dict: Confirmation message for deletion.
    """
    del_ls = crud.del_lsn(db, CID)
    return del_ls

def long_running_process():
    """
    Simulate a long-running process with the ability to interrupt and clean up.
    """
    try:
        print("Performing a long-running process. Press Ctrl+C to interrupt.")
        for i in range(5):
            time.sleep(1)
            print(f"Processing step {i + 1}")
    except KeyboardInterrupt:
        print("\nInterrupted! Cleaning up before exiting.")
    finally:
        print("Exiting the program.")

if __name__ == "__main__":
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        long_running_process()
