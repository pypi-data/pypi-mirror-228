from typing import Optional

from sentry_sdk import capture_message

from slingshot import schemas


def describe_app_type(app_type: schemas.AppType, app_sub_type: Optional[schemas.AppSubType]) -> str:
    """Describes an "app" in the broader sense (including sessions, runs, deployments, etc.)"""

    if app_type == schemas.AppType.RUN:
        return "run"
    elif app_type == schemas.AppType.DEPLOYMENT:
        return "deployment"
    elif app_type == schemas.AppType.CUSTOM:
        if app_sub_type == schemas.AppSubType.SESSION:
            return "session"
        else:
            return "app"
    else:
        capture_message("Asked to format unknown app type {app_type}, defaulting to 'app'")
        return "app"
