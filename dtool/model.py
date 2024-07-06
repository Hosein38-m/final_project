"""
Defines SQLAlchemy ORM models for the student management system.

- `Student`: Represents student information.
- `Lesson`: Represents lesson/course information.
- `Master`: Represents master/professor information.
"""
from sqlalchemy import Column, String, BigInteger, PickleType
from db import Base



class Student(Base):
    __tablename__ = 'student'

    STID = Column(BigInteger, primary_key=True, index=True)
    FName = Column(String(50), nullable=False)
    LName = Column(String(10), nullable=False)
    Father = Column(String(10), nullable=False)
    Birth = Column(String(20), nullable=False)
    IDS = Column(String(20), nullable=False)
    BornCity = Column(String(45), nullable=False)
    Address = Column(String(100), nullable=False)
    PostalCode = Column(BigInteger, nullable=False)
    CPhone = Column(String(20), nullable=False)
    HPhone = Column(String(20), nullable=False)
    Department = Column(String(45), nullable=False)
    Major = Column(String(45), nullable=False)
    Married = Column(String(10), nullable=False)
    ID = Column(BigInteger, nullable=False)
    SCourseIDs = Column(PickleType, nullable=False)
    LIDs = Column(PickleType, nullable=False)


class Lesson(Base):
    __tablename__ = 'lesson'

    CID = Column(BigInteger, primary_key=True, index=True)
    CName = Column(String(25), nullable=False)
    Department = Column(String(20), nullable=False)
    Credit = Column(String(20), nullable=False)



class Master(Base):
    __tablename__ = 'master'

    LID = Column(BigInteger, primary_key=True, index=True)
    FName = Column(String(20), nullable=False)
    LName = Column(String(20), nullable=False)
    ID = Column(BigInteger, nullable=False)
    Department = Column(String(20), nullable=False)
    Major = Column(String(20), nullable=False)
    Birth = Column(String(20), nullable=False)
    BornCity = Column(String(20), nullable=False)
    Address = Column(String(100), nullable=False)
    PostalCode = Column(String(20), nullable=False)
    CPhone = Column(String(20), nullable=False)
    HPhone = Column(String(20), nullable=False)
    LCourseIDs = Column(PickleType, nullable=False)
