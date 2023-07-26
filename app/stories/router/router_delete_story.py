
from fastapi import Depends, Response, HTTPException
from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router



@router.delete("/{story_id:str}")
def delete_story(
    story_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    delete_result = svc.repository.delete_story(story_id=story_id, 
                                                user_id=jwt_data.user_id)
    if delete_result.deleted_count == 1:
        return Response(status_code=200, content="Story successfully deleted")
    raise HTTPException(status_code=404, detail="Story not found")


