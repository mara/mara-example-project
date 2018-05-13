"""Set up Navigation, ACL & Logos"""

import flask
from mara_config import set_config, register_functionality

from app.ui import start_page

blueprint = flask.Blueprint('ui', __name__, url_prefix='/ui', static_folder='static')

MARA_FLASK_BLUEPRINTS = [start_page.blueprint, blueprint]


def compose_ui():
    import mara_acl
    import mara_app
    import mara_db
    import mara_page
    import data_integration
    from mara_page import acl
    from mara_page import navigation
    import mara_acl.users
    import mara_acl.permissions
    register_functionality(mara_acl)
    register_functionality(mara_page)
    register_functionality(mara_app)
    register_functionality(mara_db)
    register_functionality(data_integration)

    # replace logo and favicon
    set_config('mara_app.config.favicon_url')(lambda: flask.url_for('ui.static', filename='favicon.ico'))
    set_config('mara_app.config.logo_url')(lambda: flask.url_for('ui.static', filename='logo.png'))

    # add custom css
    @set_config('mara_app.layout.css_files', include_original_function=True)
    def css_files(original_function, response):
        files = original_function(response)
        files.append(flask.url_for('ui.static', filename='styles.css'))
        return files

    # define protected ACL resources
    @set_config('mara_acl.config.resources')
    def acl_resources():
        def iter(iterator_or_callable):
            if callable(iterator_or_callable):
                iterator_or_callable = iterator_or_callable()
            return iterator_or_callable

        return [acl.AclResource(name='Documentation',
                                children=iter(data_integration.MARA_ACL_RESOURCES)
                                         + iter(mara_db.MARA_ACL_RESOURCES)),
                acl.AclResource(name='Admin',
                                children=iter(mara_app.MARA_ACL_RESOURCES) + iter(mara_acl.MARA_ACL_RESOURCES))]

    # activate ACL
    set_config('mara_page.acl.current_user_email')(mara_acl.users.current_user_email)
    set_config('mara_page.acl.current_user_has_permission')(mara_acl.permissions.current_user_has_permission)
    set_config('mara_page.acl.current_user_has_permissions')(mara_acl.permissions.current_user_has_permissions)

    set_config('mara_acl.config.whitelisted_uris')(lambda: ['/mara-app/navigation-bar'])

    # navigation bar (other navigation entries will be automatically added)
    @set_config('mara_app.config.navigation_root')
    def navigation_root() -> navigation.NavigationEntry:
        def navigation_entries(module):
            navigation_entries = module.MARA_NAVIGATION_ENTRY_FNS
            if callable(navigation_entries):
                navigation_entries = navigation_entries()

            return [fn() for fn in navigation_entries]

        return navigation.NavigationEntry(label='Root', children=(
                navigation_entries(data_integration)
                + [navigation.NavigationEntry('Settings', icon='cog', description='ACL & Configuration', rank=100,
                                              children=navigation_entries(mara_app) + navigation_entries(mara_acl))]))
