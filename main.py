from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr, AnyUrl, field_validator
from typing import List, Dict, Optional, Annotated
import json
app = FastAPI()

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of patient')]
    age: int = Field(ge=18)
    # we can use Field for validation like greater than, less than or any lambda
    weight: float = Field(gt=0)
    isMarried: bool = False
    linkedin_url: AnyUrl
    email: EmailStr
    # can set default values
    allergies: Optional[List[str]] = Field(max_length=5)
    # by default pydantic fields validate to be non empty and we can use Optional from typing for optional fields
    contact_details: Dict[str, str]
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[1]
        
        if (domain_name not in valid_domains):
            raise ValueError('Not a valid domain')


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {'message' : "Patient Management System API"}

@app.get("/about")
def about():
    return {'message' : "Supp !! what do you wanna know? "}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}") 
def patient(patient_id: str = Path(..., description="get patient by patient ID", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not found')

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']

    if (sort_by not in valid_fields):
        raise HTTPException(status_code=400, detail=f'Invalid field, select from {valid_fields}')
    if (order not in ['asc', 'desc']):
        raise HTTPException(status_code=400, detail='Invalid order field, select from asc or desc')
    data = load_data()
    sort_order = ()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=(order == 'desc'))
    return sorted_data