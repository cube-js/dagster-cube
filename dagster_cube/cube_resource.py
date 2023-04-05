from dagster import Failure, Field, StringSource, get_dagster_logger, resource
import requests
from typing import Any, Dict, Optional
from urllib.parse import urljoin
import logging

class CubeResource:
    """
    This class exposes methods on top of the Cube REST API.
    Args:
        instance_url (str): Base URL for the API
        api_key (str): Cube API Token to use for authentication
    """

    def __init__(
        self,
        instance_url: str,
        api_key: str,
        log: logging.Logger = get_dagster_logger(),
    ):
        self._instance_url = instance_url
        self._api_key = api_key
        self._log = log
    

    def make_request(
        self, 
        method: str, 
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """Creates and sends a request to the desired Cube API endpoint
        Args:
            method (str): The http method use for this request (e.g. "GET", "POST").
            endpoint (str): The Cube API endpoint to send this request to.
            data (Optional(dict): Query parameters to pass to the API endpoint
        Returns:
            Dict[str, Any]: Parsed json data from the response to this request
        """

        headers = {"Authorization": self._api_key, "Content-Type": "application/json"}
        url = urljoin(self._instance_url, endpoint)

        try:
            if method == "GET":
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=data,
                )
            elif method == "POST":
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
            else:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                )
            
            if response.status_code == 422:
                try:
                    msg = response.json()
                except requests.exceptions.JSONDecodeError:
                    msg = response.text
                raise Failure(f"Received 422 status from Cube: {msg}")

            response.raise_for_status()
            
            if response.headers.get("Content-Type", "").startswith(
                "application/json"
            ):
                try:
                    response_json = response.json()
                except requests.exceptions.JSONDecodeError:
                    self._log.error("Failed to decode response from API.")
                    self._log.error("API returned: %s", response.text)
                    raise Failure(
                        "Unexpected response from Cube API. Failed to decode to JSON."
                    )
                return response_json
        
        except requests.RequestException as e:
            self._log.error("Request to Cube API failed: %s", e)


@resource(
    config_schema={
        "instance_url": Field(
            StringSource,
            description="Instance URL for API requests.",
        ),
        "api_key": Field(
            StringSource,
            is_required=True,
            description="Cube API Key.",
        ),
    },
    description="Resource to interact with your Cube Cloud instance",
)
def cube_resource(context):
    """
    This resource allows users to programmatically interface with the Cube REST API
    """
    return CubeResource(
        instance_url=context.resource_config["instance_url"],
        api_key=context.resource_config["api_key"],
        log=context.log,
    )
