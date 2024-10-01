from fastapi import APIRouter


router = APIRouter(tags=['Котята'])


@router.get('/')
async def get_cats():
    return {'cats': 'kittens'}
