from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.curd.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден!"
        )
    return charity_project


async def check_charity_project_closed_or_invested(project: CharityProject):
    print(project.close_date)
    print(project.invested_amount)
    if project.close_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_charity_project_fully_invested(project: CharityProject):
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )
