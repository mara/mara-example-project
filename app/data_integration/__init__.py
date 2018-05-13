"""Configures the data integration pipelines of the project"""

import datetime
import functools

from mara_config import set_config, register_functionality

import app.config


def compose_data_integration():
    import data_integration
    import etl_tools
    register_functionality(data_integration)
    register_functionality(etl_tools)
    set_config('data_integration.config.data_dir')(lambda: app.config.data_dir())
    set_config('data_integration.config.first_date')(lambda: app.config.first_date())
    set_config('data_integration.config.default_db_alias')(lambda: 'dwh')

    @set_config('data_integration.config.root_pipeline')
    @functools.lru_cache(maxsize=None)
    def root_pipeline():
        from data_integration.pipelines import Pipeline
        import app.data_integration.pipelines.github
        import app.data_integration.pipelines.pypi
        import app.data_integration.pipelines.utils
        import app.data_integration.pipelines.python_projects

        pipeline = Pipeline(
            id='mara_example_project',
            description='An example pipeline that integrates PyPI download stats with the Github activity of a project')

        pipeline.add(app.data_integration.pipelines.utils.pipeline)
        pipeline.add(app.data_integration.pipelines.pypi.pipeline, upstreams=['utils'])
        pipeline.add(app.data_integration.pipelines.github.pipeline, upstreams=['utils'])
        pipeline.add(app.data_integration.pipelines.python_projects.pipeline,
                     upstreams=['pypi', 'github'])
        return pipeline

    set_config('etl_tools.config.number_of_chunks')(lambda: 11)
    set_config('etl_tools.config.first_date_in_time_dimensions')(lambda: app.config.first_date())
    set_config('etl_tools.config.last_date_in_time_dimensions')(
        lambda: datetime.datetime.utcnow().date() - datetime.timedelta(days=1))
