"""
Defines Pydantic models for student management system entities.

- `Student`: Represents student information for input data.
- `StudentOut`: Represents student information for output data.
- `UpdateStudent`: Represents updateable fields for student information.
- `Lesson`: Represents lesson/course information for input data.
- `UpdateLesson`: Represents updateable fields for lesson/course information.
- `Master`: Represents master/professor information for input data.
- `MasterOut`: Represents master/professor information for output data.
- `UpdateMaster`: Represents updateable fields for master/professor information.
"""
from typing import Optional, List
from pydantic import BaseModel


class Student(BaseModel):
    STID: int
    FName: str
    LName: str
    Father: str
    Birth: str
    IDS: str
    BornCity: str
    Address: str
    PostalCode: int
    CPhone: str
    HPhone: str
    Department: str
    Major: str
    Married: str
    ID: int
    SCourseIDs: list[int] | None
    LIDs: list[int] | None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class StudentOut(BaseModel):
    STID: int
    FName: str
    LName: str
    Father: str
    SCourseIDs: list
    LIDs: list
    class Config:
        from_attributes = True

class UpdateStudent(BaseModel):
    FName: Optional[str] = None
    LName:  Optional[str] = None
    Father:  Optional[str] = None
    Birth:  Optional[str] = None
    IDS:  Optional[str] = None
    BornCity:  Optional[str] = None
    Address:  Optional[str] = None
    PostalCode: Optional[int] = None
    CPhone:  Optional[str] = None
    HPhone:  Optional[str] = None
    Department:  Optional[str] = None
    Major:  Optional[str] = None
    Married:  Optional[str] = None
    ID: Optional[int] = None
    SCourseIDs: list[int] | None
    LIDs: list[int] | None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class Lesson(BaseModel):
    CID: int
    CName: str
    Department: str
    Credit: str

    class Config:
        from_attributes = True

class UpdateLesson(BaseModel):
    CName: Optional[str] = None
    Department: Optional[str] = None
    Credit: Optional[str] = None

    class Config:
        from_attributes = True

class Master(BaseModel):
    LID: int
    FName: str
    LName: str
    ID: int
    Department: str
    Major: str
    Birth: str
    BornCity: str
    Address: str
    PostalCode: str
    CPhone: str
    HPhone: str
    LCourseIDs: list[int] | None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class MasterOut(BaseModel):
    LID: int
    FName: str
    LName: str
    ID: int
    LCourseIDs: List

    class Config:
        from_attributes = True

class UpdateMaster(BaseModel):
    FName: Optional[str] = None
    LName: Optional[str] = None
    ID: Optional[int] = None
    Department: Optional[str] = None
    Major: Optional[str] = None
    Birth: Optional[str] = None
    BornCity: Optional[str] = None
    Address: Optional[str] = None
    PostalCode: Optional[str] = None
    CPhone: Optional[str] = None
    HPhone: Optional[str] = None
    LCourseIDs: Optional[list[int]] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
