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


# Feb. 12th 2018

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

def h(cur, dest):
	return abs(cur[0] - dest[0]) + abs(cur[1] - dest[1])
	
def aStar(board, head, dest):
	open = []
	close = []
	out = ''
	succ = []
	
	heapq.heappush(open, (h(head, dest), head, 0))
	while(open):
		cur = heappop(open)
		if (cur[1][0] == head[0]+1 and cur[1][1] == head[1]):
			out = 'right'
		elif (cur[1][0] == head[0]-1 and cur[1][1] == head[1]):
			out = 'left'
		elif (cur[1][0] == head[0] and cur[1][1] == head[1]+1):
			out = 'down'
		elif (cur[1][0] == head[0] and cur[1][1] == head[1]-1):
			out = 'up'
			
		if (cur[1] == dest):
			return out

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

    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']

    return {
        #'move': random.choice(directions),
        'move': 'up',
		'taunt': 'battlesnake-python!'
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


"""
modifies a grid's content to reflect the current game board status, following the decided constant names/values
"""

def set_grid(i,j):
    #initialize point from i,j coordinates
    #make if statements to check what is on the point
    #return value of the grid space

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
