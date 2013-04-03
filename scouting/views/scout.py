from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
    )
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from ..models import (
    DBSession,
    Robot,
    Match,
    RobotMatch
    )

@view_config(route_name='scout', renderer='../templates/scout.pt')
def scout(request):
    return {}

@view_config(route_name='scout_robot', renderer='../templates/scout_robot.pt')
def scout_robot(request):
    message = ''
    robot_number = int(request.matchdict['robot_number'])
    robot = DBSession.query(Robot).filter(
        Robot.robot_number == robot_number).first()
    # TODO: Deal with trying to scout a non-existent robot
    if request.method == 'POST':
        robot.description = request.POST['description']
        robot.wheels = request.POST['wheels']
        robot.gearbox = request.POST['gearbox']
        robot.motors = request.POST['motors']
        robot.can_shoot = 'can_shoot' in request.POST
        robot.can_climb = 'can_climb' in request.POST
        robot.can_human_load = 'can_human_load' in request.POST
        robot.can_ground_load = 'can_ground_load' in request.POST
        robot.is_scouted = True if 'done' in request.POST else False
        DBSession.add(robot)
        unscouted_robots = (DBSession.query(Robot).filter(Robot.is_scouted
            == False).order_by(Robot.robot_number))
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
        'robot_number':robot.robot_number,
        'is_scouted':robot.is_scouted,
        'description':robot.description,
        'wheels':robot.wheels,
        'motors':robot.motors,
        'gearbox':robot.gearbox,
        'can_shoot':robot.can_shoot,
        'can_climb':robot.can_climb,
        'can_human_load':robot.can_human_load,
        'can_ground_load':robot.can_ground_load,
        }

@view_config(route_name='scout_match', renderer='../templates/scout_match.pt')
def scout_match(request):
    message = ''
    match_number = int(request.matchdict['match_number'])
    match = DBSession.query(Match).filter(
        Match.match_number == match_number).first()
    if match is None:
        return HTTPFound(location=request.route_url('scout'))
    is_scouted = match.is_scouted
    comments = match.comments
    red = match.red
    blue = match.blue
    r_points = match.r_points
    b_points = match.b_points
    if request.method == 'POST':
        comments = request.POST['comments']
        r_points = {
            'disc':int(request.POST['r_disc']),
            'climb':int(request.POST['r_climb']),
            'foul':int(request.POST['r_foul']),
            'total':int(request.POST['r_total']),
            }
        b_points = {
            'disc':int(request.POST['b_disc']),
            'climb':int(request.POST['b_climb']),
            'foul':int(request.POST['b_foul']),
            'total':int(request.POST['b_total']),
            }
        def verify():
            message = ''
            if (r_points['total'] !=
                r_points['disc'] + r_points['climb'] + r_points['foul']):
                message = ('Red total points does not equal the sum of all of '
                           'the red points')
                return False, message
            if (b_points['total'] !=
                b_points['disc'] + b_points['climb'] + b_points['foul']):
                message = ('Blue total points does not equal the sum of all of '
                           'the blue points')
                return False, message
            return True, message
        verified, message = verify()
        if verified:
            match.comments = comments
            match.is_scouted = True if 'done' in request.POST else False
            match.set_points(r_points=r_points, b_points=b_points)
            return HTTPFound(location=request.route_url('scout_match',
                match_number=match_number + 1))
    return {
        'message':message,
        'match_number':match_number,
        'comments':comments,
        'is_scouted':is_scouted,
        'red':red,
        'blue':blue,
        'r_points':r_points,
        'b_points':b_points,
        }

@view_config(route_name='scout_robot_match',
             renderer='../templates/scout_robot_match.pt')
def scout_robot_match(request):
    return {}
