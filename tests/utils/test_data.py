# NOTE: These are some test cases, more thoughts may be needed
#       choosing test cases to cover different scenarios

# Straight line
case_1 = {
    "input": {
        "start": {"x": 0, "y": 0},
        "commands": [
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
        ],
    },
    "expected": {
        "result": 9,
        "commands": 8,
    },
}

# L shape
case_2 = {
    "input": {
        "start": {"x": 0, "y": 0},
        "commands": [
            {"direction": "east", "steps": 1},
            {"direction": "north", "steps": 1},
            {"direction": "south", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "north", "steps": 1},
            {"direction": "south", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "north", "steps": 1},
            {"direction": "south", "steps": 1},
            {"direction": "west", "steps": 1},
        ],
    },
    "expected": {
        "result": 3,
        "commands": 12,
    },
}

# Straight line, then back
case_3 = {
    "input": {
        "start": {"x": 0, "y": 0},
        "commands": [
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "west", "steps": 1},
        ],
    },
    "expected": {
        "result": 5,
        "commands": 8,
    },
}

# No commands
case_4 = {
    "input": {"start": {"x": 0, "y": 0}, "commands": []},
    "expected": {
        "result": 1,
        "commands": 0,
    },
}

# One command
case_5 = {
    "input": {
        "start": {"x": 0, "y": 0},
        "commands": [
            {"direction": "east", "steps": 1},
        ],
    },
    "expected": {
        "result": 2,
        "commands": 1,
    },
}

# Start somewhere else
case_6 = {
    "input": {
        "start": {"x": 13, "y": 37},
        "commands": [
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
        ],
    },
    "expected": {
        "result": 5,
        "commands": 4,
    },
}

# Start on negative coordinates
case_7 = {
    "input": {
        "start": {"x": -4, "y": 0},
        "commands": [
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "east", "steps": 1},
        ],
    },
    "expected": {
        "result": 5,
        "commands": 4,
    },
}

# Circle
case_8 = {
    "input": {
        "start": {"x": 0, "y": 0},
        "commands": [
            {"direction": "east", "steps": 1},
            {"direction": "north", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "south", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "north", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "south", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "north", "steps": 1},
            {"direction": "west", "steps": 1},
            {"direction": "south", "steps": 1},
        ],
    },
    "expected": {
        "result": 4,
        "commands": 12,
    },
}
test_data = [case_1, case_2, case_3, case_4, case_5, case_6, case_7, case_8]
