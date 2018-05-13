import pathlib
import sys

from mara_config import register_functionality

def compose_mara_app():
    # configure application and packages
    import app.data_integration
    import app.bigquery_downloader
    import app.ui

    app.data_integration.compose_data_integration()
    app.bigquery_downloader.compose_bigquery_downloader()
    app.ui.compose_ui()
    register_functionality(app.ui)


# the flask app
def create_app():
    from mara_app.app import MaraApp
    return MaraApp()
