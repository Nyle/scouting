from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import notfound_view_config
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

@notfound_view_config(append_slash=True)
def notfound(request):
    return HTTPNotFound('Page Not Found')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=0)

    config.add_route('view', '/view')
    config.add_route('view_robot', '/view/r{robot_number:\d+}')

    config.add_route('scout', '/')
    config.add_route('scout_robot', '/r{robot_number:\d+}')
#     config.add_route('scout_match', '/m{match_number:\d+}')
    config.add_route('scout_robot_match',
                     '/r{robot_number:\d+}m{match_number:\d+}')
    config.scan()
    return config.make_wsgi_app()
