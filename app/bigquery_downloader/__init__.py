"""Configures what to download from bigquery"""

import pathlib

from mara_config import set_config, register_functionality

import app.config


def compose_bigquery_downloader():
    import bigquery_downloader
    register_functionality(bigquery_downloader)

    @set_config('bigquery_downloader.config.data_sets')
    def data_sets():
        import bigquery_downloader.config
        return [
            bigquery_downloader.config.DataSet(
                query_file_path=pathlib.Path('app/bigquery_downloader/pypi-downloads.sql'),
                json_credentials_path='app/bigquery_downloader/bigquery-credentials.json',
                first_date=app.config.first_date(),
                output_file_name='pypi/downloads-v1.csv.gz',
                use_legacy_sql=False,
                data_dir=app.config.data_dir()),
            bigquery_downloader.config.DataSet(
                query_file_path=pathlib.Path('app/bigquery_downloader/github-repo-activity.sql'),
                json_credentials_path='app/bigquery_downloader/bigquery-credentials.json',
                first_date=app.config.first_date(),
                output_file_name='github/repo-activity-v1.csv.gz',
                use_legacy_sql=False,
                data_dir=app.config.data_dir())
        ]
