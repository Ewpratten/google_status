import flask
from webapputils import Webapp
import requests
from typing import List

from .events.Incident import Incident
from .sources.DataSource import DataSource
from .sources.GoogleCloudServiceSource import GoogleCloudServiceSource

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)

# Service providers
providers: List[DataSource] = [
    GoogleCloudServiceSource()
]


@app.errorhandler(404)
def page_not_found(e):
    return "Error 404", 404
    # return flask.render_template('404.html'), 404


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


if __name__ == "__main__":
    app.run(debug=True)
