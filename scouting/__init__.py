from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('view', '/view')
    config.add_route('view_robot', '/view/r{robot_number:\d+}')
    config.add_route('view_match', '/view/m{match_number:\d+}')

    config.add_route('pit_scout', '/scout/pits')
    config.add_route('scout_robot', '/scout/r{robot_number:\d+}')

    config.add_route('scout', '/scout')
    config.add_route('scout_match', '/scout/m{match_number:\d+}')
    config.add_route('scout_robot_match',
                     '/scout/r{robot_number:\d+}m{match_number:\d+}')
    config.scan()
    return config.make_wsgi_app()
