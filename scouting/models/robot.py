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

class Robot(Base):
    """The data gathered for a specific robot during pit scouting.

    Attributes:
        robot_number: The number of the robot.  This is used is the primary key.
        is_scouted: Whether the robot has been scouted yet.
        scout: The name of the scout who pit scouted the robot.  This is not
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
    is_scouted = Column(Boolean)

    description = Column(UnicodeText)

    wheels = Column(UnicodeText)
    gearbox = Column(UnicodeText)
    motors = Column(UnicodeText)

    can_shoot = Column(Boolean)
    can_climb = Column(Boolean)
    can_human_load = Column(Boolean)
    can_ground_load = Column(Boolean)


    def __init__(self, robot_number):
        """Initialise the robot.

        Initialises the robot with its number and is_scouted as false.

        Args:
            number: The robot's number.
        """
        self.robot_number = robot_number
        self.is_scouted = False

    def validate(self, request):
        """Validate a request.

        Validates the data in the request and returns the validated data.

        Args:
            request: A request which contains the results of a form into which
                robot data was entered as POST data.

        Returns:
            A dictionary of the validated values.

        Raises:
            ValidationError: The form data in request doesn't validate.
        """
        values = {
            'description':request.POST['description'],
        	'wheels':request.POST['wheels'],
        	'gearbox':request.POST['gearbox'],
        	'motors':request.POST['motors'],
        	'can_shoot':'can_shoot' in request.POST,
        	'can_climb':'can_climb' in request.POST,
        	'can_human_load':'can_human_load' in request.POST,
        	'can_ground_load':'can_ground_load' in request.POST,
        	}
        return values

    def set(self, values):
        """Set the robots values.

        Sets the values of the robot to values.

        Args:
            values: A dictionary of values returned by Robot.validate().  These
                values should have already been validated.
        """
        self.description = values['description']
        self.wheels = values['wheels']
        self.gearbox = values['gearbox']
        self.motors = values['motors']
        self.can_shoot = values['can_shoot']
        self.can_climb = values['can_climb']
        self.can_human_load = values['can_human_load']
        self.can_ground_load = values['can_ground_load']
