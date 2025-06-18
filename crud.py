from sqlmodel import Session, select
from models import Campaign


# Create a new campaign and save it to the database
def create_campaign(session: Session, campaign: Campaign):
    session.add(campaign)
    session.commit()
    session.refresh(campaign)  # Refresh to get updated fields like ID
    return campaign


# Retrieve all campaigns from the database
def get_campaigns(session: Session):
    return session.exec(select(Campaign)).all()


# Get a specific campaign by its ID
def get_campaign_by_id(session: Session, campaign_id: int):
    return session.get(Campaign, campaign_id)


# Delete a campaign by ID (if it exists)
def delete_campaign(session: Session, campaign_id: int):
    campaign = session.get(Campaign, campaign_id)
    if campaign:
        session.delete(campaign)
        session.commit()
        return True
    return False


# Filter campaigns based on optional query parameters
def filter_campaigns(
    session: Session,
    name: str = None,
    status: str = None,
    min_budget: float = None,
    max_budget: float = None
):
    query = select(Campaign)

    if name:
        query = query.where(Campaign.name.contains(name))  # Partial match
    elif status:
        query = query.where(Campaign.status == status)     # Exact match
    elif min_budget is not None:
        query = query.where(Campaign.budget >= min_budget)
    elif max_budget is not None:
        query = query.where(Campaign.budget <= max_budget)

    return session.exec(query).all()
