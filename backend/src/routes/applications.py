from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from src.auth import get_current_user
from src.database import get_session
from src.models import Application, StatusEvent, User
from src.schemas.application import (
    ApplicationCreateRequest,
    ApplicationUpdateRequest,
    ApplicationListResponse,
)
from src.schemas.status_event import StatusEventCreateRequest

# Initialize the router with a prefix and tags for automatic documentation
applications_router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)

CurrentUser = Annotated[User, Depends(get_current_user)]

@applications_router.get("", status_code=status.HTTP_200_OK)
def get_applications(
    current_user: CurrentUser,
    session: Session = Depends(get_session),
) -> list[ApplicationListResponse]:
    """Fetch all applications associated with the authenticated user."""
    applications = session.scalars(
        select(Application)
        .options(selectinload(Application.status_events))
        .where(Application.user_id == current_user.id)
    ).all()

    response: list[ApplicationListResponse] = []

    for application in applications:
        latest_status = application.status_events[-1] if application.status_events else None

        response.append(
            ApplicationListResponse(
                id=application.id,
                company_name=application.company_name,
                role_name=application.role_name,
                applied_date=application.applied_date,
                current_status=latest_status.status if latest_status else None,
            )
        )

    return response


@applications_router.get("/{application_id}", status_code=status.HTTP_200_OK)
def get_application(
    application_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Fetch the application associated with the authenticated user and application id."""
    application = session.execute(
        select(Application)
        .where(Application.user_id == current_user.id)
        .where(Application.id == application_id)
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
        
    return application


@applications_router.post("", status_code=status.HTTP_201_CREATED)
def create_application(
    request: ApplicationCreateRequest,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Create a new application for the authenticated user."""
    application = Application(
        user_id=current_user.id,
        company_name=request.company_name,
        role_name=request.role_name,
    )

    if request.applied_date:
        application.applied_date = request.applied_date

    application.status_events.append(
        StatusEvent(status="Applied")
    )

    session.add(application)
    session.commit()
    session.refresh(application)

    return application


@applications_router.patch("/{application_id}", status_code=status.HTTP_200_OK)
def update_application(
    application_id: int,
    request: ApplicationUpdateRequest,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Patch the application associated with the authenticated user."""
    application = session.execute(
        select(Application)
        .where(Application.user_id == current_user.id)
        .where(Application.id == application_id)
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    updates = request.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in updates.items():
        setattr(application, field, value)

    session.commit()
        
    return application


@applications_router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Delete the application associated with the authenticated user."""
    result = session.execute(
        delete(Application)
        .where(Application.user_id == current_user.id)
        .where(Application.id == application_id)
    )
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    session.commit()


@applications_router.post("/{application_id}/status_events", status_code=status.HTTP_201_CREATED)
def create_status_event(
    application_id: int,
    request: StatusEventCreateRequest,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Create a new status event for the authenticated user's application."""
    application = session.execute(
        select(Application)
        .where(Application.user_id == current_user.id)
        .where(Application.id == application_id)
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    status_event = StatusEvent(
        status=request.status.value
    )

    application.status_events.append(status_event)
    session.commit()

    return status_event


@applications_router.get("/{application_id}/status_events", status_code=status.HTTP_200_OK)
def get_status_events(
    application_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Fetch all status events associated with the authenticated user's application."""
    application = session.execute(
        select(Application)
        .where(Application.user_id == current_user.id)
        .where(Application.id == application_id)
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application.status_events

