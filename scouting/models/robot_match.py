from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    UnicodeText,
    Boolean,
    )

from models.base import Base

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
        frisbees_sucessfully_human_loaded: How many frisbees the robot was able
            to human load.
        frisbees_unsuscessfully_human_loaded: How many frisbees the robot failed
            to human load.

        did_ground_load: Whether the robot ground loaded in the match.
        auto_frisbees_ground_loaded: How many frisbees the robot ground loaded
            in auto.
        teleop_frisbees_ground_loaded: How many frisbees the robot ground loaded
            in teleop.

        loading_description: A description of the robots loading: what it was
            good at, what it wasn't good at, strategy suggestions, etc.

    """
    __tablename__ = 'robot_matches'
    id = Column(Integer, primary_key=True)
    match_number = Column(Integer)
    robot_number = Column(Integer)

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
    climbing_description = Column(Text)

    did_human_load = Column(Boolean)
    frisbees_sucessfully_human_loaded = Column(Integer)
    frisbees_unsuscessfully_human_loaded = Column(Integer)

    did_ground_load = Column(Boolean)
    auto_frisbees_ground_loaded = Column(Integer)
    teleop_frisbees_ground_loaded = Column(Integer)

    loading_description = Column(UnicodeText)

    def __init__(self, match_number, robot_number):
        """Initialise the robot_match.

        Initialises the robot_match with its robot and match numbers.

        Args:
            match_number: The match number.
            robot_number: The robot number.
        """
        self.match_number = match_number
        self.robot_number = robot_number
