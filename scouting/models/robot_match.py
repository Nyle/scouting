from sqlalchemy import (
    Enum,
    ForeignKey,
    Column,
    Integer,
    UnicodeText,
    Boolean,
    )

from .base import Base

class RobotMatch(Base):
    """The data gathered for a specific robot in a specific match.

    Attributes:
        id: The primary key for the robot_match.
        match_number: The match number.
        robot_number: The robot number.

        robot_match_comments: Any comments by the scout about the robot, especially
            strategy suggestions.

        did_foul: Whether the robot fouled in the match.
        did_technical_foul: Whether the robot technical fouled in the match.
        foul_description: A description of any fouls committed by the robot in
            the match.

        did_shoot: Whether the robot made any attempt to shoot/dump any frisbees
            in the match.
        auto_1: Frisbees put into the low goal in auto by the robot.
        auto_2: Frisbees put into the middle goals in auto by the robot.
        auto_3: Frisbees put into the high goal in auto by the robot.
        auto_miss: Frisbees missed in auto by the robot.
        teleop_1: Frisbees put into the low goal in teleop by the robot.
        teleop_2: Frisbees put into the middle goals in teleop by the robot.
        teleop_3: Frisbees put into the high goal in teleop by the robot.
        teleop_5: Frisbees put into the pyramid goal in teleop by the robot.
        teleop_miss: Frisbees missed in teleop by the robot.
        shooting_description: A description of the shooting of the robot: how
            well it shoots, where it shoots from, strategy suggestions, etc.

        did_climb: Whether the robot attempted to climb in the match.
        climb_start: How long before the end of the match the robot started to
            climb.
        climb_end: How long before the end of the match the robot stopped
            climbing.
        frisbees_dumped: How many frisbees the robot dumped into the pyramid
            goal.
        did_fall_off_pyramid: Whether the robot fell of the pyramid while climbing.
        climbing_description: A description of how the robot climbed in the
            match, how sturdy it looked, strategy suggestions, etc.

        did_human_load: Whether the robot attempted to human load in the match.

        did_ground_load: Whether the robot ground loaded in the match.
        auto_frisbees_ground_loaded: How many frisbees the robot ground loaded
            in auto.

        loading_description: A description of the robots loading: what it was
            good at, what it wasn't good at, strategy suggestions, etc.

    """
    __tablename__ = 'robot_matches'
    id = Column(Integer, primary_key=True)
    match_number = Column(Integer)
    robot_number = Column(Integer)
    position = Column(Enum('r_1', 'r_2', 'r_3', 'b_1', 'b_2', 'b_3'))

    # TODO: Add this in when users, permissions, etc. is added in.
#     scout = Column(Text, ForeignKey('users.name'), default=None)
    is_scouted = Column(Boolean, default=False)

    robot_match_comments = Column(UnicodeText)

    did_foul = Column(Boolean)
    did_technical_foul = Column(Boolean)
    foul_description = Column(UnicodeText)

    did_shoot = Column(Boolean)
    auto_1 = Column(Integer)
    auto_2 = Column(Integer)
    auto_3 = Column(Integer)
    auto_miss = Column(Integer)
    teleop_1 = Column(Integer)
    teleop_2 = Column(Integer)
    teleop_3 = Column(Integer)
    teleop_5 = Column(Integer)
    teleop_miss = Column(Integer)
    shooting_description = Column(UnicodeText)

    did_climb = Column(Boolean)
    climb_start = Column(Integer)
    climb_finish = Column(Integer)
    level_reached = Column(Integer)
    frisbees_dumped = Column(Integer)
    did_fall_off_pyramid = Column(Boolean)
    climbing_description = Column(UnicodeText)

    did_human_load = Column(Boolean)

    did_ground_load = Column(Boolean)
    auto_frisbees_ground_loaded = Column(Integer)

    loading_description = Column(UnicodeText)

    def __init__(self, match_number, robot_number, position):
        """Initialise the robot_match.

        Initialises the robot_match with its robot and match numbers.

        Args:
            match_number: The match number.
            robot_number: The robot number.
        """
        self.match_number = match_number
        self.robot_number = robot_number
        self.position = position

    def validate(self, request):
        """Validate a request.

        Validates the data in the request and returns the validated data.

        Args:
            request: A request which contains the results of a form into which
                robot_match data was entered as POST data.

        Returns:
            A dictionary of the validated values.

        Raises:
            ValidationError: The form data in request doesn't validate.

        """
        values = {
            'is_scouted':request.POST['comments'],
            'robot_match_comments':request.POST['robot_match_comments'],
            'did_foul':'did_foul' in request.POST,
            'did_technical_foul':request.POST['did_technical_foul'],
            'foul_description':request.POST['foul_description'],
            'did_shoot':'did_shoot' in request.POST,
            'auto_1':request.POST['auto_1'],
            'auto_2':request.POST['auto_2'],
            'auto_3':request.POST['auto_3'],
            'auto_miss':request.POST['auto_miss'],
            'teleop_1':request.POST['teleop_1'],
            'teleop_2':request.POST['teleop_2'],
            'teleop_3':request.POST['teleop_3'],
            'teleop_5':request.POST['teleop_5'],
            'teleop_miss':request.POST['teleop_miss'],
            'shooting_description':request.POST['shooting_description'],
            'did_climb':'did_climb' in request.POST,
            'climb_start':request.POST['climb_start'],
            'climb_finish':request.POST['climb_finish'],
            'level_reached':request.POST['level_reached'],
            'frisbees_dumped':request.POST['frisbees_dumped'],
            'did_fall_off_pyramid':'did_fall_off_pyramid' in request.POST,
            'climbing_dscription':request.POST['climbing_description'],
            'did_human_load':'did_human_load' in request.POST,
            'did_ground_load':'did_ground_load' in request.POST,
            'auto_frisbees_ground_loaded':\
                request.POST['auto_frisbees_ground_loaded'],
            'loading_description':request.POST['loading_description'],
            }
        if ((values['did_foul'] or values['did_technical_foul']) and
            not values['foul_description']):
            raise ValidationError(
                'Please enter a description of the foul(s) the robot committed'
                self.__dict__().copy().update(values)
                )
        if values['did_shoot']:
            try:
                values['auto_1'] = int(values['auto_1'])
                values['auto_2'] = int(values['auto_2'])
                values['auto_3'] = int(values['auto_3'])
                values['auto_miss'] = int(values['auto_miss'])
                values['teleop_1'] = int(values['teleop_1'])
                values['teleop_2'] = int(values['teleop_2'])
                values['teleop_3'] = int(values['teleop_3'])
                values['teleop_4'] = int(values['teleop_4'])
                values['teleop_5'] = int(values['teleop_5'])
                values['teleop_miss'] = int(values['teleop_miss'])
            except ValueError:
                raise ValidationError(
                    'You must enter a number for all of the shooting numbers',
                    self.__dict__().copy().update(values)
                    )
        if values['did_climb']:
            try:
                values['climb_start'] = int(values['climb_start'])
                values['climb_finish'] = int(values['climb_finish'])
                values['level_reached'] = int(values['level_reached'])
                values['frisbees_dumped'] = int(values['frisbees_dumped'])
            except ValueError:
                raise ValidationError(
                    'All climbing related numbers must be numbers',
                    self.__dict__().copy().update(values)
                    )
        if values['did_ground_load']:
            try:
                values['auto_frisbees_ground_loaded'] = int(
                    values['auto_frisbees_ground_loaded'])
            except ValueError:
                raise ValidationError(
                    'All numbers of frisbees ground loaded must be numbers',
                    self.__dict__().copy().update(values)
                    )
        return values

    def set(self, values):
        """Set the robot_match's values.

        Sets the values of the robot_match to values.

        Args:
            values: A dictionary of values returned by RobotMatch.validate().
                These values should have already been validated.
        """
        self.is_scouted = values['is_scouted']
        self.robot_match_comments = values['robot_match_comments']
        self.did_foul = values['did_foul']
        self.did_technical_foul = values['did_technical_foul']
        self.foul_description = values['foul_description']
        self.did_shoot = values['did_shoot']
        if self.did_shoot:
            self.auto_1 = values['auto_1']
            self.auto_2 = values['auto_2']
            self.auto_3 = values['auto_3']
            self.auto_miss = values['auto_miss']
            self.teleop_1 = values['teleop_1']
            self.teleop_2 = values['teleop_2']
            self.teleop_3 = values['teleop_3']
            self.teleop_5 = values['teleop_5']
            self.teleop_miss = values['teleop_miss']
            self.shooting_description = values['shooting_description']
        self.did_climb = values['did_climb']
        if self.did_climb:
            self.climb_start = values['climb_start']
            self.climb_finish = values['climb_finish']
            self.level_reached = values['level_reached']
            self.frisbees_dumped = values['frisbees_dumped']
            self.did_fall_off_pyramid = values['did_fall_off_pyramid']
            self.climbing_description = values['climbing_description']
        self.did_human_load = values['did_human_load']
        self.did_ground_load = values['did_ground_load']
        if self.did_ground_load:
            self.auto_frisbees_ground_loaded =\
                values['auto_frisbees_ground_loaded']
        if self.did_human_load or self.did_ground_load:
            self.loading_description = values['loading_description']
