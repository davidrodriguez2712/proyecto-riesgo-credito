from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get('/health')
def health():
    return {
        'status': 'OK'
    }