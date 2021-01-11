from typing import List
from ..events.Incident import Incident


class DataSource(object):

    def getAllIncidents(self) -> List[Incident]:
        return []

    def getAllProvidedServiceNames(self) -> List[str]:
        return []
