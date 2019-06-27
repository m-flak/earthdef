import earthdef
import random

# you could also say columns, but i like lanes
def create_lanes(lane_width):
    screen_width = earthdef.DISPLAY_MODE[0]
    num_lanes = screen_width // lane_width
    lanes = []
    cur_x = 0

    for i in range(0, num_lanes):
        lanes.insert(i, cur_x)
        cur_x += lane_width

    return lanes

# pick a random "lane" of width at offset Y
# returns a tuple of X, Y
def random_lane(lane_width, y=0):
    return random.choice(create_lanes(lane_width)), y
