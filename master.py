"""
This module defines a FastAPI application for managing professor information. 
It includes endpoints for creating, retrieving, updating, and deleting professor information, 
with various checks to ensure data validity.

Endpoints:
    - /GetMrs/{LID}: Retrieve professor information by ID.
    - /CreateMaster: Create a new professor.
    - /Updmaster/{LID}: Update existing professor information.
    - /DelLsn/{LID}: Delete a professor by ID.

Dependencies:
    - FastAPI
    - SQLAlchemy
    - Uvicorn
    - re
    - time

Functions:
    - get_db: Returns a database session and ensures it is closed after use.
    - get_msr: Retrieve professor information by ID.
    - master: Create a new professor with validation checks.
    - upd_mas: Update existing professor information.
    - del_msr: Delete a professor by ID.
    - long_running_process: Simulate a long-running process with the ability to interrupt and clean up.
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
    Returns a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/GetMrs/{ُLID}", response_model= schemas.MasterOut, tags= ["Master"],summary= "Get Master", description= "Getting professor information")
def get_msr(LID: int, db: session = Depends(get_db)):
    """
    Retrieve professor information by ID.
    Args:
        LID (int): Professor ID.
        db (session): Database session dependency.
    Returns:
        schemas.MasterOut: Professor information.
    """
    get_ms = crud.get_msr(db, LID)
    return get_ms


@app.post("/CreateMaster", response_model= schemas.Master, tags= ["Master"],summary= "Create Master", description= "Create a master user")
def master(mr: schemas.Master, db: session = Depends(get_db)):
    """
    Create a new professor with validation checks.
    Args:
        mr (schemas.Master): Professor information.
        db (session): Database session dependency.
    Returns:
        schemas.Master: Created professor.
    """
    errors = {}
    db_mr = db.query(model.Master).filter(mr.LID == model.Master.LID).first()
    if db_mr:
        raise HTTPException(status_code=400, detail= f"This teacher exists with the number {mr.LID}")
    if len(str(mr.LID)) != 6:
        errors["LID"] = "The number of digits entered is incorrect"
    if not validators.check_farsi_name(mr.FName):
        errors["FName"] = "All letters must be Farsi or Do not contain special symbols or numbers"
    if not validators.check_farsi_name(mr.LName):
        errors["LName"] = "All letters must be Farsi or Do not contain special symbols or numbers"
    if len(mr.FName) > 10 or len(mr.LName) > 10 :
        errors["FName or LName"] = "The maximum string length must be ten"
    if not validators.validate_national_id(mr.ID):
        errors["ID"] = "code melli is incorrect"
    if not validators.college_trust(mr.Department):
        errors["Department"] = "name college is wrong"
    if not validators.trust(mr.Major):
        errors["Major"] = "field of study is wrong"
    if not validators.check_shamsi(mr.Birth):
        errors["Birth"] = "This date is incorrect"
    if not validators.is_cities(mr.BornCity):
        errors["BornCity"] = "incorrect province"
    if 100 < len(mr.Address):
        errors["Address"] = "address incorrectly"
    if len(str(mr.PostalCode)) != 10:
        errors["PostalCode"] = "postal code is invalued"
    if not bool(re.match(r"((0?9)|(\+?989))\d{2}\W?\d{3}\W?\d{4}", mr.CPhone)):
        errors["CPhone"] = "Mobile phone number must be start with 09 and 11 digits"
    if len(str(mr.HPhone)) != 11:
        errors["HPhone"] = "landline number must be 11 digits"
    if not bool(re.findall(r"^(066)", mr.HPhone)):
        errors["landline_number"] = "is landline number incorrect "
    if mr.LCourseIDs:
        for course in mr.LCourseIDs:
                db_lcourse = db.query(model.Lesson).filter(course == model.Lesson.CID).first()
                if not db_lcourse:
                    errors["LCourseIDs"] = f"Lesson with ID {course} not found"
    if errors:
        raise HTTPException(status_code = 400, detail={"detail": "Validation error", "errors": errors})
    else:
        db_user = crud.create_master(db, mr)
        return db_user


@router.patch("/Updmaster/{LID}", response_model= schemas.UpdateMaster, tags= ["Master"],summary= "Update Master", description= "Update a master user")
def upd_mas(LID: int, mr: schemas.UpdateMaster, db: session = Depends(get_db)):
    """
    Update existing professor information.
    Args:
        LID (int): Professor ID.
        mr (schemas.UpdateMaster): Updated professor information.
        db (session): Database session dependency.
    Returns:
        schemas.UpdateMaster: Updated professor information.
    """
    errors = {}
    mr1 = db.query(model.Master).filter(LID == model.Master.LID).first()
    if not mr1 :
        raise HTTPException(status_code= 404, detail= "There is no such master")
    update_data = mr.model_dump(exclude_unset= True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    if "FName" in update_data:
        if not validators.check_farsi_name(mr.FName):
            errors["FName"] = "All letters must be Farsi or Do not contain special symbols or numbers"
        if len(mr.FName) > 10:
            errors["FName"] = "The maximum string length must be ten"
    if "LName" in update_data:
        if not validators.check_farsi_name(mr.LName):
            errors["LName"] = "All letters must be Farsi or Do not contain special symbols or numbers"
        if len(mr.LName) > 10:
            errors["LName"] = "The maximum string length must be ten"
    if "ID" in update_data and not validators.validate_national_id(mr.ID):
        errors["ID"] = "code melli is incorrect"
    if "Department" in update_data and not validators.college_trust(mr.Department):
        errors["Department"] = "name college is wrong"
    if "Major" in update_data and not validators.trust(mr.Major):
        errors["Major"] = "field of study is wrong"
    if "Birth" in update_data and not validators.check_shamsi(mr.Birth):
        errors["Birth"] = "This date is incorrect"
    if "BornCity" in update_data and not validators.is_cities(mr.BornCity):
        errors["BornCity"] = "incorrect province"
    if "Address" in update_data and 100 < len(mr.Address):
        errors["address"] = "address incorrectly"
    if "PostalCode" in update_data and len(str(mr.PostalCode)) != 10:
        errors["PostalCode"] = "postal code is invalued"
    if "CPhone" in update_data and len(str(mr.CPhone)) != 11:
        errors["CPhone"] = "Mobile phone number must be 11 digits"
    if "CPhone" in update_data and not bool(re.findall(r"^(09)", mr.CPhone)):
        errors["CPhone1"] = "Mobile phone number must be start with 09"
    if "HPhone" in update_data and len(str(mr.HPhone)) != 11:
        errors["HPhone"] = "landline number must be 11 digits"
    if "HPhone" in update_data and not bool(re.findall(r"^(066)", mr.HPhone)):
        errors["HPhone1"] = "is landline number incorrect "
    if mr.LCourseIDs:
        for course in mr.LCourseIDs:
                db_lcourse = db.query(model.Lesson).filter(course == model.Lesson.CID).first()
                if not db_lcourse:
                    errors["LCourseIDs"] = f"Lesson with ID {course} not found"
    if errors:
        raise HTTPException(status_code=400, detail={"detail": "Validation error", "errors": errors})
    result = crud.update_master(db, LID, update_data)
    return result

app.include_router(router)


@app.delete("/DelLsn/{LID}", tags= ["Master"],summary= "Delete Master", description= "Delete a master user")
def del_msr(LID: int, db: session = Depends(get_db)):
    """
    Delete a professor by ID.
    Args:
        LID (int): Professor ID.
        db (session): Database session dependency.
    Returns:
        dict: Confirmation message for deletion.
    """
    del_ms = crud.del_msr(db, LID)
    return del_ms

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
