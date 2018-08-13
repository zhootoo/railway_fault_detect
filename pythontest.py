state_path = 'D:/WorkSpace/PyCharm/Dalang/game_state.bin'
import pickle
import copyreg

class BetterGameState:
    def __init__(self,level=0,lives=90,hi=90):
        self.level = level
        self.lives = lives
        self.hi = hi

def pickle_game_state(game_state):
     kwargs = game_state.__dict__
     kwargs['version'] = 2
     print(kwargs)
     return unpickle_game_state,(kwargs,)

def unpickle_game_state(kwargs):
    print(kwargs)
    version = kwargs.pop('version',1)
    if version =='1':
        kwargs.pop('lives')
    print(kwargs)
    return BetterGameState(**kwargs)

if __name__=='__main__':
    copyreg.pickle(BetterGameState,pickle_game_state)
    with open(state_path,'rb') as f:
        state = pickle.load(f)
    print(state.__dict__)


