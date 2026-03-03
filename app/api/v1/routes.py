from fastapi import APIRouter, Path, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from app.services.services_user import load_data, save_data
from app.schemas.user import Patient, PatientUpdate

router = APIRouter()


@router.get("/")
def hello():
    return {"message": "Hello from API v1!"}


@router.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the DB",
        openapi_examples={
            "Patient One": {"summary": "Example ID for Patient", "value": "P001"},
        },
    )
):

    data = load_data("patients.json")

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@router.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height/ weight/ bmi"),
    order: str = Query("asc", description="Sort in asc or desc order"),
):

    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid field, select from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="Invalid order select between asc or desc"
        )

    data = load_data("patients.json")
    sort_order = True if order == "desc" else False
    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order
    )
    return sorted_data

@router.post('/create')
def create_patient(patient: Patient):
    
    data = load_data("patients.json")
    
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = 'Patient already exists')
    
    data[patient.id] =  patient.model_dump(exclude = {'id'})
    
    save_data("patients.json", data)
    
    return JSONResponse(status_code = 201, content = {'message' : 'Patient created successfully'})  

@router.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    
    data = load_data("patients.json")
    
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = 'Patient not found')
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset = True)
    
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
        
    # existing_patient_info -> pydantic object -> updated bmi + verdict -> pydantic object -> dict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    
    existing_patient_info = patient_pydantic_obj.model_dump(exclude = {'id'})
    
    data[patient_id] = existing_patient_info
    
    save_data("patients.json", data)
    
    return JSONResponse(status_code = 200, content = {'message' : 'patient updated'})

@router.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    
    data = load_data("patients.json")
    
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = 'Patient not found')
    
    del data[patient_id]
    
    save_data("patients.json", data)    
    
    return JSONResponse(status_code = 200, content = {'message' : 'patient deleted'})

# Dependency Injection

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@router.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    return commons