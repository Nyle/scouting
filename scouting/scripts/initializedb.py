import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    Robot,
    Match,
    RobotMatch,
    )

from random import (
    randint,
    sample,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
#         robot_numbers = [int(i) for i in teams.strip().split('\n')]
#         robots = [Robot(robot_number=i) for i in robot_numbers]
#         for robot in robots:
#             DBSession.add(robot)
        robot_numbers = set([randint(1, 5000) for i in range(100)])
        for robot_number in robot_numbers:
            DBSession.add(Robot(robot_number=robot_number))
        for match_number in range(140):
            robots = sample(robot_numbers, 6)
            DBSession.add(Match(match_number=match_number,
                                r_1=robots[0], r_2=robots[1], r_3=robots[2],
                                b_1=robots[3], b_2=robots[4], b_3=robots[5],
                                ))



teams = """
27
45
70
95
111
118
125
151
192
222
245
295
329
337
358
384
422
447
467
578
610
744
842
1086
1114
1218
1241
1323
1325
1378
1405
1425
1429
1477
1629
1675
1710
1726
1732
1772
1801
1806
1912
1987
2000
2046
2169
2175
2199
2259
2337
2338
2341
2403
2474
2481
2485
2502
2512
2630
2648
2729
2809
2834
2907
2978
3018
3132
3189
3211
3284
3459
3481
3528
3641
3656
3941
3944
4011
4026
4039
4069
4158
4334
4452
4462
4472
4481
4492
4502
4522
4541
4557
4579
4601
4607
4627
4641
4797
"""
