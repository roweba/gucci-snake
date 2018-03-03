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
		'color': '#FF3399',
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

	head = [data['you']['body']['data'][0]['x'], data['you']['body']['data'][0]['y']]

	return grid, head


#initialize point from i,j coordinates
#make if statements to check what is on the point
#return value of the grid space
def set_grid(i,j,data):

	snake_list = data['snakes']['data']
	food_list = data['food']['data']
	my_length = data['you']['length']
	snake_heads = []

	#make a list of snake head coords as tuples of (x,y) points
	for snake in range(0, len(snake_list)):
		x = snake_list[snake]['body']['data'][0]['x']
		y = snake_list[snake]['body']['data'][0]['y']
		snake_heads.append([x,y])

	#our head
	if data['you']['body']['data'][0]['x'] == i and data['you']['body']['data'][0]['y'] == j:
		return 0

	#our tail
	if data['you']['body']['data'][my_length-1]['x'] == i and data['you']['body']['data'][my_length-1]['y'] == j:
		return 2

	#other snakes' body
	for snake in range(0, len(snake_list)):
		for snake_point in range(0,len(snake_list[snake]['body']['data'])):
			x = snake_list[snake]['body']['data'][snake_point]['x']
			y = snake_list[snake]['body']['data'][snake_point]['y']
			if x == i and y == j:
				return -1

	#halo
	for snake in range(0, len(snake_list)):
		#if point is adjacent to a point in the heads list mark the spot as -2 (halo)
		x = snake_list[snake]['body']['data'][0]['x']
		y = snake_list[snake]['body']['data'][0]['y']
		if [x+1,y] in snake_heads or [x-1,y] in snake_heads or [x,y+1] in snake_heads or [x,y-1] in snake_heads:
			return -2

	#food
	for food in range(0, len(food_list)):
		x = food_list[food]['x']
		y = food_list[food]['y']
		if x == i and y == j:
			return 8

	#empty
	return 1

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

		#this is jank figure out whats really happening pls
		if (cur[0] < len(grid) and cur[0] >= 0 and cur[1] < len(grid[0]) and cur[1] >= 0):
			pass
		else:
			continue

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
	min_cost = 0
	#node dictionary format:
	#"xy": a tuple in the form (x, y) signifying the position of the node
	#"estCost": the estimated cost to get to dest from here [h]
	#"curCost": the cost taken to reach this node [g]
	#"parent": the previous node in the path

	headNode = {"xy": head, "estCost": h(head, dest), "curCost": 0, "parent": None}
	heapq.heappush(openn, (headNode["estCost"] + headNode["curCost"], headNode))#push where we are to start off
	while(openn):#while we have things to check
		cur = heapq.heappop(openn)[1]#pop the best thing from the priority queue

		#if we find our destination return our initial direction
		if (cur['xy'] == dest):
			break

		#add safe tiles around the current tile to the list of successors
		if (cur['xy'][0]+1 < len(board)):#make sure we are in bounds
			#print('*'*64, 'index:', cur['xy'][0]+1, 'total:', len(board))
			if (board[cur['xy'][0]+1][cur['xy'][1]] > 0):#is the tile safe
				succ.append([cur['xy'][0]+1, cur['xy'][1]])#if so add that tile to be examined
		if (cur['xy'][0]-1 > 0):
			if (board[cur['xy'][0]-1][cur['xy'][1]] > 0):
				succ.append([cur['xy'][0]-1, cur['xy'][1]])

		if (cur['xy'][1]+1 < len(board[0])):
			#print('*'*64, 'index:', cur['xy'][0]+1, 'total:', len(board))
			try:
				if (board[cur['xy'][0]][cur['xy'][1]+1] > 0):
					succ.append([cur['xy'][0], cur['xy'][1]+1])
			except IndexError:
				print 'CAUGHT THE FIRST ERROR: ', len(board[0]), cur['xy'][1]+1
		if (cur['xy'][1]-1 > 0):

			if (board[cur['xy'][0]][cur['xy'][1]-1] > 0):
				succ.append([cur['xy'][0], cur['xy'][1]-1])

		for node in succ:
			succCost = 1 + cur["curCost"]
			if(node in [x[1]['xy'] for x in openn]): #FIXME this might be broken
				index = [x[1]['xy'] for x in openn].index(node) #This line might also be broken
				if(openn[index][1]['curCost'] <= succCost): continue
			elif(node in [x['xy'] for x in close]):
				#print('-'*20, openn[index])
				index = [x['xy'] for x in close].index(node)
				if(close[index]['curCost'] <= succCost): continue
				try:
					close[index]['curCost'] = succCost
				except IndexError:
					print 'CAUGHT THE SECOND ERROR: ', index, 'length: ', len(close)
					print '^^^^^^^^ close[index] = ', close['index']
				heapq.heappush(openn, (close[index]["estCost"] + close[index]["curCost"], close[index]))
				del close[index] #YIEKS
			else:
				openDictionary = {"xy": node, "estCost": h(node, dest), "curCost": succCost, "parent": cur}
				heapq.heappush(openn, (openDictionary["estCost"] + openDictionary["curCost"], openDictionary))

		close.append(cur)

	#backtracking to find the next tile
	if(cur['xy'] == dest):
		print 'Found the destination!!!'
		prevCur = cur
		while(cur['parent'] is not None):
			prevCur = cur
			cur = cur['parent']
			min_cost += 1
		#set our direction, Joss has a feeling this will need debugging, talk to Joss about it
		if (prevCur['xy'][0] == head[0]+1 and prevCur['xy'][1] == head[1]):
			out = 'right'
		elif (prevCur['xy'][0] == head[0]-1 and prevCur['xy'][1] == head[1]):
			out = 'left'
		elif (prevCur['xy'][0] == head[0] and prevCur['xy'][1] == head[1]+1):
			out = 'down'
		elif (prevCur['xy'][0] == head[0] and prevCur['xy'][1] == head[1]-1):
			out = 'up'
		return out, min_cost
	else:
		raise Exception('Path not found')

#def safemove():
	#if there are no openings to food, stall until there are

def closest_wall(data,grid,head,tail):
	walls = [] #list walls as [x,y points]
	board_width = data['width']
	board_length = data['length']
	closest_wall = [] #[x,y] point of the closest wall
	min_cost = 100000

	#make a list of points that are the grid edges
	for i in range(board_width-1):
		walls.append([i,0])
	for j in range(board_length-1):
		walls.append([0,j])
	for k in range(board_width-1):
		walls.append([board_width-1,k])
	for x in range(board_length-1):
		walls.append([board_length-1,x])

	for index in range(walls):
		curr_cost = aStar(grid, head, walls[index])[1]
		if curr_cost < min_cost:
			min_cost = curr_cost
			closest_wall = walls[index]

	closest_food = findFood(grid, head)
	aStar(grid, head, closest_food)
	while data['you']['health'] + closest_food > 30:
		aStar(grid,head,tail)


#def final_move():

@bottle.post('/move')
def move():
	data = bottle.request.json
	myID = data['you']['id']
	grid, head = make_grid(data)

	for i in range(len(grid)):
		print grid[i]

	findBlocked(grid, head)
	nextLoc = findFood(grid, head)
	final_dir = aStar(grid, head, nextLoc)
	print('>>>>>>>>>>>>>>>>>', final_dir)
	# TODO: Do things with data
	#directions = ['up', 'down', 'left', 'right']

	return {
		#'move': random.choice(directions),
		'move': final_dir,
		'taunt': 'skrrt'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
