from copy import copy;
from time import time,sleep;
import curses;

class board():
	def __init__(self, board_size):
		self.size = board_size
		self.body = self.empty_board()

	def change_cell(self, pos, value):
		x,y = pos
		try:
			assert(x > 0 and y>0 and x<= self.size[0] and y <= self.size[1])
		except AssertionError:
			raise KeyError("Boards take positions from 1 to N (inclusive)")
		except Exception as e:
			raise e
		self.body[y][x] = value
	
	def empty_board(self):
		rows    = self.size[1] + 2
		columns = self.size[0] + 2
		create_array = lambda limit, content, size: [copy(limit) if x in [0,size-1] else copy(content) for x in range(size)]
		active_row     = create_array(-1, 0, columns)
		decorative_row = create_array(-3,-2, columns)
		empty_b		   = create_array(decorative_row, active_row, rows) 
		return empty_b
		
	def next_gen(self, debug = False):		
		future_board = self.empty_board()
		for y in range(1,self.size[1] + 1):
			for x in range(1,self.size[0] + 1):
				neighbords = 0
				for c1 in range(-1,2):
					for c2 in range(-1,2):
						if [c1,c2] != [0,0] and self.body[y + c1][x+c2] > -1:
							neighbords += self.body[y + c1][x+c2]
				if neighbords == 3:
					future_board[y][x] = 1
				elif neighbords == 2:
					future_board[y][x] = self.body[y][x]
				else:
					future_board[y][x] = 0
		self.body = future_board
				
	def __str__(self):
		rows = self.size[1] + 2
		prty_str = ("{}\n"*rows)
		values = [' '.join(list(map(str,a))) for a in self.body]
		prty_str = prty_str.format(*values).replace("-1", "|").replace("-2", "+").replace("-3", "-") 
		return prty_str



class Extremely_Quick_and_Dirty_CursesEngine:
	def __init__(self, mainscreen):
		curses.noecho()
		curses.cbreak()
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)	
		gen = 0
		mainscreen.addstr("Select x size: \n")
		mainscreen.addstr("Select y size: \n")
		
		pos = [0,0]
		
		for i in range(2):
			mainscreen.move(i, len("Select x size: "))
			input_x = ""
			last_char = ""
			while last_char != "\n" or not input_x.isdigit():
				last_char = str(mainscreen.getkey())
				if last_char in list("1234567890"):
					input_x += str(last_char)
				elif last_char in ['KEY_BACKSPACE', '^?', 'd']:
					input_x = input_x[:-1]
				mainscreen.move(i, len("Select x size: "))
				mainscreen.addstr("{} \n".format(input_x))
				mainscreen.move(i, len("Select x size: " + input_x))

			pos[1 - i] = int(input_x)
		
		b = board([pos[1],pos[0]])
		
		mainscreen.move(4,0)
		mainscreen.addstr(str(b))
		
		cursor = [5,2]
		mainscreen.move(*cursor)
		max_cursor = [5 + pos[0] - 1, pos[1]*2]
		movement = {'KEY_RIGHT':[0,2],'KEY_LEFT':[0,-2],'KEY_UP':[-1,0],'KEY_DOWN':[1,0]}
		
		last_char = ""
		while last_char != "\n":
				last_char = str(mainscreen.getkey())
				if last_char in movement.keys():
					cursor[0] = max(5, min(cursor[0] + movement[last_char][0] , max_cursor[0]))
					cursor[1] = max(2, min(cursor[1] + movement[last_char][1] , max_cursor[1]))
					mainscreen.move(*cursor)  
				if last_char in "d10":
					position = [cursor[0] - 4, cursor[1]//2]
					value = 1 - b.body[position[0]][position[1]]
					if last_char in "01":
						value = int(last_char)
					b.change_cell([position[1],position[0]], value)
					mainscreen.move(4,0)
					mainscreen.addstr(str(b))
					mainscreen.move(*cursor)
					mainscreen.refresh()
					mainscreen.cursyncup()
		
		previous_time = 0
		while(True):
			current_time = time()
			if(current_time - previous_time>4):
				mainscreen.move(3,0)
				mainscreen.addstr(str("Generation: {}\n".format(gen)), curses.A_REVERSE)
				mainscreen.addstr(str(b))
				mainscreen.refresh()
				previous_time = current_time
				b.next_gen()
				gen += 1
						
		
curses.wrapper(Extremely_Quick_and_Dirty_)
