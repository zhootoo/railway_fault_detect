from collections import namedtuple

ALIVE = '*'
EMPTY = '_'
TICK = object()

Query = namedtuple('Query',('y','x'))
Transition = namedtuple('Transition',('y','x','state'))
def count_neighbors(y,x):
    n_ = yield Query(y+1,x)#North
    ne = yield Query(y+1,x+1)#Northeast
    e_ = yield Query(y,x+1)#Eastern
    se = yield Query(y-1,x+1)#SouthEast
    s_ = yield Query(y-1,x)#South
    sw = yield Query(y-1,x-1)#Western
    w_ = yield Query(y,x-1)
    nw = yield Query(y+1,x-1)
    neighbor_states = [n_,ne,e_,se,s_,sw,w_,nw]
    count = 0
    for state in neighbor_states:
        if state ==ALIVE:
            count += 1
    return count

def step_cell(y,x):
    state = yield Query(y,x)
    neighbors = yield from count_neighbors(y,x)
    next_state = game_logic(state,neighbors)
    yield Transition(y,x,next_state)

def game_logic(state,neighbors):
    if state=='ALIVE':
        if neighbors<2:
            return EMPTY
        elif neighbors>3:
            return EMPTY
        else:
            if neighbors==3:
                return ALIVE
    return state

def simulate(height,width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y,x)
        yield TICK

class Grid:
    def __init__(self,height,width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY]*self.width)

    def __str__(self):
        result = ''
        for r in self.rows:
            result += ''.join(r)
            result += '\n'
        return result

    def query(self,y,x):
        return self.rows[y%self.height][x%self.width]

    def assign(self,y,x,state):
        self.rows[y%self.height][x%self.width] = state

def live_a_generation(grid,sim):
    progeny = Grid(grid.height,grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item,Query):
            state = grid.query(item.y,item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y,item.x,item.state)
            item = next(sim)
    return progeny

if __name__=='__main__':
    g = Grid(5,9)
    g.assign(0,3,ALIVE)
    g.assign(1,4,ALIVE)
    g.assign(2,2,ALIVE)
    g.assign(2,3,ALIVE)
    g.assign(2,4,ALIVE)
    print(g)
    sim=simulate(g.height,g.width)
    for i in range(5):
        g = live_a_generation(g,sim)
        print('————————')
        print(g)


