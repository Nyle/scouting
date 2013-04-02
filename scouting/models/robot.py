from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Text,
    UnicodeText,
    Boolean,
    )

from models.base import Base

class Robot(Base):
    """The data gathered for a specific robot during pit scouting.

    Attributes:
        robot_number: The number of the robot.  This is used is the primary key.
        is_scouted: Whether the robot has been scouted yet.
        scout: The name of the scout who pit scouted the robot. This is not
            currently implemented since users have yet to be implemented.

        description: A general description of the robot and its abilities.

        wheels: A description of the robot's wheels.
        gearbox: A description of the robot's gearbox.
        motors: A description of the robot's motors.

        can_shoot: Whether the robot is able to shoot or dump frisbees.
        can_climb: Whether the robot is able to climb the pyramid.
        can_human_load: Whether the robot is able to human load frisbees.
        can_ground_load: Whether the robot is able to ground load frisbees.

    """
    __tablename__ = 'robots'
    robot_number = Column(Integer, primary_key=True)
    # TODO: Add this in when users, permissions, etc. is added in.
#     scout = Column(Text, ForeignKey('users.name'), default=None)
    is_scouted = Column(Boolean, default=False)

    description = Column(UnicodeText, default=u'')

    wheels = Column(UnicodeText, default=u'')
    gearbox = Column(UnicodeText, default=u'')
    motors = Column(UnicodeText, default=u'')

    can_shoot = Column(Boolean)
    can_climb = Column(Boolean)
    can_human_load = Column(Boolean)
    can_ground_load = Column(Boolean)


    def __init__(self, robot_number):
        """Initialise the robot.

        Initialises the robot with its number.  Only the number is used because
        all other information will be entered during pit scouting, after all the
        robots have been initialised from the team list during the database
        initialisation.

        Args:
            number: The robot's number.
        """
        self.robot_number = robot_number
