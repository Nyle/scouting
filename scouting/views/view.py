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
    robots = DBSession.query(Robot).order_by(Robot.robot_number).all()
    matches = DBSession.query(Match).order_by(Match.match_number).all()
    return {
        'robots':robots,
        'matches':matches,
        }

@view_config(route_name='view_robot',
             renderer='../templates/view/view_robot.pt')
def view_robot(request):
    robot_number = int(request.matchdict['robot_number'])
    robot = DBSession.query(Robot).filter(
        Robot.robot_number==robot_number).first()
    scouted_robot_matches = (DBSession
                             .query(RobotMatch)
                             .filter(RobotMatch.robot_number==robot_number)
                             .filter(RobotMatch.is_scouted==True)
                             .order_by(RobotMatch.match_number)
                             .all()
                             )
    unscouted_robot_matches = (DBSession
                               .query(RobotMatch)
                               .filter(RobotMatch.robot_number==robot_number)
                               .filter(RobotMatch.is_scouted==False)
                               .order_by(RobotMatch.match_number)
                               .all()
                               )
    if robot is None:
        return HTTPFound(location=request.route_url('view'))
    return {
        'robot':robot,
        'scouted_robot_matches':scouted_robot_matches,
        'unscouted_robot_matches':unscouted_robot_matches,
        }
