from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Text,
    UnicodeText,
    Boolean,
    )

from models.base import Base

class Match(Base):
    """The alliances and scores for a specific match.

    Attributes:
        number: The match number.  This is used is the primary key.
        scout: The name of the scout who pit scouted the robot. This is not
            currently implemented since users have yet to be implemented.
        is_scouted: Whether the match scores have been entered yet.
        is_incomplete: Whether the scout missed some of the scoring data.

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
    number = Column(Integer, primary_key=True)

    # TODO: Add this in when users, permissions, etc. is added in.
#     scout = Column(Text, ForeignKey('users.name'), default=None)
    is_scouted = Column(Boolean, default=False)
    is_incomplete = Column(Boolean, default=False)

    r_1 = Column(Integer, ForeignKey('robots.number'))
    r_2 = Column(Integer, ForeignKey('robots.number'))
    r_3 = Column(Integer, ForeignKey('robots.number'))
    b_1 = Column(Integer, ForeignKey('robots.number'))
    b_2 = Column(Integer, ForeignKey('robots.number'))
    b_3 = Column(Integer, ForeignKey('robots.number'))


    r_disc = Column(Integer)
    r_climb = Column(Integer)
    r_foul = Column(Integer)
    r_total = Column(Integer)

    b_disc = Column(Integer)
    b_climb = Column(Integer)
    b_foul = Column(Integer)
    b_total = Column(Integer)

    def __init__(self, number, red_robots, blue_robots):
        """Initialise the match.

        Initialises the match with its number and the alliance teams.

        Args:
            number: The match number.
            red_robots: A sequence type object containing the red robots
            blue_robots: A sequence type object containing the blue robots
        """
        self.number = number
        self.r_1 = red_robots[0]
        self.r_2 = red_robots[1]
        self.r_3 = red_robots[2]
        self.b_1 = blue_robots[0]
        self.b_2 = blue_robots[1]
        self.b_3 = blue_robots[2]

    def get_red(self):
        """Get the red alliance teams

        Returns:
            A  tuple of the red alliance teams.
        """
        return r_1, r_2, r_3

    def get_blue(self):
        """Get the blue alliance teams

        Returns:
            A  tuple of the blue alliance teams.
        """
        return b_1, b_2, b_3
