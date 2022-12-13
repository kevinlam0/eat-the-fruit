#Kevin Lam, mvk2uy

import uvage
import random
camera = uvage.Camera(600, 600)

# ---- Gamebox for player ----
box = uvage.from_color(300,300, "orange", 20, 20)

# ---- Movement ----
right_direction = False
left_direction = False
down_direction = False
up_direction = False

# ---- Walls ----
left_wall = uvage.from_color(0, 0, "forest green", 20, 2000)
right_wall = uvage.from_color(600, 0, "forest green", 20, 2000)
top_wall = uvage.from_color(0, 0, "forest green", 2000, 20)
bottom_wall = uvage.from_color(600, 600, "forest green", 2000, 20)
list_of_wall = []

# ---- Collectibles ----
sheet = uvage.load_sprite_sheet("fruit_and_veggies.png", 4, 8)
token = [uvage.from_image(450, 350, sheet[random.randint(0,31)] )]
for each in token:
    each.scale_by(.5)

# ---- Background ----
background = uvage.from_image(300, 300, "snake_game_background.png")
background.scale_by(2.2)

# ---- Game Settings ----
levels_finished = 0
game_over = False
game_on1 = False
game_on2 = False
game_on1done = False
game_on2start = True
level1_finished = False
level2_finished = False
level3_finished = False
level4_finished = False
level5_finished = False
game_over = False
score = 0
goal = 5
level =1

# ---- Makes walls ----
def walls(level):
    """
    makes walls according to the level
    does this in levels 3-6
    :return: list of the walls
    """
    global list_of_wall
    base_number = level * 50 # width of 2 walls
    width = base_number//2 # width of one side of the wall
    distance_1 = width//2 # distance away from 0 for the coordinate
    distance_2 = 600-distance_1 # distance away from 600 for the coordinate
    list_of_wall = [] # makes empty list every time
    list_of_wall.append(uvage.from_color(distance_1, 300, "forest green", width, 600))  # left
    list_of_wall.append(uvage.from_color(distance_2, 300, "forest green", width, 600))  # right
    list_of_wall.append(uvage.from_color(300, distance_1, "forest green", 600, width))  # top
    list_of_wall.append(uvage.from_color(300, distance_2, "forest green", 600, width))  # bottom

# ---- Movement of Box ----
def move1(o):
    """
    uses this to move the box continuously until you choose another direction
    :param o: speed of the box
    :return: moving
    """
    global box
    global right_direction
    global left_direction
    global down_direction
    global up_direction
    if right_direction == False and left_direction == False and up_direction == False and not uvage.is_pressing("down arrow"): #initial movement
        down_direction = True
        box.y += o
        right_direction = False
        left_direction = False
        up_direction = False
    if uvage.is_pressing("up arrow")  or right_direction == False and left_direction == False and down_direction == False:
        up_direction = True
        box.y -= o
        right_direction = False
        left_direction = False
        down_direction = False
    if uvage.is_pressing("down arrow"):
        down_direction = True
        box.y += o
        right_direction = False
        left_direction = False
        up_direction = False
    if uvage.is_pressing("left arrow") or left_direction == True and right_direction == False and up_direction == False and down_direction== False  :
        left_direction = True
        box.x -= o
        right_direction = False
        down_direction = False
        up_direction = False
    if uvage.is_pressing("right arrow") or right_direction == True and left_direction == False and up_direction == False and down_direction == False:
        right_direction = True
        box.x += o
        left_direction = False
        down_direction = False
        up_direction = False

# ---- Collectibles ----
def collectible(x,y):
    """
    makes the fruits to touch
    :param x: bounds x-coordinate
    :param y: bounds y-coordinate
    :return: a list of a single token
    """
    global token
    global score
    for each in token: # everything within the list
        if box.touches(each): # if the box touches the token
            token = [] # resets the list to nothing
            score += 1
            while token == []: # keep running until something is within the list
                rando1 = random.randint(x, y) # picks an x coordinate within the max dimensions
                rando2 = random.randint(x, y) # picks a y coordinate within the max dimensions
                if rando1 % 5 == 0 and rando2 % 5 == 0: # both needs to be divisible by 5
                    each = uvage.from_image(rando1, rando2, sheet[random.randint(0, 31)]) # makes an item in list as a gamebox of the collectible
                    each.scale_by(.5) # makes the token smaller
                    token.append(each) # adds to the list

def tick():
    """
    runs the game
    :return:
    """
    global lista
    global game_on1, game_on2, game_on1done
    global game_over
    global level1_finished,level2_finished,level3_finished, level4_finished, level5_finished
    global score
    global box
    global list_of_wall
    global game_on2start
    global token, level
    global game_on2done
    global spawned
    global goal

    # ---- Background ----
    camera.clear("light green")
    camera.draw(background)

    # ---- Starting the Game ----
    if uvage.is_pressing("space") and game_over == False:
        game_on1 = True

    # ---- To Restart ----
    if uvage.is_pressing("r") and game_over == True:
        game_over = False
        game_on1 = False
        game_on2 = False
        game_on1done = False
        game_on2start = True
        game_over = False
        level1_finished = False
        level2_finished = False
        level3_finished = False
        level4_finished = False
        level5_finished = False
        score = 0
        level = 1
        box = uvage.from_color(400, 300, "orange", 20, 20)

    # ---- Display Start ----
    if game_on1 == False and game_on1done == False and game_on2 == False:
        camera.draw(uvage.from_text(300, 200, "Press 'Space' to start", 50, "white", bold=True))
        camera.draw(uvage.from_text(300, 250, "Collect " + str(goal)+ " tokens to go to next level", 40, "white", bold=True))

    # ---- Draws First Token ----
    for each in token:
        camera.draw(each)

    # ---- Starting First Part of Game ----
    if game_on1 == True:
        camera.draw(box)

        # ---- Levels ----
        if level == 1:
            move1(5) # 5 speed for the box
            camera.draw(uvage.from_text(300, 35, "Level 1", 50, "white", bold=True)) # Displaying the level
            camera.draw(right_wall)
            camera.draw(left_wall)
            camera.draw(top_wall)
            camera.draw(bottom_wall)
            collectible(30, 550) # Min and max of the dimension of where token can spawn
            if score == goal: # When score reaches the goal, change the level
                score = 0 # Resets the score
                level += .5 # To go in between levels for displaying press " " to start next level
                level1_finished = True

        # ---- Display Next Level Texts ----
        if level == 1.5:
            camera.draw(uvage.from_text(300, 200, "Press '" + str(int(level+.5)) + "' to continue to Level " + str(int(level+.5)), 40, "white", bold=True))

        # ---- Start Next Level ----
        if uvage.is_pressing("2") and game_on1done == False and game_over == False and level1_finished == True:
            level = 2

        elif level ==2:
            move1(8)
            camera.draw(uvage.from_text(300, 35, "Level 2", 50, "white", bold=True))
            camera.draw(right_wall)
            camera.draw(left_wall)
            camera.draw(top_wall)
            camera.draw(bottom_wall)
            collectible(30, 550)
            if score == goal: # When score reaches goal it moves onto next level
                score = 0
                level += .5
                level2_finished = True
                game_on1 = False
                game_on1done = True
        if box.touches(left_wall) or box.touches(right_wall) or box.touches(top_wall) or box.touches(bottom_wall) and game_on1done == False: # if the box touches any of the boxes, player loses
            game_on1 = False
            game_on2 = False
            game_over = True
            game_on1done = True

        if level == 2.5: # Spawns box in the middle, so it does not hit the walls before game starts
            box.x = 300
            box.y = 300
            camera.draw(box)

    # ---- Put Text for Starting Next Game ----
    if game_on1done == True and game_on2 == False and game_over == False: #before the game 2 starts, displays texts about next level and window will be smaller
        camera.draw(uvage.from_text(300, 200, "Press '" + str(int(level + .5)) + "' to continue to Level " + str(int(level + .5)), 40, "white", bold=True))
        camera.draw(uvage.from_text(300, 230, "The window will now be smaller", 40, "white", bold=True))

    if uvage.is_pressing("3") and game_on1done == True and game_over == False :
        game_on2 = True
        level = 3

        camera.clear("light green")
        camera.draw(background)

    # ---- Start of Part 2 of Game ----
    elif game_on2 == True:
        camera.draw(box)

        if game_on2start == True: # Initially spawns it within the window
            token = [uvage.from_image(450, 350, sheet[random.randint(0, 31)])]
            for each in token:
                each.scale_by(.5)
            game_on2start = False

        # ---- Levels ----
        if level == 3:
            move1(8)
            walls(level)
            for each in list_of_wall: # Draws each wall, which are in a list
                camera.draw(each)
            collectible(120, 480) # Min and max dimensions where the collectible can spawn
            camera.draw(uvage.from_text(300, 35, "Level 3", 50, "white", bold=True)) # Displaying the level
            if score == goal:
                score = 0
                level += .5
                level3_finished = True
            for each in list_of_wall: # For each wall in the list, if it touches any, it will end the game
                if box.touches(each):
                    game_on2 = False
                    game_over = True

        elif level == 3.5:
            camera.draw(uvage.from_text(300, 200, "Press '" + str(int(level+.5)) + "' to continue to Level " + str(int(level+.5)), 40, "white", bold=True))
            box.x = 300
            box.y = 300

            if uvage.is_pressing("4") and game_on1done == True and game_over == False and level1_finished == True and level3_finished == True:
                level = 4

        elif level == 4:
            move1(8)
            walls(level)
            for each in list_of_wall:
                camera.draw(each)
            collectible(170, 430)
    #
            camera.draw(uvage.from_text(300, 35, "Level 4", 50, "white", bold=True))
            for each in list_of_wall:
                if box.touches(each):
                    game_on2 = False
                    game_over = True
            if score == goal:
                score = 0
                level += .5
                level4_finished = True

        elif level == 4.5:
            camera.draw(uvage.from_text(300, 200, "Press '" + str(int(level+.5)) + "' to continue to Level " + str(int(level+.5)), 40, "white", bold=True))
            box.x = 300
            box.y = 300

            if uvage.is_pressing("5") and game_on1done == True and game_over == False and level1_finished == True and level3_finished == True:
                level = 5

        elif level == 5:
            move1(8)
            walls(level)
            for each in list_of_wall:
                camera.draw(each)
            collectible(195, 405)
            camera.draw(uvage.from_text(300, 35, "Level 5", 50, "white", bold=True))

            if score == goal:
                score = 0
                level += .5
                level5_finished = True
            for each in list_of_wall:
                if box.touches(each):
                    game_on2 = False
                    game_over = True

        elif level == 5.5:
            camera.draw(uvage.from_text(300, 200, "Press '" + str(int(level + .5)) + "' to continue to Level " + str(int(level + .5)), 40, "white", bold=True))
            box.x = 300
            box.y = 300

            if uvage.is_pressing("6") and game_on1done == True and game_over == False and level1_finished == True and level3_finished == True:
                level = 6

        elif level == 6:
            move1(8)
            walls(level)
            for each in list_of_wall:
                camera.draw(each)
            collectible(220, 380)
            camera.draw(uvage.from_text(300, 35, "Level 6", 50, "white", bold=True))
            for each in list_of_wall:
                if box.touches(each):
                    game_on2 = False
                    game_over = True

    elif game_over == True: # Displays "GAME OVER" when person dies and turns off the games 
        camera.draw(uvage.from_text(300, 200, "GAME OVER", 40, "Red", bold=True))
        game_on1 = False
        game_on2 = False
        camera.draw(uvage.from_text(300, 230, "Press 'R' to Restart", 40, "Red", bold=True))
    camera.draw(uvage.from_text(580, 580, str(score), 50, "orange", bold = True))

    camera.display()
uvage.timer_loop(30,tick)