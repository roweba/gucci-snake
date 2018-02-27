# Feb. 12th 2018

import bottle
import os
import random
import heapq

# see todo.txt for full explanation of the following constants:
MY_HEAD = 0
EMPTY = 1
MY_TAIL = 2
FOOD = 8
SNAKE_BODY = -1
HALO = -2
BLOCKED = -3


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.jpg' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#0000FF',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'gucci snake'
    }

"""
no parameters passed, but uses the POST request containing all the current game information
each time, creates a 2D int array (same size as the board), initializes the grid with the EMPTY constant
*important top left is (0,0)
returns a list: game board (2D int array) and a list of size 2, x then y, the location of our snake's head
"""
def make_grid(data):
	# create and initialize grid
	grid = [[0 for x in range(data['width'])] for y in range(data['height'])]
	for i in range (len(grid)):
		for j in range (len(grid[i])):
			grid_value = set_grid(i,j)
            grid[i][j] = grid_value
	# create a variable for the snake head
	# note: we are unsure about the syntax for getting the head info
	head = [data['body'][0]['x'] , data['body'][0]['y']]
	# head = [data['body'][0].x , data['body'][0].y]

	return grid, head



def set_grid(i,j):
	"""Gives a single cell of the 2D int array from make_grid

	Input: two integers, i and j, that re
	modifies a grid's content to reflect the current game board status, following the decided constant names/values
	"""

    #initialize point from i,j coordinates
    #make if statements to check what is on the point
    #return value of the grid space

#finds the closest bit of food to us just by looking at position on the board,
#does not actually find which peice of food takes the least amount of moves
#to get to, maybe think about implimenting that later?
#head is a list of (x,y) for our current position, grid is the play grid
def findFood(head, grid):

    closest = [0, 0] #does not matter just needs to be a list with two things in it
    distance = 1000000000000 #big number so that the first food found will be less

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (grid[i][j] == 8):
                curDist = h(head, [i, j])
                if (curDist < distance):
                    closest = [i, j]
                    distance = curDist
    return closest


#how far we are from a given destination
def h(cur, dest):
	return abs(cur[0] - dest[0]) + abs(cur[1] - dest[1])

#find which direction we want to go to get to the given destination
def aStar(board, head, dest):
	open = [] #things to check
	close = [] #things that have been checked
	out = '' #the direction to go
	succ = [] #the list of successors

	heapq.heappush(open, (h(head, dest), head, 0))#push where we are to start off
	while(open):#while we have things to check
		cur = heappop(open)#pop the best thing from the priority queue

		#set our direction, Joss has a feeling this will need debugging, talk to Joss about it
		if (cur[1][0] == head[0]+1 and cur[1][1] == head[1]):
			out = 'right'
		elif (cur[1][0] == head[0]-1 and cur[1][1] == head[1]):
			out = 'left'
		elif (cur[1][0] == head[0] and cur[1][1] == head[1]+1):
			out = 'down'
		elif (cur[1][0] == head[0] and cur[1][1] == head[1]-1):
			out = 'up'

		#if we find our destination return our initial direction
		if (cur[1] == dest):
			return out

		#add safe tiles around the current tile to the list of successors
		if (board[cur[1][0]+1][cur[1][1]] > 0):
			succ.append([cur[1][0]+1, cur[1][1])
		if (board[cur[1][0]-1][cur[1][1]] > 0):
			succ.append([cur[1][0]-1, cur[1][1])
		if (board[cur[1][0]][cur[1][1]+1] > 0):
			succ.append([cur[1][0], cur[1][1]+1)
		if (board[cur[1][0]][cur[1][1]-1] > 0):
			succ.append([cur[1][0], cur[1][1]-1)

		for thinkofabettervariablename in succ:
			pass
		#line 8 of nikita's psudocode

@bottle.post('/move')
def move():
    data = bottle.request.json
    make_grid(data)
    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']

    return {
        #'move': random.choice(directions),
        'move': 'up',
		'taunt': 'ESKETITT'
    }


def make_grid(data):
	"""Creates a 2D int array, initializes each cell with the EMPTY constant, calls set_grid(), and returns the position of our snake's head

	Input: none, uses data from POST request
	Output: 2D int array representing the game board and a list of size 2, x then y, the location of our snake's head


	"""
	# create and initialize grid
	grid = [[0 for x in range(data['width'])] for y in range(data['height'])]
	for i in range (len(grid)):
		for j in range (len(grid[i])):
			grid_value = set_grid(i,j)
            grid[i][j] = grid_value
	# create a variable for the snake head
	# note: we are unsure about the syntax for getting the head info
	head = [data['body'][0]['x'] , data['body'][0]['y']]
	# head = [data['body'][0].x , data['body'][0].y]

	return grid, head



def set_grid(i,j):
	"""Modifies a grid's content to reflect the current game board status, following the decided constant names/values


	Input: two integers, i and j
	Output: an integer
	"""

    #initialize point from i,j coordinates
    #make if statements to check what is on the point
    #return value of the grid space



@bottle.post('/move')
def move():
    data = bottle.request.json
    make_grid(data)
    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']

    return {
        #'move': random.choice(directions),
        'move': 'up',
		'taunt': 'battlesnake-python!'
    }

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
