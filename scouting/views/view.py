from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
    )
from sqlalchemy.exc import DBAPIError
from ..models import (
    DBSession,
    Robot,
    Match,
    RobotMatch
    )


@view_config(route_name='view', renderer='../templates/view.pt')
def view(request):
    return {}

@view_config(route_name='view_robot', renderer='../templates/view_robot.pt')
def view_robot(request):
    return {}

@view_config(route_name='view_match', renderer='../templates/view_match.pt')
def view_match(request):
    return {}
