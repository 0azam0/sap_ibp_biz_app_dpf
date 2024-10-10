# Copyright 2024 DataRobot, Inc. and its affiliates.
# All rights reserved.
# DataRobot, Inc.
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
# Released under the terms of DataRobot Tool and Utility Agreement.


def ensure_app_settings(
    endpoint: str, token: str, app_id: str, allow_auto_stopping: bool
) -> None:
    """Ensure requested app settings have been applied.

    Parameters
    ----------
    app_id : str
        DataRobot custom application id
    allow_auto_stopping : str
        Whether the app should be allowed to automatically spin down after long periods of no use.
    """
    import datarobot as dr

    dr.Client(endpoint=endpoint, token=token).patch(
        f"customApplications/{app_id}/",
        json={"allowAutoStopping": allow_auto_stopping},
    )


def log_outputs(
    endpoint: str,
    project_id: str,
    model_id: str,
    deployment_id: str,
    application_id: str,
    project_name: str,
    deployment_name: str,
    app_name: str,
) -> None:
    """Log URLs for DR deployments and app.

    Parameters
    ----------
    project_id : str
        DataRobot id of the project
    model_id : str
        DataRobot id of the model
    deployment_id : str
        DataRobot id of the deployment
    application_id : str
        DataRobot id of the custom application
    project_name : str
        Name of the project
    deployment_name : str
        Name of the deployment
    app_name : str
        Name of the deployed custom application
    """
    import logging
    from urllib.parse import urljoin

    base_url = urljoin(endpoint, "/")
    project_url = base_url + "projects/{project_id}/models/{model_id}/"
    deployment_url = base_url + "console/{deployment_id}/overview"
    application_url = base_url + "custom_applications/{application_id}/"

    logger = logging.getLogger(__name__)
    logger.info("Application is live!")
    msg = (
        "AutoPilot Project: "
        f"[link={project_url.format(project_id=project_id, model_id=model_id)}]"
        f"{project_name}[/link]"
    )
    logger.info(msg)
    msg = (
        "Deployment: "
        f"[link={deployment_url.format(deployment_id=deployment_id)}]"
        f"{deployment_name}[/link]"
    )
    logger.info(msg)
    msg = (
        "Custom application: "
        f"[link={application_url.format(application_id=application_id)}]"
        f"{app_name}[/link]"
    )
    logger.info(msg)