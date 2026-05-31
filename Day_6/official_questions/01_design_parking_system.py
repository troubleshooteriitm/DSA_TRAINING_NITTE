"""
LeetCode 1603 -- Design Parking System
=======================================
Design a parking system for a parking lot with three kinds of parking spaces:
big, medium, and small, with a fixed number of slots for each size.

Implement the ParkingSystem class:
- ParkingSystem(big, medium, small): Initializes slots.
- addCar(carType) -> bool: 1=big, 2=medium, 3=small.
  Returns true if there is a parking space available.

Example:
    ps = ParkingSystem(1, 1, 0)
    ps.addCar(1) -> True
    ps.addCar(2) -> True
    ps.addCar(3) -> False
    ps.addCar(1) -> False
"""


class ParkingSystem:
    def __init__(self, big, medium, small):
        self.slots = {1: big, 2: medium, 3: small}

    def addCar(self, carType):
        if self.slots[carType] > 0:
            self.slots[carType] -= 1
            return True
        return False

    def __str__(self):
        return (f"ParkingSystem(big={self.slots[1]}, "
                f"medium={self.slots[2]}, small={self.slots[3]})")


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    ps = ParkingSystem(1, 1, 0)
    assert ps.addCar(1) == True    # big slot available
    assert ps.addCar(2) == True    # medium slot available
    assert ps.addCar(3) == False   # no small slots
    assert ps.addCar(1) == False   # big slot full

    ps2 = ParkingSystem(3, 3, 3)
    assert ps2.addCar(1) == True
    assert ps2.addCar(1) == True
    assert ps2.addCar(1) == True
    assert ps2.addCar(1) == False

    ps3 = ParkingSystem(0, 0, 0)
    assert ps3.addCar(1) == False
    assert ps3.addCar(2) == False
    assert ps3.addCar(3) == False

    print("All test cases passed")
