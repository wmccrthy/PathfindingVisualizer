
import util
import pygame as pg
import random
import sys
import time
pg.init()
# info = pg.display.Info()
# SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
window_width = 1000
window_height = 800
window = pg.display.set_mode((window_width, window_height))
columns = 40
rows = 40
grid_node_width = window_width / columns
grid_node_height = window_height / rows
grid = []

out = pg.font.SysFont('chalkboardse', 15)
pg.display.set_caption("Pathfinding Visualizer")


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

      self.weight = 0

  def reset(self):
    #   reset nodes when switching between searches, etc
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
      self.weight = 0
  
  def resetSearch(self):
      self.visited = False
      self.queued = False
      # values for retracing shorfrontier path after found
      self.parent = None
      self.path = False

  def draw(self, window, color, separation):
      navX = pg.mouse.get_pos()[0]
      navY = pg.mouse.get_pos()[1]
      width = 0
      border_rad = 0
      if abs(navX - (self.x*grid_node_width+(grid_node_width/2))) < grid_node_width/2.25 and abs(navY - (self.y * grid_node_height)-grid_node_height/2) < grid_node_height/2.25:
          if color == (0,0,0):
              shade = (50,70,70)
          else:
              shade = ((color[0]*7/8, color[1]*7/8, color[2]*7/8))
          color = (50,50,50)
          pg.draw.rect(window, shade, (self.x * grid_node_width, self.y * grid_node_height, grid_node_width-separation, grid_node_height-separation), border_radius=2)
          width = 1
          border_rad = 2
      pg.draw.rect(window, color, (self.x * grid_node_width, self.y * grid_node_height, grid_node_width-separation, grid_node_height-separation), width=width, border_radius=border_rad)
    #   pg.draw.aaline()
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
                      action.path = True
                      stop = time.perf_counter()
                      pathLength = 0
                      while curNode.start == False:
                          curNode.path = True
                          pathLength += 1 + curNode.weight
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

def DLS(target, searching, frontier, cutoff, startTime):
    nodesChecked = 0 
    depth = 0
    if not frontier.isEmpty() and searching:
        if depth == cutoff:
            searching = False
            return cutoff
        curNode = frontier.pop()
        curNode.visited = True
        for action in curNode.actions:
          # next = action
              if not action.queued and not action.visited and action.wall == False:
                  action.queued = True
                  action.parent = curNode
                  frontier.push(action)
                  nodesChecked += 1
                  if nodesChecked == 4:
                      depth += 1
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
def IDDDS(target, searching, frontier, startTime):
    for c in range(1, 99999):
        res = DLS(target, searching, frontier, c, startTime)
        if res != c:
            return res

def mazeGen(frontier, count): 

    if len(frontier) > 0:
        # print("working")
        curWall = random.choice(frontier)
        curWall.visited = True
        count += 1
        visCount = 0
        for action in curWall.actions:
            if action.visited:
                visCount += 1
                action.wall = False
                # frontier.append(action)
                count += 1
        if visCount == 1 or 3:
            curWall.wall = False
            frontier.remove(curWall)

def mazeGen2(frontier, count): 
    
    if len(frontier) > 0:
        # print("working")
        curWall = random.choice(frontier)
        curWall.visited = True
        count += 1
        visCount = 0
        for action in curWall.actions:
            if action.wall:
                frontier.append(action)
            if action.visited:
                visCount += 1
                # action.wall = False
                # count += 1

        if visCount == 1 or 0:
            curWall.wall = False
            frontier.remove(curWall)
    
                    


def euclideanDistance(c, r ,tr, cr):
 "The Euclidean distance heuristic for a PositionSearchProblem"
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
                          pathLength += curNode.weight
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
                  frontier.push(action, pathCost + euclideanDistance(action.x, action.y, target.x, target.y) + action.weight)
  pathLength = 0
  stop2 = time.perf_counter()
  runtime = str(stop2 - startTime)
  return (runtime[:6], pathLength)


def Dijkstra(target, searching, frontier, startTime):
  pathCost = 0
  if not frontier.isEmpty() and searching:
      pathCost += 1
    #   curNode = random.choice(frontier)
    #   frontier.remove(curNode)
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
                          pathLength += curNode.weight
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
                #   frontier.append(action)
                  frontier.push(action, action.weight + pathCost)
                  
                #   randint(0,2) - action.wall_prox + 1/euclideanDistance(action.x, action.y, curNode.x, curNode.y)
  pathLength = 0
  stop2 = time.perf_counter()
  runtime = str(stop2 - startTime)
  return (runtime[:6], pathLength)
def uniform():
  return 1
def main():
  storage = []
#    storage to store all search results for an instance of the game
#    allows users to review and compare the empirical efficiency of algorithms without having to remember each specific run
#    holds more information than simply the eye test
#    will store, algorithm used, path length found, time found in, and the wall count for that run
  while True:
      seeNode = True
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

      while display_mainmen and not display_instruc:
          window.fill((250, 250, 250))
          pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
          pg.mouse.set_visible(False)
          pg.draw.circle(window, (0,0,0),  (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]), 3, width=1)
          header = headerFont.render("Pathfinding Visualizer", True, (0,0,0))
          header_cords = (window_width/2-header.get_width()/2, window_height/2-150)

          x = pg.mouse.get_pos()[0]
          y = pg.mouse.get_pos()[1]
          play = bigFont.render("Visualize!", True, (0, 0, 0))
          ins = bigFont.render("Instructions", True, (0, 0, 0))
          stor = bigFont.render("Search History", True, (0,0,0))
          aut = bigFont.render("Author", True, (0, 0, 0))
          qt = bigFont.render("Quit", True, (0,0, 0))
          if x - header_cords[0] <= play.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 100 and y < header_cords[1] + 100 +play.get_height():
               play = hoverFont.render("Visualize!", True, (0,0,0))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= ins.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 175 and y < header_cords[1] + 175 +play.get_height():
               ins = hoverFont.render("Instructions", True, (0,0,0))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= stor.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 250 and y < header_cords[1] + 250 +play.get_height():
               stor = hoverFont.render("Search History", True, (0,0,0))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= aut.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 325 and y < header_cords[1] + 325+play.get_height():
               aut = hoverFont.render("Author", True, (0,0,0))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= qt.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 400 and y < header_cords[1] + 400+play.get_height():
               qt = hoverFont.render("Quit", True, (0,0,0))
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
          window.fill((250,250,250))
          header = bigFont.render("Instructions", True, (0, 0, 0))
          header_cords = (window_width/2-header.get_width()/2, window_height/2-150)
          window.blit(header, header_cords)
          instructions = font.render("s key sets start node, t sets target node, hold click to create walls. ", True, (0,0, 0))
          instructions2 = font.render("press corresponding key after start or target set to reset ", True, (0, 0, 0))
          algos = font.render("d to use depth first search, b to use breadth first search. a to use a*, u to do dijkstras", True,(0, 0, 0))
          instructions3 = font.render("press r or c to reset search, c keeps walls. press m to generate a maze", True, (0, 0, 0))
          click = font.render("press delete to return to main menu from any subpage", True, (0, 0, 0))
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
          window.fill((250, 250,250))
          yCord = -10
          search_count = 1
          if len(storage) == 0:
              no_hist = font.render("No searches have been completed yet", True, (0,0,0))
              yCord += no_hist.get_height()
              window.blit(no_hist, (10, yCord))
          for res in storage:
              toDisp = font.render(str(search_count) + ". " +  res[0] + " | Length/Cost: " + str(res[1]) + " | Time: " + str(res[2]) + " | Wall Count: " + str(res[3]), True, (0,0,0))
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
          pg.mouse.set_visible(False) 
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
               dfsB = hoverFont.render("Visualize!", True, (0,0,0))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= ins.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 175 and y < header_cords[1] + 175 +play.get_height():
               ins = hoverFont.render("Instructions", True, (0,0,0))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= stor.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 250 and y < header_cords[1] + 250 +play.get_height():
               stor = hoverFont.render("Search History", True, (0,0,0))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
          if x - header_cords[0] <= aut.get_width() and x - header_cords[0] >= 0:
              if y >= header_cords[1] + 325 and y < header_cords[1] + 325+play.get_height():
               aut = hoverFont.render("Author", True, (0,0,0))
               pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

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
                              node.reset()
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
                    #   frontier = []
                      frontier = util.PriorityQueue()
                      frontier.push(start, 1)
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
                              node.reset()
                  if event.key == pg.K_l:
                    for c in range(columns):
                        for r in range(rows):
                            node = grid[c][r]
                            randInt = random.randint(0, 11)
                            if randInt < 3 and not node.wall:
                                node.weight = random.randint(1,20)
                                # node.wall = True
                            elif not node.wall:
                                # node.wall = False
                                node.weight = 0
                  if event.key == pg.K_w:
                      x = pg.mouse.get_pos()[0]
                      y = pg.mouse.get_pos()[1]
                      c = int (x/grid_node_width)
                      r = int (y/grid_node_height)
                      noRep = 0
                      if noRep == 0:
                        grid[c][r].weight += 1
                      noRep += 1
                  if event.key == pg.K_q:
                      x = pg.mouse.get_pos()[0]
                      y = pg.mouse.get_pos()[1]
                      c = int (x/grid_node_width)
                      r = int (y/grid_node_height)
                      if grid[c][r].weight > 0:
                        grid[c][r].weight -= 1
                    
                  if event.key == pg.K_c:
                     result = False
                     frontier = None
                     for c in range(columns):
                         for r in range(rows):
                             node = grid[c][r]
                             node.resetSearch()
                  if event.key == pg.K_m:
                      start_set, targetNode_set = False, False
                      start = None
                      target = None
                      frontier = None
                      frontier = []
                      for c in range(columns):
                          for r in range(rows):
                              node = grid[c][r]
                              node.reset()
                              node.wall = True
                              frontier.append(node)
                      generate = True
                      startTime = 0
                  if event.key == pg.K_n:
                      if seeNode:
                          seeNode = False
                      else:
                          seeNode = True


          if begin_search and frontier and not A_starr and not ucs:
              # depending on inputted frontier, will be either DFS or BFS; for DFS uses Stack for frontier, for BFS uses Queue
              toprint = DFS(target, searching, frontier, startTime)
            #   toprint = IDDDS(target, searching, frontier, startTime)
          elif begin_search and frontier and A_starr:
              toprint = A_star(target, searching, frontier, startTime)
              alg = "A*"
          elif begin_search and frontier and ucs:
              toprint = Dijkstra(target, searching, frontier, startTime)
              alg = 'Dijkstras'
          elif generate:
              numVisited = 0
              for c in range(columns):
                    for r in range(rows):
                        node = grid[c][r]
                        if node.visited:
                            numVisited += 1
              toprint = mazeGen(frontier, startTime)
              if numVisited > 1050:
                  generate  = False
                  numVisited = 0
                  for c in range(columns):
                         for r in range(rows):
                             node = grid[c][r]
                             node.resetSearch()
       
          
          window.fill((0,0, 250))
          y_placement = (window_width*.20)
          for button in op_buttons:
              window.blit(button, (y_placement, 35))
              y_placement += (window_width*.20)
          
          pathC = 0
          wallCount = 0
        
        #   surf for grid (used to have nav tab on left)
          gridsurf = pg.Surface((1200, 800))
          gridsurf.fill((250, 250,250 ))
          
          for c in range(columns):
              for r in range(rows):
                  node = grid[c][r]
                  node.draw(gridsurf, (250, 250, 250), 0)
                  if node.weight > 0:
                    #   print(node.weight)
                      node.draw(gridsurf, (220-node.weight*5,220-node.weight*5,220-node.weight*5), 0)
                    #   make thing to display info abt node hovered over at top
                  if node.start == True:
                      node.draw(gridsurf, (0,205, 0), 0)
                  if node.target == True:
                      node.draw(gridsurf, (250, 0, 0), 0)
                  if node.queued == True:
                      node.draw(gridsurf, (200, 140, 130), 0)
                  if not node.start and node.visited == True:
                      if not generate:
                        node.draw(gridsurf, (0, 0, 250), 0)
                  if node.wall == True:
                      node.draw(gridsurf, (0, 0, 0), 0)
                      wallCount += 1
                  if node.path == True:
                      node.draw(gridsurf, (250,0, 0), 0)
                      begin_search = False
                      pathC += 1

                      result = True
                
          pg.draw.circle(gridsurf, (0,0,0),  (navX, navY), 3, width=1)
          pg.time.Clock().tick(360)


          window.blit(gridsurf, (0, 0))
          
          if seeNode:
            x = pg.mouse.get_pos()[0]
            y = pg.mouse.get_pos()[1]
            c = int (x/grid_node_width)
            r = int (y/grid_node_height)
            nodeInfo = out.render("Node Weight: " + str(grid[c][r].weight) +  " Node Position: " + str(grid[c][r].x) + ", " + str(grid[c][r].y), True, (0,0,0), (250,250,250))
            window.blit(nodeInfo, (window_width/2-nodeInfo.get_width()/2, 0))

        # display result on top of screen; fill storage w results of search; 
          if result == True:
           #    alg, length, time, wallCount format
              res = (alg, toprint[1], toprint[0], wallCount)
              if not storage.__contains__(res):
                  storage.append(res)
                  print()
                  for res in storage:
                      print(res[0] + " Length/Cost: " + str(res[1]) + " Time: " + str(res[2]) + " Wall Count: " + str(res[3]))
              sol = out.render(alg + " path found with length/cost " + str(toprint[1]), True, (250, 250, 250), (0,0,250))
              tm = out.render("Found in " + str(toprint[0] + " seconds"), True, (250, 250, 250 ), (0,0, 250))
              window.blit(sol, (window_width/2-sol.get_width()/2, 0))
              window.blit(tm, (window_width/2-tm.get_width()/2, 22))
              result = False
   
          pg.display.flip()
       
main()
 
 
 
 
 
 
