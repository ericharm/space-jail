import curses
import yaml
from src.game import Game

with open("config/config.yml", 'r') as stream:
  try:
    config = yaml.load(stream)
  except yaml.YAMLError as exc:
    print(exc)

def main(stdscr):
  game = Game(config)
  game.run(stdscr)

def init_curses():
  curses.initscr()
  curses.start_color()
  curses.curs_set(0)
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

init_curses()
curses.wrapper(main)

