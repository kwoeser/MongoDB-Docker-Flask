"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import arrow
import nose    # Testing framework
import logging
from acp_times import open_time, close_time

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


time = '2021-01-01T12:00'
start_time = arrow.get(time)

# RUN TEST FILE BY BEING IN BREVETS DIRECTORY AND USING CMD: nosetests tests/test_acp_times.py
def test1_distance_zero():
    """Test case when control distance km is 0"""
    assert open_time(0, 200, start_time) == start_time
    assert close_time(0, 200, start_time) == start_time.shift(minutes=60)


def test2_two_hundred_open():
    """OPEN TIME -> Test case for when brevet_dist_km is 200 and there is a distance >= 200"""
    assert open_time(200, 200, start_time) == start_time.shift(minutes=353)
    assert open_time(240, 200, start_time) == start_time.shift(minutes=353)

def test2_two_hundred_close():
    """CLOSE TIME -> Test case for when brevet_dist_km is 200 and there is a distance >= 200"""
    # print(close_time(200, 200, start_time))
    assert close_time(200, 200, start_time) == start_time.shift(minutes=810)
    assert close_time(240, 200, start_time) == start_time.shift(minutes=810)



def test3_four_hundred_open():
    """OPEN TIME -> Test case for when brevet_dist_km is 400 and there is a distance >= 400"""
    assert open_time(400, 400, start_time) == start_time.shift(minutes=728)
    assert open_time(420, 400, start_time) == start_time.shift(minutes=728)
    
def test3_four_hundred_close():
    """CLOSE TIME -> Test case for when brevet_dist_km is 400 and there is a distance >= 400"""
    assert close_time(400, 400, start_time) == start_time.shift(minutes=1620)
    assert close_time(420, 400, start_time) == start_time.shift(minutes=1620)


def test_open_times():
    """Test case for random open times"""
    assert open_time(60, 200, start_time) == start_time.shift(minutes = 106)
    assert open_time(250, 600, start_time) == start_time.shift(minutes = 447)
    assert open_time(500, 1000, start_time) == start_time.shift(minutes = 928)

def test_close_times():
    """Test case for random close times"""

    assert close_time(50, 200, start_time) == start_time.shift(minutes=210)
    assert close_time(600, 600, start_time) == start_time.shift(minutes=2400)
    assert close_time(100, 1000, start_time) == start_time.shift(minutes=400)








