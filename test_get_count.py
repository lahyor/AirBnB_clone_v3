#!/usr/bin/python3
"""
Testing .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

#print(storage.all("State"))
first_state_id = list(storage.all(State).values())[1].id
#print(first_state_id)
print("First state: {}".format(storage.get(State, first_state_id)))
