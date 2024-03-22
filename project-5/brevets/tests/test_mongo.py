"""
Nose tests for mongo_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging
#from flask_brevets import fetch_items, insert_items
from mongo import fetch_items, insert_items

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

# RUN TEST FILE BY BEING IN BREVETS DIRECTORY AND USING CMD: nosetests tests/test_acp_times.py
# bash run_tests.sh or go to terminal on docker desktop


items = [{"km": 50, 
        "open": "2021-01-01T01:28", 
        "close": "2021-01-01T03:30"
        }, 
        {"km": 200, 
        "open": "2021-01-01T05:53", 
        "close": "2021-01-01T13:30"
        }, 
        {"km": 240, 
        "open": "2021-01-01T05:53", 
        "close": "2021-01-01T13:30"
}]
distance = '200'
start_time = "2021-01-01T00:00"

def test1_insert():
    # Tests to make sure that insert_items returns a string

    # Checks to see if the inserted items return a string
    id = insert_items(distance, start_time, items)
    assert isinstance(id, str)


def test2_fetch():
    # Test fetch_items function

    # Checks to see if items have been inserted correctly by fetching them
    fetched = fetch_items()
    print(fetched)
    assert fetched[0] == distance
    assert fetched[1] == start_time
    assert fetched[2][0] == items[0]
    assert fetched[2][1] == items[1]
    assert fetched[2][2] == items[2]
    
    """('200', 
    '2021-01-01T00:00', 
    [{'km': 50, 'open': '2021-01-01T01:28', 'close': '2021-01-01T03:30'},
    {'km': 200, 'open': '2021-01-01T05:53', 'close': '2021-01-01T13:30'},
    {'km': 240, 'open': '2021-01-01T05:53', 'close': '2021-01-01T13:30'}])
    """
    


    


    







