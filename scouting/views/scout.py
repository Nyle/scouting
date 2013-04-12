from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
    )
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from ..models import (
    ValidationError,
    DBSession,
    Robot,
    Match,
    RobotMatch
    )

@view_config(route_name='pit_scout', renderer='../templates/pit_scout.pt')
def pit_scout(request):
    scouted_robots = (DBSession.query(Robot.number).filter(Robot.is_scouted)
                      .order_by(Robot.robot_number))
    return {
        'scouted_robots':scouted_robots,
        'unscouted_robots':unscouted_robots,
        }

@view_config(route_name='scout_robot', renderer='../templates/scout_robot.pt')
def scout_robot(request):
    message = ''
    robot_number = int(request.matchdict['robot_number'])
    robot = DBSession.query(Robot).filter(
        Robot.robot_number == robot_number).first()
    if robot is None:
        return HTTPFound(location=request.route_url('scout'))
    if request.method == 'POST':
        try:
            robot.set(robot.validate(request))
        except ValidationError as e:
            return {
                'message':e.message,
                'robot':e.values,
                }
        if 'done' in request.POST:
            robot.is_scouted = True
        elif 'come_back' in request.POST:
            robot.is_scouted = False
        DBSession.add(robot)
        unscouted_robots = (DBSession.query(Robot).filter(Robot.is_scouted ==
            False).order_by(Robot.robot_number))
        if unscouted_robots.all():
            next_robot = (unscouted_robots.filter(Robot.robot_number >
                robot_number).first())
            if next_robot:
                return HTTPFound(location=request.route_url('scout_robot',
                    robot_number=next_robot.robot_number))
            return HTTPFound(location=request.route_url('scout_robot',
                robot_number=unscouted_robots.first().robot_number))
        return HTTPFound(location=request.route_url('scout'))
    return {
        'message':message,
        'robot':robot.__dict__
        }

@view_config(route_name='scout', renderer='../templates/scout.pt')
def scout(request):
    return {}

@view_config(route_name='scout_match', renderer='../templates/scout_match.pt')
def scout_match(request):
    message = ''
    match_number = int(request.matchdict['match_number'])
    match = DBSession.query(Match).filter(
        Match.match_number == match_number).first()
    if match is None:
        return HTTPFound(location=request.route_url('scout'))
    if request.method == 'POST':
        try:
            match.set(match.validate(request))
        except ValidationError as e:
            return {
                'message':e.message,
                'match':e.values,
                }
        if 'done' in request.POST:
            match.is_scouted = True
        elif 'come_back' in request.POST:
            match.is_scouted = False
        DBSession.add(robot)
        return HTTPFound(location=request.route_url('scout_match',
            match_number=match_number + 1))
    return {
        'message':message,
        'match':match.__dict__,
        }

@view_config(route_name='scout_robot_match',
             renderer='../templates/scout_robot_match.pt')
def scout_robot_match(request):
    message = ''
    robot_number = int(request.matchdict['robot_number'])
    match_number = int(request.matchdict['match_number'])
    robot_match = DBSession.query(RobotMatch).filter(RobotMatch.match_number ==
        match_number).filter(RobotMatch.robot_number == robot_number).first()
    if robot_match is None:
        return HTTPFound(location=request.route_url('scout'))
    if request.method == 'POST':
        try:
            robot_match.set(match.validate(request))
        except ValidationError as e:
            return {
                'message':e.message,
                'robot_match':e.values,
                }
        if 'done' in request.POST:
            robot_match.is_scouted = True
        elif 'come_back' in request.POST:
            robot_match.is_scouted = False
        DBSession.add(robot_match)
        return HTTPFound(location=request.route_url(
            'scout_robot_match',
            match_number=robot_match.match_number + 1,
            robot_number=getattr(
                DBSession.query(Match).filter(Match.match_number==
                    robot_match.match_number).first(),
                robot_match.position
                )))
    return {
        'message':message,
        'robot_match':robot_match.__dict__,
        }
