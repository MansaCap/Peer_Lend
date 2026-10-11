# peer_lending_backend/src/security/rbac.py

from fastapi import HTTPException, status

def require_role(required_role: str):
    def wrapper(user):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role"
            )
        return True
    return wrapper
