#encoding: utf8

# YOUR NAME: Guilherme Costa Antunes
# YOUR NUMBER: 103600

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT:
# - Gonçalo Silva 103668
# - Pedro Rasinhas 103541
# - Daniel Ferriera 102442

from semantic_network import *
from bayes_net import *
from constraintsearch import *

class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def is_object(self,user,obj):
        # IMPLEMENT HERE
        if [i for i in self.query_local(user=user) if type(i.relation) == Association and (i.relation.entity2 == obj or  i.relation.entity1 == obj) and not i.relation.card] + [i for i in self.query_local(user=user, e1=obj) if type(i.relation) == Member]:
            return True
        return False

    def is_type(self,user,type):
        # IMPLEMENT HERE
        query = [i for i in self.query_local(user=user, rel='subtype') if i.relation.entity2 == type or i.relation.entity1 == type] + [i for i in self.query_local(user=user)if isinstance(i.relation, Association) and i.relation.card and (i.relation.entity2 == type or i.relation.entity1 == type)]
        if query:
            return True
        return False

    def infer_type(self,user,obj,pos=None):
        # IMPLEMENT HERE
        if self.is_object(user, obj):
            for i in  self.query_local(user=user, e1=obj):
                if type(i.relation) == Member:
                    return i.relation.entity2
            if pos:
                if pos == 1:
                    for i in self.query_local(user=user, e2=obj):
                        if type(i.relation) == Association:
                            return self.infer_signature(user, i.relation.name)[1]
                else:
                    for i in self.query_local(user=user, e1=obj):
                        if type(i.relation) == Association:
                            return self.infer_signature(user, i.relation.name)[0]
                return '__unknown__'
            else:
                for i in self.query_local(user=user, e2=obj):
                    if type(i.relation) == Association:
                        return self.infer_signature(user, i.relation.name)[1]
                for i in self.query_local(user=user, e1=obj):
                    if type(i.relation) == Association:
                        return self.infer_signature(user, i.relation.name)[0]
        return None

 
    def infer_signature(self,user,assoc):
        # IMPLEMENT HERE
        query = [i for i in self.query_local(user=user, rel=assoc)]
        if query:
            arg1, arg2 = query[0].relation.entity1, query[0].relation.entity2
            if not self.is_type(user, arg1):
                arg1 = self.infer_type(user, arg1, 1)
            if not self.is_type(user, arg2):
                arg2 = self.infer_type(user, arg2, 2)
            return (arg1, arg2)
        return None


class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def markov_blanket(self,var):
        # IMPLEMENT HERE
        children = [i for i in self.dependencies if var in self.dependencies[i][0][0]]
        child_parents = [self.dependencies[i][0][0] for i in children]
        if child_parents:
            children += child_parents[0]
            children.remove(var)
        return list(set(self.dependencies[var][0][0] + children))
            

class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def propagate(self,domains,var):
        # IMPLEMENT HERE
        for edge0 in [i for i,e in self.constraints if e == var]:
            domain = [x for x in domains[edge0] if any(self.constraints[edge0, var](edge0, x, var, y) for y in domains[var])]
            if len(domain) < len(domains[edge0]):
                domains[edge0] = domain
                self.propagate(domains, edge0)

    def higherorder2binary(self, ho_c_vars, unary_c):
        # IMPLEMENT HERE
        def produto_cartesiano(domains, ho_c_vars):
            if ho_c_vars:
                return [(i,) + j for i in domains[ho_c_vars[0]] for j in produto_cartesiano(domains, ho_c_vars[1:])]
            return [()]

        def lambdas_func(i):
            return lambda x, y, z, w: w[i] == y, lambda x, y, z, w: y[i] == w

        aux = ''.join(ho_c_vars)
        self.domains[aux] = [i for i in produto_cartesiano(self.domains, ho_c_vars) if unary_c(i)]

        for (i,e) in enumerate(ho_c_vars):
            self.constraints[e, aux],self.constraints[aux, e]  = lambdas_func(i)

        



        


        


