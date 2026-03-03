from pydantic import BaseModel, Field, computed_field
from typing import  Annotated, Literal, Optional
class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description = 'ID of the patient', examples = ['P001'])]
    name: Annotated[str, Field(..., description = 'Name of the patient')]
    city: Annotated[str, Field(..., description = 'City where the patient is living')]
    age: Annotated[int, Field(..., gt = 0, lt = 120, description = 'Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description = 'Gender of the patient')]
    height: Annotated[float, Field(..., gt = 0, description = 'Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt = 0, description = 'Weight of the patient in kgs')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round((self.weight)/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    
    name: Annotated[Optional[str], Field(default = None)]
    city: Annotated[Optional[str], Field(default = None)]
    age: Annotated[Optional[int], Field(default = None, gt = 0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default = None)  ]
    height: Annotated[Optional[float], Field(default = None, gt = 0)]
    weight: Annotated[Optional[float], Field(default = None, gt = 0)]