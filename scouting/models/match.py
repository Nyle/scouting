from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Text,
    UnicodeText,
    Boolean,
    )

from .base import (
    Base,
    DBSession,
    )

from .robot_match import RobotMatch

class Match(Base):
    """The alliances and scores for a specific match.

    Attributes:
        match_number: The match number.  This is used is the primary key.

        scout: The name of the scout who pit scouted the robot. This is not
            currently implemented since users have yet to be implemented.
        is_scouted: Whether the match scores have been entered yet.
        comments: Any comments from the scouter about the match.

        r_1: Red robot 1.
        r_2: Red robot 2.
        r_3: Red robot 3.

        b_1: Blue robot 1.
        b_2: Blue robot 2.
        b_3: Blue robot 3.

        r_disc: Red disc points.
        r_climb: Red climb points.
        r_foul: Red foul points.
        r_total: Red total points.

        b_disc: Blue disc points.
        b_climb: Blue climb points.
        b_foul: Blue foul points.
        b_total: Blue total points.
    """
    __tablename__ = 'matches'
    match_number = Column(Integer, primary_key=True)

    # TODO: Add this in when users, permissions, etc. is added in.
#     scout = Column(Text, ForeignKey('users.name'), default=None)
    is_scouted = Column(Boolean)
    comments = Column(UnicodeText)

    r_1 = Column(Integer, ForeignKey('robots.robot_number'))
    r_2 = Column(Integer, ForeignKey('robots.robot_number'))
    r_3 = Column(Integer, ForeignKey('robots.robot_number'))

    b_1 = Column(Integer, ForeignKey('robots.robot_number'))
    b_2 = Column(Integer, ForeignKey('robots.robot_number'))
    b_3 = Column(Integer, ForeignKey('robots.robot_number'))

    r_disc = Column(Integer)
    r_climb = Column(Integer)
    r_foul = Column(Integer)
    r_total = Column(Integer)

    b_disc = Column(Integer)
    b_climb = Column(Integer)
    b_foul = Column(Integer)
    b_total = Column(Integer)

    def __init__(self, match_number, red_robots, blue_robots):
        """Initialise the match.

        Initialises the match with its number and the alliance teams.

        Args:
            match_number: The match number.
            red_robots: A sequence type object or a dictionary with 0, 1, and 2
                as keys, corresponding to teams 1, 2, and 3 respectively
                containing the red robots.
            blue_robots: A sequence type object or a dictionary with 0, 1, and 2
                as keys, corresponding to teams 1, 2, and 3 respectively
                containing the blue robots.
        """
        self.match_number = match_number
        self.r_1 = red_robots[0]
        self.r_2 = red_robots[1]
        self.r_3 = red_robots[2]
        self.b_1 = blue_robots[0]
        self.b_2 = blue_robots[1]
        self.b_3 = blue_robots[2]
        is_scouted = False

        # Create the robot matches for the match
        # TODO: Find out how to make it so if the match is deleted the robot
        #       matches will be too
        for robot_number in self.red + self.blue:
            DBSession.add(RobotMatch(match_number=match_number,
                                     robot_number=robot_number))

    @property
    def red(self):
        """Get the red alliance teams.

        Returns:
            A  tuple of the red alliance teams.
        """
        return self.r_1, self.r_2, self.r_3

    @property
    def blue(self):
        """Get the blue alliance teams.

        Returns:
            A  tuple of the blue alliance teams.
        """
        return self.b_1, self.b_2, self.b_3

    @property
    def r_points(self):
        """Get the red alliance points.

        Returns:
            A dictionary of the points scored by the red alliance with the keys
            disc, climb, foul, total.
        """
        return {
            'disc':self.r_disc,
            'climb':self.r_climb,
            'foul':self.r_foul,
            'total':self.r_total,
            }

    @property
    def b_points(self):
        """Get the blue alliance points.

        Returns:
            A dictionary of the points scored by the blue alliance with the keys
            disc, climb, foul, total.
        """
        return {
            'disc':self.b_disc,
            'climb':self.b_climb,
            'foul':self.b_foul,
            'total':self.b_total,
            }

    def set_points(self, r_points, b_points):
        """Set the matches points.

        Uses two dictionaries of the form output by r_points() and b_points() to
        set the matches points.

        Args:
            r_points: A dictionary containing the red alliance points.
            b_points: A dictionary containing the blue alliance points.
        """
        r_disc = r_points['disc']
        r_climb = r_points['climb']
        r_foul = r_points['foul']
        r_total = r_points['total']
        b_disc = b_points['disc']
        b_climb = b_points['climb']
        b_foul = b_points['foul']
        b_total = b_points['total']
