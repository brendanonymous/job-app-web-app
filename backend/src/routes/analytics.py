from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.auth import get_current_user
from src.database import get_session
from src.models import Application, StatusEvent, User
from src.visualizations.sankey import generate_sankey_dto
from src.schemas.sankey import SankeyDto

# Initialize the router with a prefix and tags for automatic documentation
analytics_router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)

CurrentUser = Annotated[User, Depends(get_current_user)]

@analytics_router.get("/sankey", status_code=status.HTTP_200_OK, response_model=SankeyDto)
def generate_sankey(
    current_user: CurrentUser,
    session: Session = Depends(get_session)):
    """Generate a Sankey dto for the authed user's
    application data and return to user as JSON"""

    applications = session.execute(
        select(Application)
        .where(Application.user_id == current_user.id)
    ).scalars().all()

    # collect all status paths and relabel them
    status_paths = []
    for application in applications:
        interview_count, status_path= 1, []
        for i in range(len(application.status_events)):
            status = application.status_events[i].status
            if status == "Interview":
                status += f" {interview_count}"
                interview_count += 1
            status_path.append(status)
        status_paths.append(status_path)

    sankey_dto = generate_sankey_dto(status_paths)

    # return the Pydantic model directly. 
    # FastAPI will serialize to JSON
    return sankey_dto