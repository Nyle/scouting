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
    ValidationError,
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

    def __init__(self, match_number, r_1, r_2, r_3, b_1, b_2, b_3):
        """Initialise the match.

        Initialises the match with its number and the alliance teams.

        Args:
            match_number: The match number.
            r_1, r_2, r_3: The red alliance's robot's numbers
            b_1, b_2, b_3: The blue alliance's robot's numbers
        """
        self.match_number = match_number
        self.r_1 = r_1
        self.r_2 = r_2
        self.r_3 = r_3
        self.b_1 = b_1
        self.b_2 = b_2
        self.b_3 = b_3
        is_scouted = False

        # Create the robot matches for the match
        # TODO: Find out how to make it so if the match is deleted the robot
        #       matches will be too
        DBSession.add(RobotMatch(match_number=match_number,
                                 robot_number=self.r_1,
                                 position='r_1'))
        DBSession.add(RobotMatch(match_number=match_number,
                                 robot_number=self.r_2,
                                 position='r_2'))
        DBSession.add(RobotMatch(match_number=match_number,
                                 robot_number=self.r_3,
                                 position='r_3'))
        DBSession.add(RobotMatch(match_number=match_number,
                                 robot_number=self.b_1,
                                 position='b_1'))
        DBSession.add(RobotMatch(match_number=match_number,
                                 robot_number=self.b_2,
                                 position='b_2'))
        DBSession.add(RobotMatch(match_number=match_number,
                                 robot_number=self.b_3,
                                 position='b_3'))

    def validate(self, request):
        """Validate a request.

        Validates the data in the request and returns the validated data.

        Args:
            request: A request which contains the results of a form into which
                match data was entered as POST data.

        Returns:
            A dictionary of the validated values.

        Raises:
            ValidationError: The form data in request doesn't validate.

        """
        values = {
            'r_disc':request.POST['r_disc'],
            'r_climb':request.POST['r_climb'],
            'r_foul':request.POST['r_foul'],
            'r_total':request.POST['r_total'],
            'b_disc':request.POST['b_disc'],
            'b_climb':request.POST['b_climb'],
            'b_foul':request.POST['b_foul'],
            'b_total':request.POST['b_total'],
            'comments':request.POST['comments']
            }
        try:
            values['r_disc'] = int(values['r_disc'])
            values['r_climb'] = int(values['r_climb'])
            values['r_foul'] = int(values['r_foul'])
            values['r_total'] = int(values['r_total'])
            values['b_disc'] = int(values['b_disc'])
            values['b_climb'] = int(values['b_climb'])
            values['b_foul'] = int(values['b_foul'])
            values['b_total'] = int(values['b_total'])
        except ValueError:
            raise ValidationError(
                'All point values must be integers',
                self.__dict__.copy().update(values)
                )
        if (values['r_disc'] + values['r_climb'] + values['r_foul'] !=
            values['r_total']):
            raise ValidationError(
                ('The sum of all red point categories must be equal to the'
                 'total red points'),
                self.__dict__.copy().update(values)
                )
        if b_disc + b_climb + b_foul != b_total:
            raise ValidationError(
                ('The sum of all blue point categories must be equal to the'
                 'total blue points'),
                self.__dict__.copy().update(values)
                )
        return values

    def set(self, values):
        """Set the match's values.

        Sets the values of the match to values.

        Args:
            values: A dictionary of values returned by Match.validate().  These
                values should have already been validated.
        """
        self.r_disc = values['r_disc']
        self.r_climb = values['r_climb']
        self.r_foul = values['r_foul']
        self.r_total = values['r_total']
        self.b_disc = values['b_disc']
        self.b_climb = values['b_climb']
        self.b_foul = values['b_foul']
        self.b_total = values['b_total']
