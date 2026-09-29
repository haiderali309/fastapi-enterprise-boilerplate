from fastapi import APIRouter, Depends
from typing import Any, Callable, List, Optional
from .checker import PermissionChecker


class SecureRouter(APIRouter):
    """
    Custom APIRouter subclass that extends standard FastAPI routing to support
    declarative role-based access control (RBAC).

    Usage:
        router = SecureRouter(prefix="/users")

        @router.get("/", permissions=[Permission.VIEW_USER])
        async def list_users():
            ...
    """

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        permissions: Optional[List[Any]] = None,
        dependencies: Optional[List[Depends]] = None,
        **kwargs: Any
    ) -> None:
        """
        Intercepts route creation. If `permissions` are passed, automatically
        attaches a `PermissionChecker` dependency to the route pipeline.
        """
        permissions = permissions or []
        dependencies = list(dependencies or [])

        # Automatically inject PermissionChecker dependency if permissions are specified
        if permissions:
            dependencies.append(Depends(PermissionChecker(permissions)))

        super().add_api_route(path, endpoint, dependencies=dependencies, **kwargs)

    def api_route(
        self,
        path: str,
        *,
        permissions: Optional[List[Any]] = None,
        **kwargs: Any
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator for custom API routes with permissions."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.add_api_route(path, func, permissions=permissions, **kwargs)
            return func
        return decorator

    # Standard HTTP Method Shortcuts extended to support permissions=[]
    def get(self, path: str, *, permissions: Optional[List[Any]] = None, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.api_route(path, methods=["GET"], permissions=permissions, **kwargs)

    def post(self, path: str, *, permissions: Optional[List[Any]] = None, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.api_route(path, methods=["POST"], permissions=permissions, **kwargs)

    def put(self, path: str, *, permissions: Optional[List[Any]] = None, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.api_route(path, methods=["PUT"], permissions=permissions, **kwargs)

    def delete(self, path: str, *, permissions: Optional[List[Any]] = None, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.api_route(path, methods=["DELETE"], permissions=permissions, **kwargs)

    def patch(self, path: str, *, permissions: Optional[List[Any]] = None, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.api_route(path, methods=["PATCH"], permissions=permissions, **kwargs)

    def options(self, path: str, *, permissions: Optional[List[Any]] = None, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.api_route(path, methods=["OPTIONS"], permissions=permissions, **kwargs)

    def head(self, path: str, *, permissions: Optional[List[Any]] = None, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.api_route(path, methods=["HEAD"], permissions=permissions, **kwargs)