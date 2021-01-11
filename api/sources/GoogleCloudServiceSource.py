import requests
from typing import List
import datetime

from .DataSource import DataSource
from ..events.Incident import Incident


class GoogleCloudServiceSource(DataSource):

    # cache of all provided service names
    _provided_service_name_cache: List[str] = None

    def getAllProvidedServiceNames(self) -> List[str]:

        # Handle building cache
        if not self._provided_service_name_cache:
            self._provided_service_name_cache = []

            # Fill the cache
            for item in self.getAllIncidents():
                self._provided_service_name_cache.append(item.service)

            # Filter duplicates
            self._provided_service_name_cache = list(
                dict.fromkeys(self._provided_service_name_cache))

        return self._provided_service_name_cache

    def getAllIncidents(self) -> List[Incident]:

        # Fetch from Google
        resp = requests.get("https://status.cloud.google.com/incidents.json")

        # Handle errors
        if int(resp.status_code / 100) != 2:
            return []

        # Parse to JSON
        data_json = resp.json()

        # Handle every item
        output = []
        for event in data_json:
            # Calculate end time
            end_time = None
            if "end" in event and event["end"]:
                end_time = datetime.datetime.strptime(event["end"], '%Y-%m-%dT%H:%M:%SZ')
            
            output.append(Incident(
                time_start=datetime.datetime.strptime(event["begin"], '%Y-%m-%dT%H:%M:%SZ'),
                time_end=end_time,
                description=event["external_desc"],
                service=event["service_name"],
                severity=event["severity"],
                url="https://status.cloud.google.com"+event["uri"]
            ))
        return output
