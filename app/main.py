# Feb. 12th 2018

import bottle
import os
import random
import heapq
import copy

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
			grid_value = set_grid(i,j,data)
			grid[i][j] = grid_value

	head = [data['you']['body']['data']['x'][0], data['you']['body']['data']['y'][0]]

	return grid, head



def set_grid(i,j,data):

    snake_list = data['snakes']['data']
    food_list = data['food']['data']

    for snake in range(0, len(snake_list)):
        x = snake_list['body']['data'][snake]['x']
        y = snake_list['body']['data'][snake]['y']
        if x == i and y == j:
            return -1
    for food in range(0, len(food_list)):
        x = food_list[food]['x']
        y = food_list[food]['y']
        if x == i and y == j:
            return 8
    return 1
    #initialize point from i,j coordinates
    #make if statements to check what is on the point
    #return value of the grid space

#finds the closest bit of food to us just by looking at position on the board,
#does not actually find which peice of food takes the least amount of moves
#to get to, maybe think about implimenting that later?
#head is a list of (x,y) for our current position, grid is the play grid
def findFood(grid, head):

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

#a function to mark all tiles that are unreachable
#Joss is working on this when procrastinating jk I think its done
def findBlocked(grid, head):
	checked = copy.deepcopy(grid)
	open = []
	open.append(head)

	while(open):

		cur = open.pop() #using 1 r for you nikita
		checked[cur[0]][cur[1]] = 9

		#right
		if (cur[0]+1 < len(grid)):
			if (checked[cur[0]+1][cur[1]] > 0):
				if (checked[cur[0]+1][cur[1]] != 9):
					open.append([cur[0]+1, cur[1]])
		#left
		if (cur[0]-1 >= 0):
			if (checked[cur[0]-1][cur[1]] > 0):
				if (checked[cur[0]-1][cur[1]] != 9):
					open.append([cur[0]-1, cur[1]])
		#down
		if (cur[1]+1 < len(grid[0])):
			if (checked[cur[0]][cur[1]+1] > 0):
				if (checked[cur[0]][cur[1]+1] != 9):
					open.append([cur[0], cur[1]+1])
		#up
		if (cur[1]-1 >= 0):
			if (checked[cur[0]][cur[1]-1] > 0):
				if (checked[cur[0]][cur[1]-1] != 9):
					open.append([cur[0], cur[1]-1])

	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if (grid[i][j] > 0):
				if (checked[i][j] != 9):
					grid[i][j] = -3

#how far we are from a given destination
def h(cur, dest):
	return abs(cur[0] - dest[0]) + abs(cur[1] - dest[1])



#find which direction we want to go to get to the given destination
#http://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
def aStar(board, head, dest):
	openn = [] #things to check
	close = [] #things that have been checked
	out = '' #the direction to go
	succ = [] #the list of successors
	cur = None

	#node dictionary format:
	#"xy": a tuple in the form (x, y) signifying the position of the node
	#"estCost": the estimated cost to get to dest from here [h]
	#"curCost": the cost taken to reach this node [g]
	#"parent": the previous node in the path

	headNode = {"xy": head, "estCost": h(head, dest), "curCost": 0, "parent": None}
	heapq.heappush(openn, (headNode["estCost"] + headNode["curCost"], headNode))#push where we are to start off
	while(openn):#while we have things to check
		cur = heappop(openn)[1]#pop the best thing from the priority queue

		#if we find our destination return our initial direction
		if (cur['xy'] == dest):
			break

		#add safe tiles around the current tile to the list of successors
		#TODO: board edges
		if (board[cur['xy'][0]+1][cur['xy'][1]] > 0):
			succ.append(cur['xy'][0]+1, cur['xy'][1])
		if (board[cur['xy'][0]-1][cur['xy'][1]] > 0):
			succ.append(cur['xy'][0]-1, cur['xy'][1])
		if (board[cur['xy'][0]][cur['xy'][1]+1] > 0):
			succ.append(cur['xy'][0], cur['xy'][1]+1)
		if (board[cur['xy'][0]][cur['xy'][1]-1] > 0):
			succ.append(cur['xy'][0], cur['xy'][1]-1)

		for node in succ:
			succCost = 1 + cur["curCost"]
			if(node in openn[:][1]['xy']): #FIXME this might be broken
				index = openn[:][1]['xy'].index(node)
				if(openn[index][1]['curCost'] <= succCost): continue
			elif(node in close[:][1]['xy']):
				if(openn[index][1]['curCost'] <= succCost): continue
				closed[index]['curCost'] = succCost
				heapq.heappush(openn, (closed[index]["estCost"] + closed[index]["curCost"], closed[index]))
				del closed[index] #YIEKS
			else:
				openDictionatry = {"xy": node, "estCost": h(node, dest), "curCost": succCost, "parent": cur}
				heapq.heappush(openn, (openDictionatry["estCost"] + openDictionatry["curCost"], openDictionatry))

		closed.append(cur)

	#backtracking to find the next tile
	if(cur['xy'] == dest):
		prevCur = cur
		while(cur['parent'] is not None):
			prevCur = cur
			cur = cur['parent']
		#set our direction, Joss has a feeling this will need debugging, talk to Joss about it
		if (prevCur['xy'][0] == head[0]+1 and prevCur['xy'][1] == head[1]):
			out = 'right'
		elif (prevCur['xy'][0] == head[0]-1 and prevCur['xy'][1] == head[1]):
			out = 'left'
		elif (prevCur['xy'][0] == head[0] and prevCur['xy'][1] == head[1]+1):
			out = 'down'
		elif (prevCur['xy'][0] == head[0] and prevCur['xy'][1] == head[1]-1):
			out = 'up'
	else:
		raise Exception('Path not found')


@bottle.post('/move')
def move():
	data = bottle.request.json
	myID = data['you']['id']
	grid, head = make_grid(data)
	nextLoc = findFood(grid, head)
	findBlocked(grid, head)
	final_dir = aStar(grid, head)
    # TODO: Do things with data
    #directions = ['up', 'down', 'left', 'right']

	return {
		#'move': random.choice(directions),
		'move': final_dir,
		'taunt': 'WELP!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
