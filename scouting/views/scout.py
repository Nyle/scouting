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

position_to_text = {
    'r_1':'Red Alliance 1',
    'r_2':'Red Alliance 2',
    'r_3':'Red Alliance 3',
    'b_1':'Blue Alliance 1',
    'b_2':'Blue Alliance 2',
    'b_3':'Blue Alliance 3',
    }

@view_config(route_name='scout', renderer='../templates/scout.pt')
def scout(request):
    unscouted_robots = (DBSession
                        .query(Robot.robot_number)
                        .filter(Robot.is_scouted==False)
                        .order_by(Robot.robot_number)
                        .all()
                        )
    scouted_robots = (DBSession
                      .query(Robot.robot_number)
                      .filter(Robot.is_scouted==True)
                      .order_by(Robot.robot_number)
                      .all()
                      )
    matches = (DBSession
               .query(Match)
               .order_by(Match.match_number)
               .all()
               )
    return {
        'unscouted_robots':unscouted_robots,
        'scouted_robots':scouted_robots,
        'matches':matches
        }

@view_config(route_name='scout_robot',
             renderer='../templates/scout/scout_robot.pt')
def scout_robot(request):
    message = ''
    robot_number = int(request.matchdict['robot_number'])
    robot = DBSession.query(Robot).filter(
        Robot.robot_number == robot_number).first()
    if robot is None:
        return HTTPFound(location=request.route_url('scout'))
    if request.method == 'POST':
        try:
            values = robot.validate(request)
        except ValidationError as e:
            return {
                'page_title':'Robot ' + str(robot_number),
                'submit_location':request.route_url('scout_robot',
                                                    robot_number=robot_number),
                'message':e.message,
                'robot':e.values,
                }
        if 'unfinished' in request.POST:
            values['is_scouted'] = False
        else:
            values['is_scouted'] = True
        robot.set(values)
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
    if robot.is_scouted:
        message = 'Note: This robot has allready been scouted'
    return {
        'page_title':'Robot ' + str(robot_number),
        'submit_location':request.route_url('scout_robot',
                                            robot_number=robot_number),
        'message':message,
        'robot':robot.__dict__
        }

# @view_config(route_name='scout_match',
#              renderer='../templates/scout/scout_match.pt')
# def scout_match(request):
#     message = ''
#     match_number = int(request.matchdict['match_number'])
#     match = DBSession.query(Match).filter(
#         Match.match_number == match_number).first()
#     if match is None:
#         return HTTPFound(location=request.route_url('scout'))
#     if request.method == 'POST':
#         try:
#             values = match.validate(request)
#         except ValidationError as e:
#             return {
#                 'page_title':'Match ' + str(match_number),
#                 'submit_location':request.route_url('scout_match',
#                                                     match_number=match_number),
#                 'message':e.message,
#                 'match':e.values,
#                 }
#         if 'unfinished' in request.POST:
#             values['is_scouted'] = False
#         else:
#             values['is_scouted'] = True
#         match.set(values)
#         DBSession.add(match)
#         return HTTPFound(location=request.route_url('scout_match',
#             match_number=match_number + 1))
#     return {
#         'page_title':'Match ' + str(match_number),
#         'submit_location':request.route_url('scout_match',
#                                             match_number=match_number),
#         'message':message,
#         'match':match.__dict__,
#         }

@view_config(route_name='scout_robot_match',
             renderer='../templates/scout/scout_robot_match.pt')
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
            values = robot_match.validate(request)
        except ValidationError as e:
            return {
                'page_title':('Robot ' + str(robot_number) +
                      ', Match ' + str(match_number)),
                'submit_location':request.route_url('scout_robot_match',
                                                    robot_number=robot_number,
                                                    match_number=match_number),
                'message':e.message,
                'robot_match':e.values,
                }
        if 'unfinished' in request.POST:
            values['is_scouted'] = False
        else:
            values['is_scouted'] = True
        robot_match.set(values)
        DBSession.add(robot_match)
        return HTTPFound(location=request.route_url(
            'scout_robot_match',
            match_number=robot_match.match_number + 1,
            robot_number=getattr(
                DBSession.query(Match).filter(Match.match_number==
                    robot_match.match_number + 1).first(),
                robot_match.position
                )))
    if robot_match.is_scouted:
        message = 'Note: This robot match has allready been scouted'
    return {
        'page_title':('Robot ' + str(robot_number) +
                      ', Match ' + str(match_number) +
                      ', ' + position_to_text[robot_match.position]),
        'submit_location':request.route_url('scout_robot_match',
                                            robot_number=robot_number,
                                            match_number=match_number),
        'message':message,
        'robot_match':robot_match.__dict__,
        }
