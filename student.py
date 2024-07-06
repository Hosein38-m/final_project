"""
This module defines a FastAPI application for managing student records. It includes
endpoints for creating, retrieving, updating, and deleting student information, with
various validation checks to ensure data integrity.

Endpoints:
    - /GetStu/{STID}: Retrieve a student by their ID.
    - /RegStu: Create a new student.
    - /UpdStu/{STID}: Update an existing student's information.
    - /DelStu/{STID}: Delete a student by their ID.

Dependencies:
    - FastAPI
    - SQLAlchemy
    - Uvicorn
    - re
    - time

Functions:
    - get_db: Yields a database session and ensures it is closed after use.
    - get_std: Retrieve a student by their ID.
    - create_std: Create a new student with validation checks.
    - update_std: Update an existing student's information.
    - del_std: Delete a student by their ID.
    - long_running_process: Simulates a long-running process, allowing interruption with cleanup.
"""
import re
import time
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import session
from dtool import model, schemas, crud, validators
from db import engine, SessionLocal


model.Base.metadata.create_all(bind=engine)

router = APIRouter()
app = FastAPI()



def get_db():
    """Yields a database session and ensures it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/GetStu/{ُSTID}", response_model=schemas.Student, tags= ["Student"], summary= "Get Student", description= "Getting a student information")
def get_std(STID: int, db: session = Depends(get_db)):
    """
    Retrieve a student by their ID.
    Args:
        STID (int): The ID of the student to retrieve.
        db (session): Database session dependency.
    Returns:
        schemas.Student: The retrieved student.
    """
    get_st = crud.get_student(db, STID)
    return get_st


@app.post("/RegStu", response_model= schemas.Student, tags= ["Student"], summary= "Create Student", description= "Create a student user")
def create_std(users: schemas.Student, db: session = Depends(get_db)):
    """
    Create a new student with validation checks.
    Args:
        users (schemas.Student): The student data to create.
        db (session): Database session dependency.
    Returns:
        schemas.Student: The created student.
    """
    errors = {}
    for course in users.SCourseIDs:
        db_lcourse = db.query(model.Lesson).filter(course == model.Lesson.CID).first()
        if not db_lcourse:
            errors["Lcourse"] = f"Lesson with ID {course} not found"
    for master in users.LIDs:
        db_master = db.query(model.Master).filter(model.Master.LID == master).first()
        if not db_master:
            errors["LID"] = f"Master with ID {master} not found"

    db_std = db.query(model.Student).filter(model.Student.STID == users.STID).first()
    if db_std :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="studentID already exists ,studentID must be unique")

    if len(str(users.STID)) != 11:
        errors["STID"] = "The number of digits entered is incorrect"
    if not bool(re.match(r"^(402|401|400)", str(users.STID))):
        errors["STID1"] = "The year field is incorrect"
    if not bool(re.match(r"...114150..", str(users.STID))):
        errors["STID2"] = "The fixed field is wrong"
    if len(str(users.STID)) == 11 and not 99 >= int(str(users.STID)[9:11]) >= 1:
        errors["STID3"] = "The index part is wrong"
    if not (validators.check_farsi_name(users.FName)and validators.check_farsi_name(users.LName) and validators.check_farsi_name(users.Father)):
        errors["name"] = "All letters must be Farsi or Do not contain special symbols or numbers"
    if len(users.FName) > 10 or len(users.LName) > 10 or len(users.Father) > 10:
        errors["name2"] = "The maximum string length must be ten"
    if not validators.check_shamsi(users.Birth):
        errors["Birth"] = "This date is incorrect"
    if  not re.match(r"([\u0627][\u0644][\u0641]|[\u0628-\u06CC])[\/][0-9]{2}\s{1}[0-9]{6}", users.IDS) :
        errors["IDS"] = "The letter part of the birth certificate was entered incorrectly"
    if not validators.is_cities(users.BornCity):
        errors["BornCity"] = "incorrect province"
    if 100 < len(users.Address):
        errors["address"] = "address incorrectly"
    if not validators.check_farsi_name(users.Address) :
        errors["address1"] = "address must be farsi"
    if len(str(users.PostalCode)) != 10:
        errors["postal_code"] = "postal code is invalued"
    if not bool(re.match(r"((0?9)|(\+?989))\d{2}\W?\d{3}\W?\d{4}", users.CPhone)):
        errors["CPhone"] = "Mobile phone number must be start with 09 and 11 digits"
    if len(str(users.HPhone)) != 11:
        errors["landline_number"] = "landline number must be 11 digits"
    if not bool(re.findall(r"^(066)", users.HPhone)):
        errors["landline_number"] = "is landline number incorrect "
    if not validators.college_trust(users.Department):
        errors["name_college"] = "name college is wrong"
    if not validators.trust(users.Major):
        errors["field_study"] = "field of study is wrong"
    if not (users.Married == "متاهل" or users.Married == "مجرد"):
        errors["marital"] = "is marital status is wrong value"
    if not validators.validate_national_id(users.ID):
        errors["code_melli"] = "code melli is incorrect"

    if errors:
        raise HTTPException(status_code = 400, detail={"detail": "Validation error", "errors": errors})
    else:
        db_user = crud.create_student(db, users)
        return db_user



@router.patch("/UpdStu/{STID}", tags= ["Student"], summary= "Update Student", description= "Update a student user")
def update_std(STID: int, student_update: schemas.UpdateStudent, db: session = Depends(get_db)):
    """
    Update an existing student's information.
    Args:
        STID (int): The ID of the student to update.
        student_update (schemas.UpdateStudent): The updated student data.
        db (session): Database session dependency
    Returns:
        schemas.Student: The updated student data.
    """
    update_data = student_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    errors = {}
    if "FName" in update_data and not validators.check_farsi_name(update_data["FName"]):
        errors["FName"] = "All letters must be Farsi or Do not contain special symbols or numbers"
    if "LName" in update_data and not validators.check_farsi_name(update_data["LName"]):
        errors["LName"] = "All letters must be Farsi or Do not contain special symbols or numbers"
    if "Father" in update_data and not validators.check_farsi_name(update_data["Father"]):
        errors["Father"] = "All letters must be Farsi or Do not contain special symbols or numbers"
    if "FName" in update_data and len(update_data["FName"]) > 10:
        errors["FName1"] = "The maximum string length must be ten"
    if "LName" in update_data and len(update_data["LName"]) > 10:
        errors["LName1"] = "The maximum string length must be ten"
    if "Father" in update_data and len(update_data["Father"]) > 10:
        errors["Father1"] = "The maximum string length must be ten"
    if "Birth" in update_data and not validators.check_shamsi(update_data["Birth"]):
        errors["Birth"] = "This date is incorrect"
    if "IDS" in update_data and not bool(re.match(r"([\u0627][\u0644][\u0641]|[\u0628-\u06CC])[\/][0-9]{2}\s{1}[0-9]{6}", update_data["IDS"])):
        errors["IDS"] = "The letter part of the birth certificate was entered incorrectly"
    if "BornCity" in update_data and not validators.is_cities(update_data["BornCity"]):
        errors["BornCity"] = "incorrect province"
    if "Address" in update_data and 100 < len(update_data["Address"]):
        errors["address"] = "address incorrectly"
    if "PostalCode" in update_data and len(str(update_data["PostalCode"])) != 10:
        errors["postal_code"] = "postal code is invalued"
    if "CPhone" in update_data and not bool(re.match(r"((0?9)|(\+?989))\d{2}\W?\d{3}\W?\d{4}", update_data["CPhone"])):
        errors["CPhone"] = "Mobile phone number must be start with 09"
    if "HPhone" in update_data and len(str(update_data["HPhone"])) != 11:
        errors["HPhone"] = "landline number must be 11 digits"
    if "HPhone" in update_data and not bool(re.findall(r"^(066)", update_data["HPhone"])):
        errors["HPhone1"] = "is landline number incorrect "
    if "Department" in update_data and not validators.college_trust(update_data["Department"]):
        errors["Department"] = "name college is wrong"
    if "Major" in update_data and not validators.trust(update_data["Major"]):
        errors["Major"] = "field of study is wrong"
    if "Married" in update_data and not (update_data["Married"] == "متاهل" or update_data["Married"] == "مجرد"):
        errors["Married"] = "is marital status is wrong value"
    if "ID" in update_data and not validators.validate_national_id(update_data["ID"]):
        errors["ID"] = "code melli is incorrect"
    if errors:
        raise HTTPException(status_code=400, detail={"detail": "Validation error", "errors": errors})
    result = crud.update_student(db, STID, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return result


app.include_router(router)


@app.delete("/DelStu/{STID}", tags= ["Student"], summary= "Delete Student ", description= "Delete a student user")
def del_std(STID: int, db: session = Depends(get_db)):
    """
    Delete a student by their ID.
    Args:
        STID (int): The ID of the student to delete.
        db (session): Database session dependency.
    Returns:
        dict: Confirmation message of the deletion.
    """
    del_st = crud.del_std(db, STID)
    return del_st


def long_running_process():
    """
    Simulates a long-running process, allowing interruption with cleanup.
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
