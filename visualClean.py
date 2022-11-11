from cgi import test
import os
from pickle import FALSE
from random import Random, randint
import tarfile
# from tkinter import Menu
import util
from turtle import pos, width, window_height, window_width
import pygame as pg
# import pygame_menu
import sys
import time
pg.init()
info = pg.display.Info()
SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
window_width = 1200
window_height = 800
window = pg.display.set_mode((window_width, window_height))
columns = 50
rows = 50
grid_node_width = 1200 / columns
grid_node_height = 800 / rows
grid = []


# node class with draw method to visualize nodes and values to determine status of node in algorithm logic
class Node:
  def __init__(self, c, r):
      self.x = c
      self.y = r
      self.start = False
      self.wall = False
      self.target = False

      # values to be set by the user and used in search
      # values for controlling search
      self.visited = False
      self.queued = False
      # values for retracing shorfrontier path after found
      self.parent = None
      self.path = False
      # actions for checking surrounding nodes in search
      self.actions = []
      self.wall_prox = 0
  def draw(self, window, color, separation):
      pg.draw.rect(window, color, (self.x * grid_node_width, self.y * grid_node_height, grid_node_width-separation, grid_node_height-separation))
#  function for appending all legal actions to nodes
#  fills self.actions list
  def getActions(self):
      # get action to left (node neighbor) (if not in furthest column left)
      if (self.x > 0):
          self.actions.append(grid[self.x-1][self.y])

      # get action to right (node neighbor) (if not in furthest column right)
      if (self.x < columns -1):
          self.actions.append(grid[self.x+1][self.y])

      # down (if not at bottom row)
      if (self.y > 0):
          self.actions.append(grid[self.x][self.y-1])

      # up (if not at top row)
      if (self.y < rows-1):
          self.actions.append(grid[self.x][self.y+1])
        
    #   diagonals 
    # if in rightmost column, only have diagonals left 
    # if in top row, only have diagonals bottom 
    # if in bottom row, only have diagonals up 

    #   if (self.y < rows-1) and self.y > 0:
    #         if (self.x > 0 and self.x < columns - 1):
    #             if not grid[self.x][self.y+1].wall:
    #                 if not grid[self.x+1][self.y].wall:
    #                     self.actions.append(grid[self.x+1][self.y+1])
    #                 if not grid[self.x-1][self.y].wall: 
    #                     self.actions.append(grid[self.x-1][self.y+1])
    #             if not grid[self.x][self.y-1].wall:
    #                 if not grid[self.x-1][self.y].wall:
    #                     self.actions.append(grid[self.x-1][self.y-1])
    #                 if not grid[self.x+1][self.y].wall:
    #                     self.actions.append(grid[self.x+1][self.y-1])
            

      
  def coords(self):
      return (self.x, self.y)
      
# initialize graph of nodes
# grid of [columns][rows] filled with node in each
for c in range(columns):
  fill = []
  for r in range(rows):
      fill.append(Node(c, r))
  grid.append(fill)

# get actions for each node (iterate over all nodes and fill their actions list)
for c in range(columns):
            for r in range(rows):
                node = grid[c][r]
                node.getActions() 
     
   

def DFS(target, searching, frontier, startTime):
  if not frontier.isEmpty() and searching:
      curNode = frontier.pop()
      curNode.visited = True
      for action in curNode.actions:
          # next = action
              if not action.queued and not action.visited and action.wall == False:
                  action.queued = True
                  action.parent = curNode
                  frontier.push(action)
                  if action == target:
                      stop = time.perf_counter()
                      pathLength = 0
                      while curNode.start == False:
                          curNode.path = True
                          pathLength += 1
                          curNode = curNode.parent
                      runtime = str(stop - startTime)
                   #    print("Path found with length " + str(pathLength))
                   #    print("Path found in " + runtime[:6] + " seconds")
                      searching = False
                      return (runtime[:6], pathLength)
  pathLength = 0
  stop2 = time.perf_counter()
  runtime = str(stop2 - startTime)
  return (runtime[:6], pathLength)
  # return (runtime[:6], pathLength)


def euclideanDistance(c, r ,tr, cr):
 start = (c ,r)
 target = (tr, cr)
 return abs(start[0] - target[0]) + abs(start[1] - target[1])
 # return ( (start[0] - target[0]) ** 2 + (start[1] - target[1]) ** 2 ) ** 0.5


def A_star(target, searching, frontier, startTime):
  # create timer,
  pathCost = 0
  if not frontier.isEmpty() and searching:
      pathCost += 1
      curNode = frontier.pop()
      curNode.visited = True
      if curNode == target:
                      pathLength = 0
                      while curNode.start == False:
                          curNode.path = True
                          pathLength += 1
                          curNode = curNode.parent
                      stop = time.perf_counter()
                      runtime = str(stop - startTime)
                   #    print("Path found with length " + str(pathLength))
                   #    print("Path found by A* in " + runtime[:6] + " seconds")
                      searching = False
                      return (runtime[:6], pathLength)
      for action in curNode.actions:
          # next = action
              if not action.queued and not action.visited and action.wall == False:
                  action.queued = True
                  action.parent = curNode
                  frontier.push(action, pathCost + euclideanDistance(action.x, action.y, target.x, target.y))
  pathLength = 0
  stop2 = time.perf_counter()
  runtime = str(stop2 - startTime)
  return (runtime[:6], pathLength)


def UCS(target, searching, frontier, startTime):
  test_cost = 0
  if not frontier.isEmpty() and searching:
      curNode = frontier.pop()
      curNode.visited = True
      if curNode == target:
                      pathLength = 0
                      while curNode.start == False:
                          curNode.path = True
                          curNode = curNode.parent
                          pathLength += 1
                      stop = time.perf_counter()
                      runtime = str(stop - startTime)
                    #   print("Path found with length " + str(pathLength))
                    #   print("Path found by A* in " + runtime[:6] + " seconds")
                      searching = False
                      return (runtime[:6], pathLength)
      
      for action in curNode.actions:
          for a in action.actions:
           if a.wall == True:
              action.wall_prox += 1
          if action == target:
                      pathLength = 0
                      while curNode.start == False:
                          curNode.path = True
                          curNode = curNode.parent
                          pathLength += 1
                      stop = time.perf_counter()
                      runtime = str(stop - startTime)
                   #    print("Path found with length " + str(pathLength))
                   #    print("Path by RCS in " + runtime[:6] + " seconds")
                      searching = False
                      return (runtime[:6], pathLength)
          if not action.queued and not action.visited and action.wall == False:
                  action.queued = True
                  action.parent = curNode
                  frontier.push(action, test_cost)
                  test_cost += 1
                #   randint(0,2) - action.wall_prox + 1/euclideanDistance(action.x, action.y, curNode.x, curNode.y)
  pathLength = 0
  stop2 = time.perf_counter()
  runtime = str(stop2 - startTime)
  return (runtime[:6], pathLength)



def main():
  storage = []
#    storage to store all search results for an instance of the game
#    allows users to review and compare the empirical efficiency of algorithms without having to remember each specific run
#    holds more information than simply the eye test
#    will store, algorithm used, path length found, time found in, and the wall count for that run

  while True:
      start_set = False
      targetNode_set = False
 
      searching = True
   #    boolean for making search algorithms stop running when target is found
 
      begin_search = False
   #    boolean for controlling searching algorithms in main loop
 
      A_starr = False
      ucs = False
      result = False
 
      generate = False
   #    boolean for controlling maze gen
 
      display_mainmen = True
   #    boolean to control displaying main menu
 
      display_instruc = False
   #    boolean to control displaying instructions page
 
      display_vis = False
   #    boolean to control displaying visualizer
 
      display_stored = False
     
   
      pg.font.init()
      out = pg.font.SysFont('chalkboardse', 15)
      font = pg.font.SysFont('chalkboardse', 20)
      bigFont = pg.font.SysFont('chalkboardse', 40)
      hoverFont = pg.font.SysFont('chalkboardse', 40)
      hoverFont.set_underline(True)
      hoverFont.set_bold(True)
      headerFont = pg.font.SysFont('chalkboardse', 55)
   #    headerFont.set_bold(True)
      while display_mainmen and not display_instruc:
          window.fill((0, 0, 250))
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
          header = headerFont.render("Pathfinding Visualizer", True, (250,250,250), (0, 0, 250))
          header_cords = (window_width/2-header.get_width()/2, window_height/2-150)

        #   header = Button("Pathfinding Visualizer", headerFont, (250, 250,250), header_cords[0], header_cords[1], window)
        #   header.place()

          x = pg.mouse.get_pos()[0]
          y = pg.mouse.get_pos()[1]
          play = bigFont.render("Visualize!", True, (250, 250, 250))
          ins = bigFont.render("Instructions", True, (250, 250, 250))
          stor = bigFont.render("Search History", True, (250,250,250))
          aut = bigFont.render("Author", True, (250, 250, 250))
          qt = bigFont.render("Quit", True, (250,250, 250))
          if x - header_cords[0] <= play.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 100 and y < header_cords[1] + 100 +play.get_height():
               play = hoverFont.render("Visualize!", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= ins.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 175 and y < header_cords[1] + 175 +play.get_height():
               ins = hoverFont.render("Instructions", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= stor.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 250 and y < header_cords[1] + 250 +play.get_height():
               stor = hoverFont.render("Search History", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= aut.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 325 and y < header_cords[1] + 325+play.get_height():
               aut = hoverFont.render("Author", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= qt.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 400 and y < header_cords[1] + 400+play.get_height():
               qt = hoverFont.render("Quit", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
 
         
 
           
         
          window.blit(header, header_cords)
          window.blit(play, (header_cords[0], header_cords[1]+100))
          window.blit(ins, (header_cords[0], header_cords[1]+175))
          window.blit(stor, (header_cords[0], header_cords[1] + 250))
          window.blit(aut, (header_cords[0], header_cords[1] + 325))
          window.blit(qt, (header_cords[0], header_cords[1] + 400))
          pg.display.flip()
          for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  sys.exit()
              elif event.type == pg.MOUSEBUTTONDOWN:
                   if x - header_cords[0] <= play.get_width() and x - header_cords[0] >= 0:
                       if y >= header_cords[1] + 100 and y < header_cords[1] + 100 +stor.get_height():
                           display_instruc = False
                           display_mainmen = False
                           display_vis = True
                   if x - header_cords[0] <= ins.get_width() and x - header_cords[0] >= 0:
                       if y >= header_cords[1] + 175 and y < header_cords[1] + 175 +stor.get_height():
                           display_instruc = True
                           display_mainmen= False
                   if x - header_cords[0] <= stor.get_width() and x - header_cords[0] >= 0:
                       if y >= header_cords[1] + 250 and y < header_cords[1] + 250+stor.get_height():
                           display_stored = True
                           display_mainmen= False
                   if x - header_cords[0] <= qt.get_width() and x - header_cords[0] >= 0:
                       if y >= header_cords[1] + 400 and y < header_cords[1] + 400+play.get_height():
                           pg.quit()
                           sys.exit()
                 
                 
                 
                     
                 
      while display_instruc and not display_mainmen:
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
          window.fill((0,0,250))
          header = bigFont.render("Instructions", True, (250, 250, 250))
          header_cords = (window_width/2-header.get_width()/2, window_height/2-150)
          window.blit(header, header_cords)
          instructions = font.render("s key sets start node, t sets target node, hold click to create walls. ", True, (250,250, 250))
          instructions2 = font.render("press corresponding key after start or target set to reset ", True, (250, 250, 250))
          algos = font.render("d to use depth first search, b to use breadth first search. a to use a*, u to do a random cost search", True,(250, 250, 250))
          instructions3 = font.render("press r or w to reset search, w keeps walls. press c to clear the search", True, (250,250,250))
          click = font.render("press delete to return to main menu from any section", True, (250, 250, 250))
          window.blit(click, (window_width/2-click.get_width()/2, header_cords[1]+310))
          window.blit(instructions, (window_width/2-instructions.get_width()/2, header_cords[1]+100))
          window.blit(instructions2, (window_width/2-instructions2.get_width()/2, header_cords[1]+155))
          window.blit(algos, (window_width/2-algos.get_width()/2, header_cords[1]+210))
          window.blit(instructions3,  (window_width/2-instructions3.get_width()/2, header_cords[1]+265))
          pg.display.flip()
          for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  sys.exit()
              elif event.type == pg.KEYDOWN:
                  if event.key == pg.K_BACKSPACE:
                   display_mainmen = True
                   display_instruc = False
 
 
      while display_stored and not display_mainmen:
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
          window.fill((0, 0,250))
          yCord = -10
          search_count = 1
          if len(storage) == 0:
              no_hist = font.render("No searches have been completed yet", True, (250,250,250))
              yCord += no_hist.get_height()
              window.blit(no_hist, (10, yCord))
          for res in storage:
              toDisp = font.render(str(search_count) + ". " +  res[0] + " | Length: " + str(res[1]) + " | Time: " + str(res[2]) + " | Wall Count: " + str(res[3]), True, (250,250,250))
              yCord += toDisp.get_height()
              search_count += 1
              window.blit(toDisp, (10, yCord))
               # print(res[0] + " Length: " + str(res[1]) + " Time: " + str(res[2]) + " Wall Count: " + str(res[3]))
          pg.display.flip()
          for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  sys.exit()
              elif event.type == pg.KEYDOWN:
                  if event.key == pg.K_BACKSPACE:
                       display_mainmen = True
                       display_stored = False
         
 
 
      while not display_instruc and not display_mainmen and display_vis:
        #   pg.mouse.set_cursor(pg.cursors.diamond)
          pg.mouse.set_cursor(pg.cursors.arrow)

        # create buttons for doing searches 
          op_buttons = []

          dfsB = font.render("DFS", True, (250, 250, 250))
          op_buttons.append(dfsB)
          aStarB = font.render("A*", True, (250, 250, 250))
          op_buttons.append(aStarB)
          bfsB = font.render("BFS", True, (250,250,250))
          op_buttons.append(bfsB)
          rB = font.render("Reset", True, (250,250, 250))
          op_buttons.append(rB)
          navX = pg.mouse.get_pos()[0]
          navY = pg.mouse.get_pos()[1]

          if navX - 10 <= dfsB.get_width() and navX - 10 >= 0:
              if navY >= window_height/2-(window_height/4) and navY < window_height/2-(window_height/4) + dfsB.get_height():
               dfsB = hoverFont.render("Visualize!", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= ins.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 175 and y < header_cords[1] + 175 +play.get_height():
               ins = hoverFont.render("Instructions", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= stor.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 250 and y < header_cords[1] + 250 +play.get_height():
               stor = hoverFont.render("Search History", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= aut.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 325 and y < header_cords[1] + 325+play.get_height():
               aut = hoverFont.render("Author", True, (250,250,250))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        #   if x - header_cords[0] <= qt.get_width() and x - header_cords[0] >= 0:
        #        if y >= header_cords[1] + 400 and y < header_cords[1] + 400+play.get_height():
        #        qt = hoverFont.render("Quit", True, (250,250,250))
        #        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

        

          for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  sys.exit()
              elif event.type == pg.MOUSEMOTION:
                  
                  x = pg.mouse.get_pos()[0]                 
                  y = pg.mouse.get_pos()[1]
                  c = int (x/grid_node_width)
                  r = int (y/grid_node_height)
                  if event.buttons[0]:
                      grid[c][r].wall = True
                  if event.buttons[2]:
                      grid[c][r].wall = False
              elif event.type == pg.KEYDOWN:
                  if event.key == pg.K_BACKSPACE:
                       display_instruc = True
                       start_set = False
                       targetNode_set = False
                       searching = True
                       begin_search = False
                       A_starr = False
                       ucs = False
                       result = False
                       generate = False
                       start = None
                       target = None
                       frontier = None
                       for c in range(columns):
                          for r in range(rows):
                              node = grid[c][r]
                              node.start = False
                              node.wall = False
                              node.target = False
                              # values to be set by the user and used in search
                              # values for controlling search
                              node.visited = False
                              node.queued = False
                              # values for retracing shorfrontier path after found
                              node.parent = None
                              node.path = False
                   #    modify this so bug where going to mainmen and coming back requires reset before search (make it auto reset)
                  
                  x = pg.mouse.get_pos()[0]
                  y = pg.mouse.get_pos()[1]
                  c = int (x/grid_node_width)
                  r = int (y/grid_node_height)
                  if event.key == pg.K_s and not start_set and not grid[c][r].wall:
                      start_cords = (c, r)
                      start = grid[c][r]
                      start.start = True
                      start.visited = True
                      start_set = True
                      # frontier.append(start)
                      # fifo.put(start)
                  elif event.key == pg.K_s and start_set:
                      start.start = False
                      start_set = False
                      start.visited = False
                      start = None
                      start_cords = None
                  if event.key == pg.K_t and not targetNode_set and not grid[c][r].wall:
                      target_cords = (c, r)
                      target = grid[c][r]
                      target.target = True
                      targetNode_set = True
                  elif event.key == pg.K_t and targetNode_set:
                      target.target = False
                      targetNode_set = False
                      target = None
                      target_cords = None
                  if event.key == pg.K_d and start_set and targetNode_set:
                      begin_search = True
                      A_starr = False
                      ucs = False
                      frontier = util.Stack()
                      frontier.push(start)
                      startTime = time.perf_counter()
                      alg = "DFS"
                  if event.key == pg.K_b and start_set and targetNode_set:
                      begin_search = True
                      A_starr = False
                      ucs = False
                      frontier = util.Queue()
                      frontier.push(start)
                      startTime = time.perf_counter()
                      alg = "BFS"
                  if event.key == pg.K_a and start_set and targetNode_set:
                      begin_search = True
                      frontier = util.PriorityQueue()
                      frontier.push(start, 0)
                      A_starr = True
                      startTime = time.perf_counter()
                  if event.key == pg.K_u and start_set and targetNode_set:
                      begin_search = True
                      A_starr = False
                      frontier = util.PriorityQueue()
                      frontier.push(start, 0)
                      ucs = True
                      startTime = time.perf_counter()
                  if event.key == pg.K_r:
                      result = False
                      start_set, targetNode_set = False, False
                      start = None
                      target = None
                      frontier = None
                      for c in range(columns):
                          for r in range(rows):
                              node = grid[c][r]
                              node.start = False
                              node.wall = False
                              node.target = False
                              # values to be set by the user and used in search
                              # values for controlling search
                              node.visited = False
                              node.queued = False
                              # values for retracing shorfrontier path after found
                              node.parent = None
                              node.path = False
                  if event.key == pg.K_w:
                      result = False
                      start_set, targetNode_set = False, False
                      start = None
                      target = None
                      frontier = None
                      for c in range(columns):
                          for r in range(rows):
                              node = grid[c][r]
                              node.start = False
                              node.target = False
                              # values to be set by the user and used in search
                              # values for controlling search
                              node.visited = False
                              node.queued = False
                              # values for retracing shorfrontier path after found
                              node.parent = None
                              node.path = False
                  if event.key == pg.K_c:
                     result = False
                     frontier = None
                     for c in range(columns):
                         for r in range(rows):
                             node = grid[c][r]
                             # node.start = False
                             # node.target = False
                             # values to be set by the user and used in search
                             # values for controlling search
                             node.visited = False
                             node.queued = False
                             # values for retracing shorfrontier path after found
                             node.parent = None
                             node.path = False
                  if event.key == pg.K_m:
                      start_set, targetNode_set = False, False
                      start = None
                      target = None
                      frontier = None
                      count = 0
                      for c in range(columns):
                          for r in range(rows):
                              node = grid[c][r]
                              node.start = False
                              node.wall = True
                              node.target = False
                              # values to be set by the user and used in search
                              # values for controlling search
                              node.visited = False
                              node.queued = False
                              # values for retracing shorfrontier path after found
                              node.parent = None
                              node.path = False
                      generate = True
                      frontier = util.PriorityQueue()
                      # randX = randint(0, 59)
                      # randY = randint(0, 49)
                      # targX = randint(0, 59)
                      # targY = randint(0, 49)
                      start = grid[0][0]
                      target = grid[49][49]
                      startTime = 0
                      frontier.push(start, 0)
          if begin_search and frontier and not A_starr and not ucs:
              # depending on inputted frontier, will be either DFS or BFS; for DFS uses Stack for frontier, for BFS uses Queue
              toprint = DFS(target, searching, frontier, startTime)
            #   toprint = IDDDS(target, searching, frontier, startTime)
          elif begin_search and frontier and A_starr:
              toprint = A_star(target, searching, frontier, startTime)
              alg = "A*"
          elif begin_search and frontier and ucs:
              toprint = UCS(target, searching, frontier, startTime)
              alg = 'RCS'
       
          
          window.fill((0,0, 250))
          y_placement = (window_width*.20)
          for button in op_buttons:
              window.blit(button, (y_placement, 35))
              y_placement += (window_width*.20)
          
          pathC = 0
          wallCount = 0
        
          

        #   surf for grid (used to have nav tab on left)
          gridsurf = pg.Surface((1200, 800))
          gridsurf.fill((250, 0,0 ))
          
          for c in range(columns):
              for r in range(rows):
                  node = grid[c][r]
                  node.draw(gridsurf, (250, 250, 250), 1)
                  if node.wall == True:
                      node.draw(gridsurf, (0, 0, 0), 1)
                      wallCount += 1
                  if node.start == True:
                      node.draw(gridsurf, (255,255, 0), 1)
                  if node.target == True:
                      node.draw(gridsurf, (250, 0, 0), 1)
                  if node.queued == True:
                      node.draw(gridsurf, (200, 140, 130), 1)
                  if not node.start and node.visited == True:
                      node.draw(gridsurf, (0, 0, 250), 1)
                  if node.path == True:
                      node.draw(gridsurf, (250,0, 0), 1)
                      begin_search = False
                      pathC += 1

                      result = True
          
          window.blit(gridsurf, (0, 0))


          if result == True:
           #    alg, length, time, wallCount format
           #
              res = (alg, toprint[1], toprint[0], wallCount)
              if not storage.__contains__(res):
                  storage.append(res)
                  print()
                  for res in storage:
                      print(res[0] + " Length: " + str(res[1]) + " Time: " + str(res[2]) + " Wall Count: " + str(res[3]))
              sol = out.render(alg + " path found with length " + str(toprint[1]), True, (250, 250, 250), (0,0,250))
              tm = out.render("Found in " + str(toprint[0] + " seconds"), True, (250, 250, 250 ), (0,0, 250))
              window.blit(sol, (window_width/2-sol.get_width()/2, 0))
              window.blit(tm, (window_width/2-tm.get_width()/2, 22))
              result = False
         
          pg.display.flip()
       
main()
# print(pg.font.get_fonts())
 
 
 
 
 
 