

# crud - create, read, update, delete


from fastapi import APIRouter, FastAPI, Depends, HTTPException, Query, Form
from fastapi.responses import JSONResponse
from api.utils import check_db_connection
from api.services.auth_service import AuthService

from api.db import Session, get_db # your db module with init_db
import api.crud as crud # your CRUD operations
from api.services.raw_order_service import RawOrderService
from api.v1.schemas import OrderOut, RawOrderOut   # your pydantic schema
from typing import List

router = APIRouter()

@router.get("/health", tags=["Monitoring"])
async def health_check(db: Session = Depends(get_db)):
    """
    Check the health status of the service.

    Returns:
        dict: {"status": "ok"} if the database connection is healthy.
        Otherwise, returns 503 status with {"status": "unhealthy"}.

    Example:
        curl -v http://localhost:8000/health
    """

    db_ok = check_db_connection()
    if db_ok:
        return {"status": "ok"}
    return JSONResponse(status_code=503, content={"status": "unhealthy"}, summary="Check service health")


@router.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    """
        Authenticate user credentials and issue an access token.

        Args:
            username (str): The username submitted via form.
            password (str): The password submitted via form.

        Returns:
            dict: Access token and token type upon successful authentication.

        Raises:
            HTTPException: 401 Unauthorized if credentials are invalid.

        Example:
            curl -X POST http://localhost:8000/token \\
              -F "username=admin" \\
              -F "password=secret"
    """

    # providing dummy user
    fake_user = {"username": "admin", "password_hash": AuthService.hash_password("secret")}

    if username != fake_user["username"] or not AuthService.verify_password(password, fake_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = AuthService.create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/me")
def read_current_user(current_user: dict = Depends(AuthService.get_current_user)):
    """
        Retrieve information about the currently authenticated user.

        Returns:
            dict: Details of the authenticated user.

        Example:
            curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/me
    """

    return {"authenticated_user": current_user}

@router.post("/raw-orders", response_model=RawOrderOut, tags=["Raw Layer", "Orders"], summary="Ingest raw order data")
async def receive_raw_order(
        payload: dict,
        db: Session = Depends(get_db),
        user: dict = Depends(AuthService.get_current_user)
):
    """
        Accept and store raw order data.

        Args:
            payload (dict): Raw order data to ingest.
            db (Session): Database session.
            user (dict): Currently authenticated user.

        Returns:
            RawOrderOut: Created raw order data transfer object (DTO).
    """

    service = RawOrderService(db)
    dto = service.create(payload)
    return dto

@router.get("/raw-orders/{uid}", response_model=RawOrderOut, tags=["Raw Layer", "Orders"], summary="Retrieve raw order data")
def get_raw_order(
        uid: int,
        db: Session = Depends(get_db),
        user: dict = Depends(AuthService.get_current_user)
):
    """
        Retrieve a single raw order by its unique ID.

        Args:
            uid (int): Unique identifier of the raw order.
            db (Session): Database session.
            user (dict): Currently authenticated user.

        Returns:
            RawOrderOut: Raw order data transfer object.

        Raises:
            HTTPException: 404 if the order is not found.

        Example:
            curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/raw-orders/1234
     """

    service = RawOrderService(db)
    raw_order_dto = service.get_by_uid(uid)
    if not raw_order_dto:
        raise HTTPException(status_code=404, detail="Order not found")

    model = RawOrderOut.from_orm(raw_order_dto)

    return model
