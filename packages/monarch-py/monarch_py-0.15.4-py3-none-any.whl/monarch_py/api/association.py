from typing import List, Union

from fastapi import APIRouter, Depends, Query
from monarch_py.api.additional_models import PaginationParams
from monarch_py.api.config import solr
from monarch_py.datamodels.model import AssociationResults

router = APIRouter(
    tags=["association"],
    responses={404: {"description": "Not Found"}},
)


@router.get("")
@router.get("/all")
async def _get_associations(
    category: Union[List[str], None] = Query(default=None),
    subject: Union[List[str], None] = Query(default=None),
    predicate: Union[List[str], None] = Query(default=None),
    object: Union[List[str], None] = Query(default=None),
    entity: Union[List[str], None] = Query(default=None),
    direct: Union[bool, None] = Query(default=None),
    pagination: PaginationParams = Depends(),
) -> AssociationResults:
    """Retrieves all associations for a given entity, or between two entities."""
    response = solr().get_associations(
        category=category,
        predicate=predicate,
        subject=subject,
        object=object,
        entity=entity,
        direct=direct,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return response
