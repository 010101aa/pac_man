import pygame, math, os, platform
pygame.init()

if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_profiles")):
	os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_profiles"))

class Config():

	def __init__(self):
		self.skript_path = os.path.abspath(__file__)
		self.config_path = os.path.dirname(self.skript_path) + "/config.txt"
		self.dir_path = os.path.dirname(self.skript_path)

		with open(self.config_path, "r") as file:
			self.config_dict = eval(file.read())

		self.draw_walls = self.config_dict["draw_walls"]
		self.draw_ecks = self.config_dict["draw_ecks"]
		self.eck_color = self.config_dict["eck_color"]
		self.draw_points = self.config_dict["draw_points"]
		self.draw_score = self.config_dict["draw_score"]
		self.draw_pac_man = self.config_dict["draw_pac_man"]
		self.fill_screen = self.config_dict["fill_screen"]
		self.draw_walls_base = self.config_dict["draw_walls_base"]
		self.draw_ghost = self.config_dict["draw_ghost"]
		self.draw_ghost_base = self.config_dict["draw_ghost_base"]
		self.ghost_color = self.config_dict["ghost_color"]
		self.draw_pac_man_base = self.config_dict["draw_pac_man_base"]
		self.pac_man_color = self.config_dict["pac_man_color"]
		self.wall_color = self.config_dict["wall_color"]
		self.point_color = self.config_dict["point_color"]
		self.score_color = self.config_dict["score_color"]
		self.fill_screen_color = self.config_dict["fill_screen_color"]
		self.button_color = self.config_dict["button_color"]
		self.draw_button_base = self.config_dict["draw_button_base"]
		self.text_color = self.config_dict["text_color"]
		self.draw_button_text = self.config_dict["draw_button_text"]
		self.button_text_color = self.config_dict["button_text_color"]

	def reset(self):
		with open(self.dir_path + "/config.txt", "w") as file:
			with open(self.dir_path + "/config_back_up.txt", "r") as back_up_file:
				file.write(back_up_file.read())

config = Config()

class Vektor():

	def __init__(self, p_1, p_2):
		self.ghost_x, self.ghost_y = p_1[0], p_1[1]
		self.pac_man_x, self.pac_man_y = p_2[0], p_2[1]
		self.vektor = (self.pac_man_x - self.ghost_x, self.pac_man_y - self.ghost_y)
		self.length = math.sqrt(self.vektor[0] ** 2 + self.vektor[1] ** 2)

class Window():

	def __init__(self):
		self.width, self.height = 1000, 700
		self.clock, self.tick = pygame.time.Clock(), 90
		self.screen = None
		self.running = True
		self.map_list = []
		self.points_left = 0
		self.font = pygame.font.Font(None, 50)
		self.won_text = self.font.render("YOU WIN", True, config.text_color)
		self.lost_text = self.font.render("YOU LOOSE", True, config.text_color)
		self.read_map()
		self.won = False
		self.center_rect = self.won_text.get_rect(center=(self.width / 2, self.height / 2))
		self.block_pic = pygame.image.load(config.dir_path + "/images/block/block.png")
		self.back_button = Button(self.width - 200, 50, 150, 40, "rect", self.font.render("Back", True, config.button_text_color), "back")
		self.reset_button = Button(self.width - 200, 100, 150, 40, "rect", self.font.render("Reset", True, config.button_text_color), "reset")
		self.do_reset = False

	def draw(self, pac_man, point_list, ghost_list):
		if config.fill_screen:
			self.screen.fill(config.fill_screen_color)

		if config.draw_pac_man:
			pac_man.draw(self.screen)

		if config.draw_walls:
			if config.draw_walls_base:
				for block in self.map_list:
					if block[0] == "#":
						pygame.draw.rect(self.screen, config.wall_color, (block[1] * 25, block[2] * 25, 25, 25))

			else:
				for block in self.map_list:
					if block[0] == "#":
						self.screen.blit(self.block_pic, (block[1] * 25, block[2] * 25, 25, 25))

		if config.draw_points:
			for block in self.map_list:
				if block[0] == ".":
					pygame.draw.circle(self.screen, config.point_color, (block[1] * 25 + 12.5, block[2] * 25 + 12.5), 2)

		for ghost in ghost_list:
			ghost.draw(self.screen)

		for point in point_list:
			point.draw(self.screen)

		if config.draw_score:
			self.screen.blit(self.font.render(str(self.points_left), True, config.score_color), (5, 5))

		if self.won:
			self.screen.blit(self.won_text, self.center_rect)

		for ghost in ghost_list:
			if ghost.won:
				self.screen.blit(self.lost_text, self.center_rect)

		self.back_button.draw(self.screen)
		self.reset_button.draw(self.screen)

	def update(self, pac_man, point_list, point_maker, ghost_list):
		pac_man.update(self.map_list, self.width, self.height, point_list)

		for ghost in ghost_list:
			ghost.update(pac_man, self.width, self.height, point_list)

		for index, block in enumerate(self.map_list):
			if block[0] == ".":
				if pac_man.rect.colliderect(block[3]):
					self.points_left -= 1
					del self.map_list[index]

		if self.points_left == 0:
			self.won = True

		keys = pygame.key.get_pressed()

		if keys[pygame.K_r]:
			self.read_map()

	def mainloop(self, pac_man, point_maker, ghost_list, menu):
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Pack Man")

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					self.running = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.back_button.check_click(pygame.mouse.get_pos()):
						self.running = False

					if self.reset_button.check_click(pygame.mouse.get_pos()):
						self.reset(menu)

			if not self.running:
				break

			self.point_list = point_maker.point_list

			self.update(pac_man, self.point_list, point_maker, ghost_list)
			self.draw(pac_man, self.point_list, ghost_list)

			self.clock.tick(self.tick)

			point_maker.__init__()
			config.__init__()

			pygame.display.flip()

		if not self.do_reset:
			main()

	def read_map(self):
		self.map_list = []
		self.points_left = 0
		with open(config.dir_path + "/map.txt") as file:
			for row, line in enumerate(file.readlines()):
				for column, char in enumerate(line.strip()):
					if char == ".":
						self.points_left += 1
					if char != " ":
						rect = pygame.Rect(column * 25 + 1, row * 25 + 1, 23, 23)
						self.map_list.append([char, column, row, rect])

	def reset(self, menu):
		self.do_reset = True
		self.running = False
		menu.start_game()

class WayEndPoint():

	def __init__(self, x, y, n_right, n_left, n_down, n_up):
		self.x, self.y = x, y
		self.right, self.left = pygame.Rect(self.x + 24, self.y, 1, 25), pygame.Rect(self.x, self.y, 1, 25)
		self.down, self.up = pygame.Rect(self.x, self.y + 24, 25, 1), pygame.Rect(self.x, self.y, 25, 1)
		self.rect_list = [self.right, self.left, self.down, self.up]
		self.n_right = n_right
		self.n_left = n_left
		self.n_down = n_down
		self.n_up = n_up
		self.n_list = []
		if self.n_right:
			self.n_list.append("right")

		if self.n_left:
			self.n_list.append("left")

		if self.n_down:
			self.n_list.append("down")

		if self.n_up:
			self.n_list.append("up")

	def draw(self, screen):
		if config.draw_ecks:
			pygame.draw.rect(screen, config.eck_color, self.right)
			pygame.draw.rect(screen, config.eck_color, self.left)
			pygame.draw.rect(screen, config.eck_color, self.down)
			pygame.draw.rect(screen, config.eck_color, self.up)

			if self.n_right:
				pygame.draw.rect(screen, config.eck_color, (self.x + 25, self.y + 12, 25, 1))

			if self.n_left:
				pygame.draw.rect(screen, config.eck_color, (self.x - 25, self.y + 12, 25, 1))

			if self.n_down:
				pygame.draw.rect(screen, config.eck_color, (self.x + 12, self.y + 25, 1, 25))

			if self.n_up:
				pygame.draw.rect(screen, config.eck_color, (self.x + 12, self.y - 25, 1, 25))

class PointMaker():

	def __init__(self):
		self.map_name = config.dir_path + "/map.txt"
		self.row_list = []
		self.column_list = []
		self.point_list_ro = []
		self.point_list = []
		self.max_row_len = 0
		self.load()

	def load(self):
		with open(self.map_name, "r") as file:
			for line in file.readlines():
				if len(line.strip()) > self.max_row_len:
					self.max_row_len = len(line.strip())

				self.row_list.append(line.strip())

			for index in range(self.max_row_len):
				temp_list = []
				for row in self.row_list:
					temp_list.append(row[index])

				self.column_list.append("".join(temp_list))

		with open(self.map_name) as file:
			for row, line in enumerate(file.readlines()):
				for column, char in enumerate(line.strip()):
					if char == "." or char == " ":
						point = [column * 25, row * 25, False, False, False, False]
						if self.row_list[row][column + 1] == "." or self.row_list[row][column + 1] == " ":
							point[2] = True

						if self.row_list[row][column - 1] == "." or self.row_list[row][column - 1] == " ":
							point[3] = True

						if self.column_list[column][row + 1] == "." or self.column_list[column][row + 1] == " ":
							point[4] = True

						if self.column_list[column][row - 1] == "." or self.column_list[column][row - 1] == " ":
							point[5] = True

						if point[2] == True and point[3] == True and point[4] == False and point[5] == False:
							pass

						elif point[2] == False and point[3] == False and point[4] == True and point[5] == True:
							pass

						else:
							self.point_list_ro.append(point)

		for point in self.point_list_ro:
			self.point_list.append(WayEndPoint(point[0], point[1], point[2], point[3], point[4], point[5]))

class PackMan():

	def __init__(self, window):
		self.x, self.y = 325, 550
		self.width, self.height = 25, 25
		self.vars = [1, 1, 1, 1]
		self.image = pygame.image.load(config.dir_path + "/images/pack_man_ra/pack_man_r0.png")
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.direction = None
		self.next_direction = None
		self.window = window
		self.ani_cicle, self.ani_cicle_dir, self.ani_counter = 0, 1, 3
		self.animate_w = True
		self.at_point = None
		self.first = True

	def animate(self):
		if self.ani_counter == 0:
			if self.ani_cicle == 5:
				self.ani_cicle = 3
				self.ani_cicle_dir *= -1

			if self.ani_cicle == -1:
				self.ani_cicle = 1
				self.ani_cicle_dir *= -1

			if self.direction == "right":
				self.image = pygame.image.load(config.dir_path + f"/images/pack_man_ra/pack_man_r{self.ani_cicle}.png")

			if self.direction == "left":
				self.image = pygame.image.load(config.dir_path + f"/images/pack_man_la/pack_man_l{self.ani_cicle}.png")

			if self.direction == "down":
				self.image = pygame.image.load(config.dir_path + f"/images/pack_man_da/pack_man_d{self.ani_cicle}.png")

			if self.direction == "up":
				self.image = pygame.image.load(config.dir_path + f"/images/pack_man_ua/pack_man_u{self.ani_cicle}.png")

			self.ani_counter = 3
			if self.animate_w:
				self.ani_cicle += self.ani_cicle_dir

		else:
			self.ani_counter -= 1

	def draw(self, screen):
		if config.draw_pac_man_base:
			pygame.draw.rect(screen, config.pac_man_color, self.rect)

		else:
			self.animate()
			screen.blit(self.image, self.rect)

	def update(self, map_list, width, height, point_list):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.next_direction = "right"

		if keys[pygame.K_LEFT]:
			self.next_direction = "left"

		if keys[pygame.K_DOWN]:
			self.next_direction = "down"

		if keys[pygame.K_UP]:
			self.next_direction = "up"
		
		point_in = None
		at_point = False
		collides = 0
		for index, point in enumerate(point_list):
			for p_rect in point.rect_list:
				if p_rect.colliderect(self.rect):
					collides += 1
					point_in = index

		if collides == 4:
			if point_in != None and self.next_direction in point_list[point_in].n_list:
				self.direction = self.next_direction
				at_point = True

			else:
				self.direction = None

		if not at_point:
			if self.direction == "right" and self.next_direction == "left":
				self.direction = self.next_direction

			if self.direction == "left" and self.next_direction == "right":
				self.direction = self.next_direction

			if self.direction == "down" and self.next_direction == "up":
				self.direction = self.next_direction

			if self.direction == "up" and self.next_direction == "down":
				self.direction = self.next_direction

		if self.first:
			if self.next_direction == "left" or self.next_direction == "right":
				self.direction = self.next_direction
				self.first = False
		
		if self.direction == "right":
			self.x += self.vars[0]

		elif self.direction == "left":
			self.x -= self.vars[1]

		elif self.direction == "down":
			self.y += self.vars[2]


		elif self.direction == "up":
			self.y -= self.vars[3]

		self.x = max(0, min(width - self.width, self.x))
		self.y = max(0, min(height - self.height, self.y))
	        
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Ghost():

	def __init__(self, x, y, path_left, path_right):
		self.x, self.y = x, y
		self.image_left = pygame.image.load(path_left)
		self.image_right = pygame.image.load(path_right)
		self.image = self.image_left
		self.rect = pygame.Rect(self.x, self.y, 25, 25)
		self.won = False
		self.direction = "right"
		self.directions = ["right", "left", "down", "up"]
		self.opp_direction_dict = {"right":"left", "left":"right", "down":"up", "up":"down"}
		self.next_direction = "right"
		self.var = 0.5

	def draw(self, screen):
		if config.draw_ghost:
			if config.draw_ghost_base:
				pygame.draw.rect(screen, config.ghost_color, self.rect)

			else:
				if self.direction == "right":
					self.image = self.image_right

				if self.direction == "left":
					self.image = self.image_left

				screen.blit(self.image, self.rect)

	def update(self, pac_man, width, height, point_list):
		if self.rect.colliderect(pac_man.rect):
			self.won = True

		point_in = None
		at_point = False
		collides = 0
		for index, point in enumerate(point_list):
			for p_rect in point.rect_list:
				if p_rect.colliderect(self.rect):
					collides += 1
					point_in = index

		len_dict = {}
		if collides == 4:
			p_n_list = point_list[point_in].n_list
			if self.opp_direction_dict[self.direction] in p_n_list:
				p_n_list.remove(self.opp_direction_dict[self.direction])

			for direction in p_n_list:
				if direction == "right":
					len_dict.update({Vektor((self.x + 25, self.y), (pac_man.x, pac_man.y)).length:"right"})

				if direction == "left":
					len_dict.update({Vektor((self.x - 25, self.y), (pac_man.x, pac_man.y)).length:"left"})

				if direction == "down":
					len_dict.update({Vektor((self.x, self.y + 25), (pac_man.x, pac_man.y)).length:"down"})

				if direction == "up":
					len_dict.update({Vektor((self.x, self.y - 25), (pac_man.x, pac_man.y)).length:"up"})

			if len_dict == {}:
				self.direction = self.opp_direction_dict[self.direction]

			else:
				self.direction = len_dict[min(len_dict.keys())]

		if self.direction == "right":
			self.x += self.var

		elif self.direction == "left":
			self.x -= self.var

		elif self.direction == "down":
			self.y += self.var

		elif self.direction == "up":
			self.y -= self.var

		self.x = max(0, min(width - 25, self.x))
		self.y = max(0, min(height - 25, self.y))

		self.rect = self.rect = pygame.Rect(self.x, self.y, 25, 25)

class Button():

	def __init__(self, x, y, width, height, button_type, image, action):
		self.x, self.y = x, y
		self.width, self.height = width, height
		self.type = button_type
		self.event = action
		self.text_button = False
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.text_length = 0
		self.image_text_b = pygame.image.load(config.dir_path + "/images/menu/buttons/button_text_b.png")
		self.image_text_e = pygame.image.load(config.dir_path + "/images/menu/buttons/button_text_e.png")
		self.image_text_m = pygame.image.load(config.dir_path + "/images/menu/buttons/button_text_m.png")

		if image != None:
			if isinstance(image, str):
				self.image = pygame.image.load(image)

			else:
				self.image = image
				self.text_button = True
				self.text_length = len(action)

		else:
			self.image = None

	def draw(self, screen):
		config.__init__()
		if config.draw_button_base or self.image == None:
			if self.type == "circle":
				pygame.draw.circle(screen, config.button_color, (self.x, self.y), (self.width / 2 + self.height / 2) / 2)

			if self.type == "rect":
				pygame.draw.rect(screen, config.button_color, (self.x, self.y, self.width, self.height))

		else:
			if self.image != None:
				if self.text_button:
					for i in range(self.text_length + 1):
						if i == 0:
							screen.blit(self.image_text_b, (self.x - 10, self.y))

						if i == self.text_length:
							screen.blit(self.image_text_e, (self.x + 20 * (i - 1) - 10, self.y))

						else:
							screen.blit(self.image_text_m, (self.x + 20 * i - 10, self.y))

						if config.draw_button_text:
							screen.blit(self.image, (self.x, self.y))

				elif not self.text_button:
					screen.blit(self.image, (self.x, self.y))

	def check_click(self, mouse_pos):
		if self.x < mouse_pos[0] < self.x + self.width:
			if self.y < mouse_pos[1] < self.y + self.height:
				return True

		else:
			return False

	def __repr__(self):
		return f"X: {self.x}, Y: {self.y}, Event: {self.event}, TextButton: {self.text_button}"

class Edit():

	def __init__(self):
		pygame.init()

		self.options = ["Colors", "Pictures", "Drawing", "Save", "Load", "Delete", "Reset", "Help", "Back"]
		self.first_y = 100
		self.font = pygame.font.Font(None, 50)
		self.small_font = pygame.font.Font(None, 25)
		self.selected_option = None
		self.sub_option = None
		self.clicked = False
		self.color_options = []
		self.color_buttons = []
		self.picture_paths = []
		self.input = False
		self.input_string = ""
		self.input_key = ""
		self.draw_options = []
		self.draw_option_buttons = []
		self.draw_option_values = []
		self.get_draw_options()
		self.get_color_options()
		self.get_picture_paths()
		self.clock = pygame.time.Clock()
		self.tick = 24
		self.swich_button = None
		self.temp_config_dict = config.config_dict
		self.temp_config_dict.update({"back":""})
		self.input_name = ""
		self.input_name_bool = False
		self.load_failed = False

		self.button_list = []

		for index, option in enumerate(self.options):
			self.button_list.append(Button(50, index * 50 + self.first_y,
											20 * len(option), 40, "rect", self.font.render(option, True,
											config.button_text_color), option.lower()))

	def mainloop(self):
		screen = pygame.display.set_mode((1000, 700))
		pygame.display.set_caption("Pac Man")

		self.running = True
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					self.clicked = True

				if event.type == pygame.KEYDOWN:
					if self.input:
						if event.key == pygame.K_RETURN and self.input:
							self.input = False

							try:
								new_tulpe = eval(self.input_string)

							except Exception:
								new_tulpe = config.config_dict[self.input_key]
								
							self.temp_config_dict.update({self.input_key:new_tulpe})

							config.config_dict = self.temp_config_dict
							with open(config.dir_path + "/config.txt", "w") as file:
								file.write(str(config.config_dict))

							self.input_string = ""
							self.temp_config_dict = config.config_dict

						elif event.key == pygame.K_BACKSPACE:
							self.input_string = self.input_string[:-1]

						else:
							self.input_string += event.unicode

					elif self.input_name_bool:
						if event.key == pygame.K_BACKSPACE:
							self.input_name = self.input_name[:-1]

						else:
							self.input_name += event.unicode

						self.load_failed = False

			if config.fill_screen:
				screen.fill(config.fill_screen_color)

			if self.selected_option == None:
				for button in self.button_list:
					button.draw(screen)
					if self.clicked and button.check_click(pygame.mouse.get_pos()):
						if button.event != "back":
							self.selected_option = button.event

						else:
							self.running = False

				self.input = False

			elif self.selected_option == "help":
				self.selected_option = None
				if platform.system() == "Windows":
					os.system("start " + config.dir_path + "/help.txt")

				elif platform.system() == "Darwin":
					os.system("open " + config.dir_path + "/help.txt")

			elif self.selected_option == "deinstall":
				self.selected_option = None

			elif self.selected_option == "save":
				self.input_name_bool = True

				screen.blit(self.font.render("Name:", True, config.text_color), (250, self.first_y))
				screen.blit(self.font.render(self.input_name, True, config.text_color), (400, self.first_y))

				save_button = Button(100, 200, 150, 40, "rect", self.font.render("Save", True, config.button_text_color), "save")
				back_button = Button(100, 650, 150, 40, "rect", self.font.render("Back", True, config.button_text_color), "back")

				save_button.draw(screen)
				back_button.draw(screen)

				if self.clicked and back_button.check_click(pygame.mouse.get_pos()):
					self.selected_option = None

				if self.clicked and save_button.check_click(pygame.mouse.get_pos()) and self.input_name != "":
					with open(config.dir_path + "/config_profiles/" + self.input_name + ".txt", "w") as file:
						file.write(str(config.config_dict))

					self.selected_option = None
					self.input_name_bool = False

			elif self.selected_option == "load":
				self.input_name_bool = True

				screen.blit(self.font.render("Name:", True, config.text_color), (250, self.first_y))
				screen.blit(self.font.render(self.input_name, True, config.text_color), (400, self.first_y))

				load_button = Button(100, 200, 150, 40, "rect", self.font.render("Load", True, config.button_text_color), "load")
				back_button = Button(100, 650, 150, 40, "rect", self.font.render("Back", True, config.button_text_color), "back")
				if self.sub_option == None:
					list_button = Button(100, 300, 150, 40, "rect", self.font.render("List", True, config.button_text_color), "list")

				load_button.draw(screen)
				back_button.draw(screen)
				if self.sub_option == None:
					list_button.draw(screen)

				if self.sub_option == "config_list":
					for index, file in enumerate(os.listdir(config.dir_path + "/config_profiles/")):
						if file != ".DS_Store":
							screen.blit(self.small_font.render(file[:-4], True, config.text_color), (400, self.first_y + 50 + index * 25))

				if self.clicked and back_button.check_click(pygame.mouse.get_pos()):
					if self.sub_option != None:
						self.sub_option = None

					else:
						self.selected_option = None

				if self.clicked and list_button.check_click(pygame.mouse.get_pos()):
					self.sub_option = "config_list"

				if self.clicked and load_button.check_click(pygame.mouse.get_pos()) and self.input_name != "":
					try:
						with open(config.dir_path + "/config_profiles/" + self.input_name + ".txt", "r") as load_file:
							with open(config.config_path, "w") as config_file:
								config_file.write(load_file.read())

						self.input_name = ""
						self.selected_option = None

					except FileNotFoundError:
						self.load_failed = True

				if self.load_failed:
					screen.blit(self.font.render("Wrong Name", True, config.text_color), (250, 200))

			elif self.selected_option == "reset":
				self.selected_option = None
				config.reset()

			elif self.selected_option == "colors":
				for button in self.color_buttons:
					button.draw(screen)
					screen.blit(self.font.render(str(self.temp_config_dict[button.event]), True, config.text_color), (button.x + 400, button.y))

					if self.clicked and button.check_click(pygame.mouse.get_pos()):
						if button.event == "back":
							self.selected_option = None

						else:
							self.input = True
							self.input_key = button.event

			elif self.selected_option == "delete":
				self.input_name_bool = True

				screen.blit(self.font.render("Name:", True, config.text_color), (250, self.first_y))
				screen.blit(self.font.render(self.input_name, True, config.text_color), (400, self.first_y))
				if self.sub_option == None:
					list_button = Button(100, 300, 150, 40, "rect", self.font.render("List", True, config.button_text_color), "list")


				delete_button = Button(100, 200, 150, 40, "rect", self.font.render("Delete", True, config.button_text_color), "delete")
				back_button = Button(100, 650, 150, 40, "rect", self.font.render("Back", True, config.button_text_color), "back")
				
				if self.sub_option == None:
					list_button.draw(screen)

				delete_button.draw(screen)
				back_button.draw(screen)

				if self.sub_option == "config_list":
					for index, file in enumerate(os.listdir(config.dir_path + "/config_profiles/")):
						if file != ".DS_Store":
							screen.blit(self.small_font.render(file[:-4], True, config.text_color), (400, self.first_y + 50 + index * 25))

				if self.clicked and list_button.check_click(pygame.mouse.get_pos()):
					self.sub_option = "config_list"

				if self.clicked and back_button.check_click(pygame.mouse.get_pos()):
					if self.sub_option != None:
						self.sub_option = None

					else:
						self.selected_option = None

				if self.clicked and delete_button.check_click(pygame.mouse.get_pos()) and self.input_name != "":
					os.remove(config.dir_path + "/config_profiles/" + self.input_name + ".txt")

					self.selected_option = None
					self.input_name_bool = False

			if self.input:
				self.temp_config_dict.update({self.input_key:self.input_string})

			elif self.selected_option == "drawing":
				self.get_draw_options()
				for index, button in enumerate(self.draw_option_buttons):
					button.draw(screen)

					if index < len(self.draw_option_values):
						screen.blit(self.font.render(str(self.draw_option_values[index]),
								True, config.text_color), (button.x + 500, button.y))

					elif self.clicked and button.check_click(pygame.mouse.get_pos()):
						self.selected_option = None
						continue

					if self.clicked and button.check_click(pygame.mouse.get_pos()):
						if config.config_dict[button.event]:
							config.config_dict.update({button.event:False})

						elif not config.config_dict[button.event]:
							config.config_dict.update({button.event:True})
						
						with open(config.config_path, "w") as file:
							file.write(str(config.config_dict))

				self.input = False

			if self.selected_option == "pictures":
				if self.sub_option == None:
					for index, path in enumerate(self.picture_paths):
						screen.blit(self.small_font.render(str(path), True, config.text_color), (400, index * 25))

					screen.blit(self.font.render("General:", True, config.text_color), (100, 0))

				elif self.sub_option == "pac_man":
					for index, path in enumerate(self.pac_man_pictures):
						screen.blit(self.small_font.render(str(path), True, config.text_color), (400, index * 25))

					screen.blit(self.font.render("Pac Man:", True, config.text_color), (100, 0))

				back_button = Button(100, 650, 150, 40, "rect", self.font.render("Back", True, config.button_text_color), "back")
				back_button.draw(screen)
				if back_button.check_click(pygame.mouse.get_pos()) and self.clicked:
					if self.sub_option == None:
						self.selected_option = None

					else:
						self.sub_option = None

				pac_man_button = Button(400, 650, 150, 40, "rect",
										self.font.render("Pac Man", True, config.button_text_color), "pac_man")
				pac_man_button.draw(screen)

				if pac_man_button.check_click(pygame.mouse.get_pos()) and self.clicked:
					self.sub_option = "pac_man"

				self.input = False

			config.__init__()

			self.get_color_options()
			self.get_draw_options()

			self.clicked = False

			self.clock.tick(self.tick)
			pygame.display.flip()

		main()

	def get_color_options(self):
		self.color_options = []
		self.color_buttons = []

		for key, value in config.__dict__.items():
			if "color" in key:
				self.color_options.append(key)

		for index, option in enumerate(self.color_options):
			self.color_buttons.append(
				Button(250, index * 50 + self.first_y,
				20 * len(option), 40, "rect", self.font.render(option.replace("_", " "), True, config.button_text_color),
				option.lower())
				)

		self.color_buttons.append(
			Button(250, (len(self.color_buttons) + 1) * 50 + self.first_y,
			100, 40, "rect", self.font.render("back", True, config.button_text_color),
			"back")
			)

	def get_picture_paths(self):
		self.pac_man_pictures = []
		self.picture_paths = []

		dir_images = config.dir_path + "/images/"

		for dir_path, sub_dir, files in os.walk(dir_images):
			for file in files:
				if file != ".DS_Store":
					if "pack_man" in file:
						self.pac_man_pictures.append(file)

					else:
						self.picture_paths.append(file)

		self.picture_paths.append("")
		self.pac_man_pictures.append("")
		self.picture_paths.append(f"Total: {len(self.picture_paths) - 1}")
		self.pac_man_pictures.append(f"Total: {len(self.pac_man_pictures) - 1}")

	def get_draw_options(self):
		self.draw_option_buttons = []
		self.draw_options = []
		self.draw_option_values = []

		for key, value in  config.__dict__.items():
			if "draw" in key:
				self.draw_options.append(key)

				self.draw_option_values.append(value)

		for index, option in enumerate(self.draw_options):
			self.draw_option_buttons.append(
				Button(250, index * 50, 20 * len(option), 40, "rect", self.font.render(option.replace("_", " "), True,
				config.button_text_color), option.lower()
				))

		self.draw_option_buttons.append(
			Button(250, (len(self.draw_option_buttons) + 1) * 50, 100, 40, "rect",
			self.font.render("Back", True, config.button_text_color), "back"
			))

class Menu():

	def __init__(self):
		self.width, self.height = 1000, 700
		self.running = True
		self.button_list = []
		self.next_action = None

		self.button_list.append(Button(self.width / 2 - 100, self.height / 2 - 100, 200, 200, "rect", config.dir_path + 
								"/images/menu/buttons/play_button.png", "start_game()"))

		self.button_list.append(Button(self.width / 2 - 300, self.height / 2  - 50, 100, 100, "rect", config.dir_path + 
								"/images/menu/buttons/config_button.png", "edit_profile()"))

	def mainloop(self):
		screen = pygame.display.set_mode((self.width, self.height))

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					for button in self.button_list:
						if button.check_click(pygame.mouse.get_pos()):
							self.running = False
							self.next_action = button.event

			if self.running == False:
				break

			if config.fill_screen:
				screen.fill(config.fill_screen_color)

			for button in self.button_list:
				button.draw(screen)

			config.__init__()

			pygame.display.flip()

		if self.next_action != None:
			eval(f"self.{self.next_action}")

	def start_game(self):
		window = Window()
		pack_man = PackMan(window)

		point_maker = PointMaker()

		ghost = Ghost(25, 25, config.dir_path + "/images/ghost/ghost_left_red.png", config.dir_path + "/images/ghost/ghost_right_red.png")

		ghost_2 = Ghost(625, 25, config.dir_path + "/images/ghost/ghost_left_yellow.png", config.dir_path + "/images/ghost/ghost_right_yellow.png")

		ghost_3 = Ghost(25, 650, config.dir_path + "/images/ghost/ghost_left_purple.png", config.dir_path + "/images/ghost/ghost_right_purple.png")

		ghost_list = [ghost, ghost_2, ghost_3]

		window.mainloop(pack_man, point_maker, ghost_list, self)

	def edit_profile(self):
		edit_class = Edit()
		edit_class.mainloop()

def main():
	menu = Menu()

	menu.mainloop()

if __name__ == "__main__":
	main()
