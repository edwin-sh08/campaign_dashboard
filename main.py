from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session

# Import local modules
from database import create_db_and_tables, get_session
from models import Campaign, CampaignCreate
from crud import (
    create_campaign,
    get_campaigns,
    get_campaign_by_id,
    delete_campaign,
    filter_campaigns
)

app = FastAPI()


# Automatically create the database and tables when the app starts
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Create a new campaign
@app.post("/campaigns/", response_model=Campaign)
def add_campaign(
    campaign_data: CampaignCreate,
    session: Session = Depends(get_session)
):
    campaign = Campaign.from_orm(campaign_data)
    return create_campaign(session, campaign)


# Retrieve all campaigns (no filters)
@app.get("/campaigns/", response_model=List[Campaign])
def list_campaigns(session: Session = Depends(get_session)):
    return get_campaigns(session)


# Get a single campaign by its ID
@app.get("/campaigns/{campaign_id}", response_model=Campaign)
def get_one_campaign(
    campaign_id: int,
    session: Session = Depends(get_session)
):
    campaign = get_campaign_by_id(session, campaign_id)
    if campaign:
        return campaign
    raise HTTPException(status_code=404, detail="Campaign not found")


# Delete a campaign by ID
@app.delete("/campaigns/{campaign_id}")
def remove_campaign(
    campaign_id: int,
    session: Session = Depends(get_session)
):
    success = delete_campaign(session, campaign_id)
    if success:
        return {"detail": "Campaign deleted"}
    raise HTTPException(status_code=404, detail="Campaign not found")


# Filter campaigns based on optional query parameters
@app.get("/campaigns/filter", response_model=List[Campaign])
def filter_campaign_route(
    name: Optional[str] = Query(None, description="Filter by campaign name"),
    status: Optional[str] = Query(None, description="Filter by status"),
    min_budget: Optional[float] = Query(None, description="Minimum budget"),
    max_budget: Optional[float] = Query(None, description="Maximum budget"),
    session: Session = Depends(get_session)
):
    return filter_campaigns(session, name, status, min_budget, max_budget)
