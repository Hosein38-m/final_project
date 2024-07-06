"""
This module defines CRUD operations (Create, Read, Update, Delete) for interacting with
student, master, and lesson records in a database using SQLAlchemy.

It includes functions to:
- Create new student, master, and lesson records.
- Retrieve existing student, master, and lesson records.
- Update student, master, and lesson records with new data.
- Delete student, master, and lesson records from the database.

All functions handle database sessions and raise appropriate HTTP exceptions if records
are not found or validation fails.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dtool import schemas
from dtool.model import Student, Master, Lesson



def create_student(db: Session, student: schemas.Student):
    """
    Create a new student record.
    Args:
        db (Session): Database session.
        student (schemas.Student): Student data.
    Returns:
        Student: Created student object.
    """
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def create_master(db: Session, master: schemas.Master):
    """
    Create a new master record.
    Args:
        db (Session): Database session.
        master (schemas.Master): Master data.
    Returns:
        Master: Created master object.
    """
    db_master = Master(**master.model_dump())
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    return db_master


def create_lesson(db: Session, lesson: schemas.Lesson):
    """
    Create a new lesson record.
    Args:
        db (Session): Database session.
        lesson (schemas.Lesson): Lesson data.
    Returns:
        Lesson: Created lesson object.
    """
    db_lesson = Lesson(**lesson.model_dump())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def get_student(db: Session, stid: int):
    """
    Retrieve a student record.
    Args:
        db (Session): Database session.
        stid (int): Student ID.
    Returns:
        Student: Retrieved student object.
    Raises:
        HTTPException: If student with the given ID does not exist.
    """
    get_std = db.query(Student).filter(Student.STID == stid).first()
    if get_std is None :
        raise HTTPException(status_code=400, detail="student is not found")
    return get_std

def get_msr(db: Session, Lid: int):
    """
    Retrieve a master record.
    Args:
        db (Session): Database session.
        Lid (int): Master ID.
    Returns:
        Master: Retrieved master object.
    Raises:
        HTTPException: If master with the given ID does not exist.
    """
    get_ms = db.query(Master).filter(Master.LID == Lid).first()
    if get_ms is None :
        raise HTTPException(status_code=400, detail="master is not found")
    return get_ms

def get_lsn(db: Session, Cid: int):
    """
    Retrieve a lesson record.
    Args:
        db (Session): Database session.
        Cid (int): Lesson ID.
    Returns:
        Lesson: Retrieved lesson object.
    Raises:
        HTTPException: If lesson with the given ID does not exist.
    """
    get_ls = db.query(Lesson).filter(Lesson.CID == Cid).first()
    if get_ls is None :
        raise HTTPException(status_code=400, detail="lesson is not found")
    return get_ls

def update_student(db: Session, stid: int, updated_data: dict):
    """
    Update a student record.
    Args:
        db (Session): Database session.
        stid (int): Student ID.
        updated_data (dict): Updated data for the student.
    Returns:
        Student: Updated student object.
    Raises:
        HTTPException: If student with the given ID does not exist.
    """
    student = db.query(Student).filter(Student.STID == stid).first()
    if student is None:
        raise HTTPException(status_code=400, detail="student is not found")
    for key, value in list(updated_data.items()):
        if value is None:
            del updated_data[key]
    for key, value in updated_data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

def update_master(db: Session, LID: int, updated_data: dict):
    """
    Update a master record.
    Args:
        db (Session): Database session.
        LID (int): Master ID.
        updated_data (dict): Updated data for the master.
    Returns:
        Master: Updated master object.
    Raises:
        HTTPException: If master with the given ID does not exist.
    """
    master = db.query(Master).filter(Master.LID == LID).first()
    for key, value in list(updated_data.items()):
        if value is None:
            del updated_data[key]
    for key, value in updated_data.items():
        setattr(master, key, value)
    db.commit()
    db.refresh(master)
    return master

def update_course(db: Session, CID: int, updated_data: dict):
    """
    Update a lesson record.
    Args:
        db (Session): Database session.
        CID (int): Lesson ID.
        updated_data (dict): Updated data for the lesson.
    Returns:
        Lesson: Updated lesson object.
    Raises:
        HTTPException: If lesson with the given ID does not exist.
    """
    course = db.query(Lesson).filter(Lesson.CID == CID).first()
    for key, value in list(updated_data.items()):
        if value is None:
            del updated_data[key]
    for key, value in updated_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

def del_std(db: Session, stid: int):
    """
    Delete a student record.
    Args:
        db (Session): Database session.
        stid (int): Student ID.
    Returns:
        str: Success message.
    Raises:
        HTTPException: If student with the given ID does not exist.
    """
    student = db.query(Student).filter(Student.STID == stid).first()
    if student is None:
        raise HTTPException(status_code=400, detail="student is not found")
    db.delete(student)
    db.commit()
    return "delete record is succesful"

def del_msr(db: Session, Lid: int):
    """
    Delete a master record.
    Args:
        db (Session): Database session.
        Lid (int): Master ID.
    Returns:
        str: Success message.
    Raises:
        HTTPException: If master with the given ID does not exist.
    """
    master = db.query(Master).filter(Master.LID == Lid).first()
    if master is None:
        raise HTTPException(status_code=400, detail="master is not found")
    db.delete(master)
    db.commit()
    return "delete record is succesful"

def del_lsn(db: Session, Cid: int):
    """
    Delete a lesson record.
    Args:
        db (Session): Database session.
        Cid (int): Lesson ID.
    Returns:
        str: Success message.
    Raises:
        HTTPException: If lesson with the given ID does not exist.
    """
    lesson = db.query(Lesson).filter(Lesson.CID == Cid).first()
    if lesson is None:
        raise HTTPException(status_code=400, detail="lesson is not found")
    db.delete(lesson)
    db.commit()
    return "delete record is succesful"
