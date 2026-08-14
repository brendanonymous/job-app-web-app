from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from fastapi import APIRouter, status, Depends
from src.database import get_session
from src.models import Application, StatusEvent
from src.schemas.application import (
    ApplicationCreateRequest,
    ApplicationCreateResponse,
    ApplicationUpdateRequest,
    ApplicationListResponse
    )
from src.schemas.status_event import (
    StatusEventCreateRequest
    )

# Initialize the router with a prefix and tags for automatic documentation
applications_router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)

@applications_router.get("", status_code=status.HTTP_200_OK)
def get_applications(session: Session = Depends(get_session)) -> list[ApplicationListResponse]:
    """Fetch all applications associated with current user."""
    applications = session.scalars(
        select(Application)
        .options(selectinload(Application.status_events))
        .where(Application.user_id == LOCAL_DEV_USER_ID)
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

    print(response[0].current_status)
        
    return response


@applications_router.get("/{application_id}", status_code=status.HTTP_200_OK)
def get_application(application_id: int, session: Session = Depends(get_session)):
    """fetch the application associated with the application id"""
    application = session.execute(
        select(Application)
        .where(Application.user_id == LOCAL_DEV_USER_ID)
        .where(Application.id == application_id)
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
        
    return application


@applications_router.post("", status_code=status.HTTP_201_CREATED)
def create_application(request: ApplicationCreateRequest, session: Session = Depends(get_session)):
    """create a new application associated with the user id"""
    application = Application(
        user_id=LOCAL_DEV_USER_ID,
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
def update_application(application_id: int, request: ApplicationUpdateRequest, session: Session = Depends(get_session)):
    """patch the application associated with the application id"""
    application = session.execute(
        select(Application)
        .where(Application.user_id == LOCAL_DEV_USER_ID)
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
def delete_application(application_id: int, session: Session = Depends(get_session)):
    """delete the application associated with the application id"""
    result = session.execute(
        delete(Application)
        .where(Application.user_id == LOCAL_DEV_USER_ID)
        .where(Application.id == application_id)
    )
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    session.commit()


@applications_router.post("/{application_id}/status_events", status_code=status.HTTP_201_CREATED)
def create_status_event(application_id: int, request: StatusEventCreateRequest, session: Session = Depends(get_session)):
    """create a new status event associated with the application id"""
    application = session.execute(
        select(Application)
        .where(Application.user_id == LOCAL_DEV_USER_ID)
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
def get_status_events(application_id: int, session: Session = Depends(get_session)):
    """fetch all status events associated with the application id"""
    application = session.execute(
        select(Application)
        .where(Application.user_id == LOCAL_DEV_USER_ID)
        .where(Application.id == application_id)
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application.status_events

