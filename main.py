from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  
    allow_headers=["*"],  
)

assets = {
    1: {
        "id": 1,
        "name": "Laptop",
        "serial": "lap/02/ars",
        "brand": "Apple",
        "model": "MacBook",
        "status": "available",
        "staff_no": None,
        "email": None,
        "department": None,
        "return_date": None
    },
    2: {
        "id": 2,
        "name": "Projector",
        "serial": "proj/01/xyz",
        "brand": "Sony",
        "model": "XYZ-1000",
        "status": "available",
        "staff_no": None,
        "email": None,
        "department": None,
        "return_date": None
    },
    3: {
        "id": 3,
        "name": "Monitor",
        "serial": "mon/01/abc",
        "brand": "Samsung",
        "model": "S27R650FDN",
        "status": "available",
        "staff_no": None,
        "email": None,
        "department": None,
        "return_date": None
    },
    4: {
        "id": 4,
        "name": "Printer",
        "serial": "prn/01/pqr",
        "brand": "HP",
        "model": "LaserJet Pro MFP M428fdw",
        "status": "available",
        "staff_no": None,
        "email": None,
        "department": None,
        "return_date": None
    },
    5: {
        "id": 5,
        "name": "Printer",
        "serial": "prn/02/uvw",
        "brand": "Epson",
        "model": "EcoTank ET-2760",
        "status": "available",
        "staff_no": None,
        "email": None,
        "department": None,
        "return_date": None
    }
}

class Asset(BaseModel):
    id: Optional[int] = None
    name: str
    serial: str
    brand: str
    model: str
    status: str
    staff_no: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    return_date: Optional[str] = None


class UpdateAsset(BaseModel):
    name: Optional[str] = None
    serial: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    status: Optional[str] = None
    staff_no: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    return_date: Optional[str] = None

@app.get("/")
def index():
    return {"name": "First Data"}

@app.get("/get-all-assets")
def get_all_assets():
    return assets

@app.get("/get-asset/{asset_id}")
def get_asset(asset_id: int = Path(..., description="The ID of the asset you want to view")):
    if asset_id in assets:
        return assets[asset_id]
    else:
        return {"Data": "Asset not found"}

@app.get("/get-by-name/")
def get_asset_by_name(name: str):
    for asset_id, asset_data in assets.items():
        if asset_data["name"] == name:
            return {asset_id: asset_data}
    return {"Data": "Not found"}

@app.post("/create-asset")
def create_asset(asset: Asset):
    new_asset_id = max(assets.keys(), default=0) + 1  
    asset.id = new_asset_id  
    assets[new_asset_id] = asset.dict()
    return assets[new_asset_id]

@app.put("/update-asset/{asset_id}")
def update_asset(asset_id: int, asset: UpdateAsset):
    if asset_id not in assets:
        return {"Error": "Asset does not exist"}
    
    for key, value in asset.dict().items():
        if value is not None:
            assets[asset_id][key] = value
    
    return assets[asset_id]

@app.delete("/delete-asset/{asset_id}")
def delete_asset(asset_id: int):
    if asset_id not in assets:
        return {"Error": "Asset does not exist"}
    
    del assets[asset_id]
    return {"Message": "Asset deleted successfully"}
