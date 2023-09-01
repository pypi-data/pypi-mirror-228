import logging
from datetime import datetime
from typing import Mapping, Optional

from ms_python_client.components.events.events_component import EventsComponent
from ms_python_client.interfaces.ms_client_interface import MSClientInterface
from ms_python_client.utils.event_generator import (
    ZOOM_ID_EXTENDED_PROPERTY_ID,
    EventParameters,
    PartialEventParameters,
    create_event_body,
    create_partial_event_body,
)

logger = logging.getLogger("ms_python_client")


class NotFoundError(Exception):
    """Execption raised when an event is not found

    Args:
        Exception (Exception): The base exception
    """


class CERNEventsComponents:
    """CERN Events component"""

    def __init__(self, client: MSClientInterface) -> None:
        self.events_component = EventsComponent(client)

    def list_events(
        self,
        user_id: str,
        parameters: Optional[Mapping[str, str]] = None,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """List all the events of a user

        Args:
            user_id (str): The user id
            parameters (dict): Optional parameters for the request
            extra_headers (dict): Optional headers for the request

        Returns:
            dict: The response of the request
        """
        return self.events_component.list_events(user_id, parameters, extra_headers)

    def get_event_by_zoom_id(
        self,
        user_id: str,
        zoom_id: str,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Get an event of a user

        Args:
            user_id (str): The user id
            zoom_id (str): The event id
            extra_headers (dict): Optional headers for the request

        Returns:
            dict: The response of the request
        """
        parameters = {
            "$count": "true",
            "$filter": f"singleValueExtendedProperties/Any(ep: ep/id eq \
                        '{ZOOM_ID_EXTENDED_PROPERTY_ID}' and ep/value eq '{zoom_id}')",
            "$expand": f"singleValueExtendedProperties($filter=id eq \
                        '{ZOOM_ID_EXTENDED_PROPERTY_ID}')",
        }
        response = self.events_component.list_events(user_id, parameters, extra_headers)

        count = response.get("@odata.count", 0)
        if count == 0:
            raise NotFoundError(f"Event with zoom id {zoom_id} not found")

        if count > 1:
            logger.warning(
                "Found %s events with zoom id %s. Returning the first one.",
                count,
                zoom_id,
            )

        return response.get("value", [])[0]

    def get_event_zoom_id(
        self,
        user_id: str,
        event_id: str,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> str:
        """Get the zoom id of an event of a user

        Args:
            user_id (str): The user id
            event_id (str): The event id
            extra_headers (dict): Optional headers for the request

        Returns:
            str: The zoom id of the event
        """
        parameters = {
            "$expand": f"singleValueExtendedProperties($filter=id eq '{ZOOM_ID_EXTENDED_PROPERTY_ID}')",
        }
        response = self.events_component.get_event(
            user_id, event_id, parameters, extra_headers
        )

        for property in response["singleValueExtendedProperties"]:
            if property["id"] == ZOOM_ID_EXTENDED_PROPERTY_ID:
                return property["value"]

        raise NotFoundError(f"Zoom id not found for event {event_id}")

    def create_event(
        self,
        user_id: str,
        zoom_id: str,
        event: EventParameters,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Create an event for a user

        Args:
            user_id (str): The user id
            zoom_id (str): The zoom id of the event
            event (EventParameters): The event data
            extra_headers (dict): Optional headers for the request

        Returns:
            dict: The response of the request
        """
        json = create_event_body(event, zoom_id)
        return self.events_component.create_event(user_id, json, extra_headers)

    def update_event_by_zoom_id(
        self,
        user_id: str,
        zoom_id: str,
        event: PartialEventParameters,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> dict:
        """Update an event for a user

        Args:
            user_id (str): The user id
            zoom_id (str): The zoom id of the event
            event (EventParameters): The event parameters
            extra_headers (dict): Optional headers for the request

        Returns:
            dict: The response of the request
        """
        json = create_partial_event_body(event)
        event_id = self.get_event_by_zoom_id(user_id, zoom_id, extra_headers)["id"]
        return self.events_component.update_event(
            user_id, event_id, json, extra_headers
        )

    def delete_event_by_zoom_id(
        self,
        user_id: str,
        zoom_id: str,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Delete an event of a user

        Args:
            user_id (str): The user id
            zoom_id (str): The event id
            extra_headers (dict): Optional headers for the request

        Returns:
            dict: The response of the request
        """
        event_id = self.get_event_by_zoom_id(user_id, zoom_id, extra_headers)["id"]
        self.events_component.delete_event(user_id, event_id, extra_headers)

    def get_current_event(
        self,
        user_id: str,
    ) -> dict:
        """Get the current event of a user

        Args:
            user_id (str): The user id

        Returns:
            dict: The response of the request
        """
        datetime_now = datetime.now().isoformat()
        parameters = {
            "$count": "true",
            "$filter": f"start/dateTime le '{datetime_now}' and end/dateTime ge '{datetime_now}'",
        }
        extra_headers = {"Prefer": 'outlook.timezone="Europe/Zurich"'}
        response = self.events_component.list_events(user_id, parameters, extra_headers)

        count = response.get("@odata.count", 0)
        if count == 0:
            raise NotFoundError("No current event found")

        if count > 1:
            logger.warning("Found %s current events. Returning the first one.", count)

        return response.get("value", [])[0]
