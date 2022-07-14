import logging

import xlwings as xw
from fastapi import APIRouter, Body, Depends, Security
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from ..core.auth import User, authenticate
from ..core.database import get_db
from ..utils import process_cursor_result

logger = logging.getLogger(__name__)

# Require authentication for all endpoints for this router
router = APIRouter(
    dependencies=[Security(authenticate)],
    prefix="/employees",
    tags=["Database"],
)


@router.post("/select")
def select_employees(
    data: dict = Body,
    current_user: User = Security(authenticate),
    db: Session = Depends(get_db),
):
    # Spreadsheet objects
    book = xw.Book(json=data)
    sheet = book.sheets[0]
    result_cell = sheet["D1"]

    # Get the query parameters as dictionary
    params = sheet["A5:B5"].options(dict, expand="down").value

    # You can log who is running the query
    logger.info(f"Running 'select employees' query for user {current_user.email}")

    # SQL Query using SQLAlchemy placeholders
    sql = """
    SELECT *
    FROM employees
    WHERE salaried_flag = :salaried_flag
    """
    if params["job title"]:
        sql += "AND LOWER(job_title) LIKE LOWER(:job_title)"

    # Execute the query via SQLAlchemy
    result = db.execute(
        text(sql),
        {
            "salaried_flag": params["salaried?"],
            "job_title": f"%{params['job title']}%",
        },
    )

    # Delete existing data in the spreadsheet and write the result back
    result_cell.expand().clear_contents()
    result_cell.value = process_cursor_result(result)

    return book.json()
