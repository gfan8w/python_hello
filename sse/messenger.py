from pydantic import BaseModel
from datetime import date

    
class MessengerReq(BaseModel): 
    id: int
    firstname: str
    lastname: str
    salary: float
    date_employed: date
    status: int
    vendor_id: int
    