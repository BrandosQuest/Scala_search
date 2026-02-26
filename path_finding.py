from operator import truediv

from search_problem import SearchProblem
from world import World

## Assume that:
# State is a pair (x,y)
# World is as defined in the imported class World, so has limits given by x_lim

class PathFinding(SearchProblem):
    def __init__(self, init, goal, world: World):
        self.actions = ['N','S','W','E']
        self.world = world
        super().__init__(init, goal, {a: 1 for a in self.actions})

    # Return all valid successors from `state` as:
    # {('N'|'S'|'W'|'E', (next_x, next_y)), ...}
    # Include only states that are inside limits and not in `self.world.walls`.
    def getSuccessors(self, state: tuple[int, int]) -> set[tuple[str, tuple[int, int]]]:#insieme di azioni stato
        #data una coordinata trova un set(insieme) che contiene 4 tuple contenenti stringa 'N'|'S'|'W'|'E' e la posizione futura
        #raise NotImplementedError("To be implemented")#da modicicare
        transitionModel = set()

        if self.isInTheLimits((state[0], state[1]+1)):
            nord= ('N', (state[0], state[1]+1))
            transitionModel.add(nord)
        # else:
        #     nord= ('N', (state[0], state[1]))

        if self.isInTheLimits((state[0], state[1]-1)):
            sud= ('S', (state[0], state[1]-1))
            transitionModel.add(sud)
        # else:
        #     sud= ('S', (state[0], state[1]))

        if self.isInTheLimits((state[0]-1, state[1])):
            west= ('W', (state[0]-1, state[1]))
            transitionModel.add(west)
        # else:
        #     west= ('W', (state[0], state[1]))

        if self.isInTheLimits((state[0]+1, state[1])):
            est= ('E', (state[0]+1, state[1]))
            transitionModel.add(est)
        # else:
        #     est= ('E', (state[0], state[1]))

        # transitionModel.add(nord)
        # transitionModel.add(sud)
        # transitionModel.add(west)
        # transitionModel.add(est)
        return transitionModel

    
    # Return True iff `state` is inside the world boundaries [0..x_lim] x [0..y_lim].
    def isInTheLimits(self, state: tuple[int, int]) -> bool:
        if state[0]>=0 and state[0]<=self.world.x_lim and state[1]>=0 and  state[1]<=self.world.y_lim:
            for t in self.world.walls:
               if state[0]==t[0] and state[1]==t[1]:
                   return False
            return True
        else:
            return False
        #raise NotImplementedError("To be implemented")#da modicicare
        
    # Return True iff `state` is the goal state (`self.goal`).
    def isGoal(self, state: tuple[int, int]) -> bool:
        if state[0]==self.goal[0] and state[1]==self.goal[1]:
            return True
        else:
            return False
        #raise NotImplementedError("To be implemented")#da modicicare


#da modificare