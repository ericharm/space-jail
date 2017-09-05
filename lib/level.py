from tile import Tile
import random

class Level:

  def __init__(self, config):
    self.tiles = []
    self.width = config['width']
    self.height = config['height']
    self.room_settings = config['rooms']

  def generate(self, config):
    self.create_empty_tiles()
    generator = Generator()
    generator.generate_level(self, config)
    self.insert_rooms(generator.rooms)
    generator.generate_corridors()

  def create_empty_tiles(self):
    for x in range(0,self.width):
      self.tiles.append([])
      for y in range(0,self.height):
        self.tiles[x].append(None)
        tile = Tile(x,y)
        tile.set_type('empty')
        self.tiles[x][y] = tile

  def insert_rooms(self, rooms):
    for room in rooms:
      # self.insert_walls(room)
      for column in range (room.x, room.x + room.width):
        for row in range (room.y, room.y + room.height):
          self.tiles[column][row].set_type('floor')

  def insert_walls(self, room):
    x = room.x - 1
    y = room.y - 1
    width = room.width + 2
    height = room.height + 2
    for column in range (x, x + width):
      for row in range (y, y + height):
        self.tiles[column][row].set_type('wall')

  def get_odd_empty_tiles(self):
    odd_empty_tiles = []
    for column in range(0, self.width):
      for row in range(0, self.height):
        if self.tiles[column][row].empty() and self.tiles[column][row].odd():
          odd_empty_tiles.append(self.tiles[column][row])
    return odd_empty_tiles

  def draw(self, screen):
    for x in range(0,self.width):
      for y in range(0,self.height):
        self.tiles[x][y].draw(screen)


class Generator:

  def __init__(self):
    self.rooms = []

  def generate_level(self, level, config):
    self.level = level
    self.config = config
    self.generate_rooms()

  def generate_rooms(self):
    room_config = self.config['rooms']
    for attempt in range(0, room_config['generation_attempts']):
      room = self.generate_odd_sized_room(room_config)
      if (room.isolated_from_rooms(self.rooms) and room.within_level(self.level)):
        self.rooms.append(room)

  def generate_odd_sized_room(self, room_config):
    x = self.odd_number(0, self.config['width'])
    y = self.odd_number(0, self.config['height'])
    wd = self.odd_number(room_config['min_width'], room_config['max_width'])
    ht = self.odd_number(room_config['min_height'], room_config['max_height'])
    return Room(x, y, wd, ht)

  def generate_corridors(self):
    while len(self.level.get_odd_empty_tiles()) > 0:
      tiles = self.level.get_odd_empty_tiles()
      tree = [tiles[0]] # could start at a random instead
      self.generate_corridor(tiles, tree, tiles[0])

  def generate_corridor(self, tiles, tree, source_tile): #
    current_tile = source_tile
    while len(tree) > 0:
      neighbors = current_tile.get_neighbors(tiles)
      if len(neighbors) > 0:
        neighbor = neighbors[random.randint(0, len(neighbors)) - 1]
        self.connect_neighbors_as_corridor(current_tile, neighbor)
        current_tile = neighbor
        tree.append(current_tile)
      else:
        if current_tile.type is "empty":
          current_tile.type = "corridor"
        current_tile = tree.pop()

  def connect_neighbors_as_corridor(self, source_tile, target_tile): #
    source_tile.set_type("corridor")
    target_x = target_tile.location['x']
    target_y = target_tile.location['y']
    self.level.tiles[target_x][target_y].set_type("corridor")
    direction = target_tile.direction_from(source_tile)
    between_x = direction[0] + target_x
    between_y = direction[1] + target_y
    self.level.tiles[between_x][between_y].set_type("corridor")

  def odd_number(self, min_, max_):
    number = (random.randint(min_, max_))
    if (number % 2 is 0):
      return number + 1
    else:
      return number


class Room:

  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def collides_with_room(self, room):
    if (self.x > room.x + room.width or self.y > room.y + room.height):
      return False
    elif (self.x + self.width < room.x or self.y + self.height < room.y):
      return False
    else:
      return True

  def isolated_from_rooms(self, rooms):
      colliding_rooms = list(
          filter(lambda room: self.collides_with_room(room), rooms)
      )
      return (len(colliding_rooms) is 0)

  def within_level(self, level):
    return (self.x + self.width < level.width and
        self.y + self.height < level.height)

