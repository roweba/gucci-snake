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
	
	heapq.heappush(open, ((h(head, dest)), head))
	while(open):
		cur = heappop(open)
		if (cur[0] == head[0]+1 and cur[1] == head[1]):
			out = 'right'
		elif (cur[0] == head[0]-1 and cur[1] == head[1]):
			out = 'left'
		elif (cur[0] == head[0] and cur[1] == head[1]+1):
			out = 'down'
		elif (cur[0] == head[0] and cur[1] == head[1]-1):
			out = 'up'
			
		if (cur == dest):
			return out

		succ	
			
		if (board[cur[0]+1][cur[1]] > 0):
			

			
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


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
