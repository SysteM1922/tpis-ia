# Guilherme Antunes 103600
# Discutido com: Pedro Rasinhas 103541 e Gonçalo Silva 103668
# Outras fontes: Pesquisas gerais na internet mas nada de relevante a anotar

from tree_search import *
from cidades import *
from blocksworld import *


def func_branching(connections,coordinates):
    return sum([len([1 for con in connections if city in con]) for city in coordinates])/len(coordinates)-1

class MyCities(Cidades):
    def __init__(self,connections,coordinates):
        super().__init__(connections,coordinates)
        self.branching = func_branching(connections,coordinates)
        # ADD CODE HERE IF NEEDED

class MySTRIPS(STRIPS):
    def __init__(self,optimize=False):
        super().__init__(optimize)

    def simulate_plan(self,state,plan):
        for a in plan:
            state = self.result(state,a)
        return state

 
class MyNode(SearchNode):
    def __init__(self,state,parent,arg3=None,arg4=None,arg5=None):
        super().__init__(state,parent)
        self.cost = arg3
        self.heuristic = arg4
        self.depth = arg5

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',optimize=0,keep=0.25): 
        super().__init__(problem,strategy)
        self.problem = problem
        self.optimize = optimize
        self.keep = keep
        if optimize == 1:
            root = tuple((problem.initial,None,0,problem.domain.heuristic(problem.initial,problem.goal),0))
        elif optimize == 2 or optimize == 4:
            root = tuple((problem[1],None,0,problem[0][3](problem[1], problem[2]),0))
        else:
            root = MyNode(problem.initial,None,0,problem.domain.heuristic(problem.initial,problem.goal),0)
        self.all_nodes = [root]
        self.open_nodes = [0]
        #ADD HERE ANY CODE YOU NEED

    def astar_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        if self.optimize in [1,2,4]:
            self.open_nodes.sort(key=lambda e: self.all_nodes[e][3]+self.all_nodes[e][2])
        else:
            self.open_nodes.sort(key=lambda e: self.all_nodes[e].heuristic+self.all_nodes[e].cost)


    # remove a fraction of open (terminal) nodes
    # with lowest evaluation function
    # (used in Incrementally Bounded A*)
    def forget_worst_terminals(self):
        if self.optimize in [2,4]:
            avg_depth = sum([self.all_nodes[i][4] for i in self.open_nodes])/len(self.open_nodes)
            numKeep = int(self.keep*((self.problem[0][5]**(avg_depth+1)-1)/(self.problem[0][5]-1)))+1
        elif self.optimize == 1:
            avg_depth = sum([self.all_nodes[i][4] for i in self.open_nodes])/len(self.open_nodes)
            numKeep = int(self.keep*((self.problem.domain.branching**(avg_depth+1)-1)/(self.problem.domain.branching-1)))+1
        else:
            avg_depth = sum([self.all_nodes[i].depth for i in self.open_nodes])/len(self.open_nodes)
            numKeep = int(self.keep*((self.problem.domain.branching**(avg_depth+1)-1)/(self.problem.domain.branching-1)))+1
        self.open_nodes = self.open_nodes[:numKeep]

    # procurar a solucao
    def search2(self):
        visited_states = {}
        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]
            if self.optimize == 1:
                if self.problem.goal_test(node[0]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node[0]):
                    newstate = self.problem.domain.result(node[0],a)
                    if newstate not in self.get_path(node):
                        newnode = tuple((newstate,nodeID, node[2]+self.problem.domain.cost(node[0], (node[0], newstate)), self.problem.domain.heuristic(newstate, self.problem.goal), node[4]+1))
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            elif self.optimize in [2,4]:
                if self.problem[0][4](node[0], self.problem[2]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem[0][0](node[0]):
                    newstate = self.problem[0][1](node[0],a)
                    if newstate not in self.get_path(node):
                        newnode = tuple((newstate,nodeID, node[2]+self.problem[0][2](node[0], (node[0], newstate)), self.problem[0][3](newstate, self.problem[2]), node[4]+1))
                        if self.optimize == 4:
                            if newstate not in visited_states:
                                visited_states[newstate] = newnode
                            elif visited_states[newstate][2] > newnode[2]:
                                self.all_nodes.insert(self.all_nodes.index(visited_states[newstate]),newnode)
                                self.all_nodes.remove(visited_states[newstate])
                                visited_states[newstate] = newnode
                                continue
                            else:
                                continue
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            else:
                if self.problem.goal_test(node.state):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    if newstate not in self.get_path(node):
                        newnode = MyNode(newstate,nodeID, node.cost+self.problem.domain.cost(node.state, (node.state, newstate)), self.problem.domain.heuristic(newstate, self.problem.goal), node.depth+1)
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            if self.strategy == 'IBA*':
                self.forget_worst_terminals()
        return None

    def get_path(self, node):
        if self.optimize in [1,2,4]:
            if node[1] == None:
                return [node[0]]
            path = self.get_path(self.all_nodes[node[1]])
            path += [node[0]]
            return path
        else:
            return super().get_path(node)

# If needed, auxiliary functions can be added




