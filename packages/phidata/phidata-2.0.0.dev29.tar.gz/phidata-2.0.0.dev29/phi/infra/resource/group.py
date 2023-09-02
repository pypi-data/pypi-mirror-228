from typing import Optional, List, Any

from phi.base import PhiBase
from phi.workspace.settings import WorkspaceSettings


class InfraResourceGroup(PhiBase):
    env: Optional[str] = None

    apps: Optional[List[Any]] = None
    resources: Optional[List[Any]] = None

    def create_resources(
        self,
        group_filter: Optional[str] = None,
        name_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        dry_run: Optional[bool] = False,
        auto_confirm: Optional[bool] = False,
        force: Optional[bool] = None,
        workspace_settings: Optional[WorkspaceSettings] = None,
    ) -> int:
        raise NotImplementedError

    def delete_resources(
        self,
        group_filter: Optional[str] = None,
        name_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        dry_run: Optional[bool] = False,
        auto_confirm: Optional[bool] = False,
        force: Optional[bool] = None,
        workspace_settings: Optional[WorkspaceSettings] = None,
    ) -> int:
        raise NotImplementedError

    def update_resources(
        self,
        group_filter: Optional[str] = None,
        name_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        dry_run: Optional[bool] = False,
        auto_confirm: Optional[bool] = False,
        force: Optional[bool] = None,
        workspace_settings: Optional[WorkspaceSettings] = None,
    ) -> int:
        raise NotImplementedError
