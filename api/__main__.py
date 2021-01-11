import flask
from webapputils import Webapp
import requests
from typing import List
from datetime import datetime

from .events.Incident import Incident
from .sources.DataSource import DataSource
from .sources.GoogleCloudServiceSource import GoogleCloudServiceSource
from .sources.GoogleWorkspaceSource import GoogleWorkspaceSource

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)

# Service providers
providers: List[DataSource] = [
    GoogleCloudServiceSource(),
    GoogleWorkspaceSource()
]


@app.errorhandler(404)
def page_not_found(e):
    return "Error 404", 404
    # return flask.render_template('404.html'), 404

@app.route("/")
def index():
    return flask.render_template('index.html')


@app.route("/api/services")
def getServices():

    # Fetch services from each provider
    services: List[str] = []
    for provider in providers:
        services += provider.getAllProvidedServiceNames()

    return flask.jsonify({
        "success": "true",
        "services": services
    })
    
@app.route("/api/incidents")
def getIncidents():

    # Fetch incidents from each provider
    incidents: List[str] = []
    for provider in providers:
        incidents += provider.getAllIncidents()
        
    # Sort by start time
    incidents.sort(key=lambda x: datetime.timestamp(x.time_start), reverse=True)

    return flask.jsonify({
        "success": "true",
        "incidents": incidents
    })


if __name__ == "__main__":
    app.run(debug=True)
