from fastapi import FastAPI, Path
import json
app = FastAPI()

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
    return {'error' : 'Patient not found'}
