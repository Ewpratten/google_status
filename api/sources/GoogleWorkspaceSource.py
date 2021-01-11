import requests
from typing import List
import json
from datetime import datetime

from .DataSource import DataSource
from ..events.Incident import Incident

class GoogleWorkspaceSource(DataSource):

    # cache of all provided service names
    _provided_service_name_cache: List[str] = None

    def getAllProvidedServiceNames(self) -> List[str]:

        # Handle building cache
        if not self._provided_service_name_cache:
            self._provided_service_name_cache = []

            # Fetch from Google
            resp = requests.get("https://www.google.com/appsstatus/json/en")

            # Handle errors
            if int(resp.status_code / 100) != 2:
                return []

            # Fetch JSON (stripping JS wrapper)
            data_json = json.loads(
                resp.text.replace("dashboard.jsonp(", "")[:-2])

            # Fetch service list
            services = data_json["services"]

            # Add to cache
            for service in services:
                self._provided_service_name_cache.append(service["name"])

        return self._provided_service_name_cache

    def getAllIncidents(self) -> List[Incident]:

        # Fetch from Google
        resp = requests.get("https://www.google.com/appsstatus/json/en")

        # Handle errors
        if int(resp.status_code / 100) != 2:
            return []

        # Fetch JSON (stripping JS wrapper)
        data_json = json.loads(resp.text.replace("dashboard.jsonp(", "")[:-2])

        # Fetch service list
        services = data_json["services"]

        # Fetch all events
        events = data_json["messages"]

        # Build incident list
        output = []
        for event in events:
            # Get the service name
            service_name = "unknown"
            for service in services:
                if service["id"] == event["service"]:
                    service_name = service["name"]

            output.append(Incident(
                time_start=datetime.fromtimestamp(event["time"]/1000),
                description=event["message"],
                service=service_name,
                severity="unknown"
            ))
        return output
