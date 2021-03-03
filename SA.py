# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 21:58:34 2020

@author: ElMousel
"""

from cvrp_algorithm import CVRPAlgorithm
import random
import copy
import heapq
import numpy

class SAPopulation(object):
    def __init__(self, info, total_iters):
        self.info = info
        self.info.max_route_len = 10
        self.neighbor = []
        for x in [self.info.steep_improve_solution(self.info.make_random_solution(greedy=True)) for _ in range(800)]:
            heapq.heappush(self.neighbor, (x.cost, x))
        self.best_solution = self.neighbor[0][1]
        self.iters = 0
        self.total_iters = total_iters
        self.same_route_prob = 0.25
        self.Ti = 5000
        self.alpha = 0.99
        self.T0 = self.Ti
        random.seed()

    def step(self):
        self.T0 = self.temperature(self.T0)
        old_sol = self.neighbor[0][1]
        self.info.refresh(old_sol)
        self.repairing(old_sol)
        self.info.refresh(old_sol)
        old_sol=copy.copy(old_sol)
        old_cost = old_sol.cost
        new_sol=copy.copy(old_sol)
        new_sol=self.biggest_overlap_crossover(new_sol,self.best_solution)
        self.info.refresh(new_sol)
        self.simple_random_mutation(new_sol)
        self.info.refresh(new_sol)
        self.repairing(new_sol)
        self.info.refresh(new_sol)
        self.info.steep_improve_solution(new_sol)
        self.info.refresh(new_sol)
        new_sol = copy.copy(new_sol)
        new_cost = new_sol.cost
        form_1 = self.acceptance_probability(old_cost,new_cost,self.T0)
        if new_cost <= old_cost:
            self.neighbor [0] = (self.fitness(new_sol),new_sol)
        elif random.uniform(0,1) < form_1 :
            self.neighbor [0] = (self.fitness(new_sol),new_sol)
        self.iters += 1
        if self.neighbor[0][1].cost < self.best_solution.cost:
            self.best_solution = self.neighbor[0][1]
        return self.best_solution
        #calc fitness
    def fitness(self, neighborr):
        penalty = self.penalty(neighborr)
        return neighborr.cost + penalty

    #calculates our penalty
    def penalty(self, neighborr):
        penalty_sum = 0
        for route in neighborr.routes:
            penalty_sum += max(0, route.demand - self.info.capacity)**2
        mnv = sum(self.info.demand[i] for i in range(self.info.dimension)) / self.info.capacity
        alpha = self.best_solution.cost / ((1 / (self.iters + 1)) * (self.info.capacity * mnv / 2)**2 + 0.00001)
        penalty = alpha * penalty_sum * self.iters / self.total_iters
        neighborr.penalty = penalty
        return penalty

    # returns true when a repair was needed, false otherwise
    def repairing(self, neighborr):
        routes = neighborr.routes
        r_max_i = max((i for i in range(len(routes))), key = lambda i: routes[i].demand)
        r_min_i = min((i for i in range(len(routes))), key = lambda i: routes[i].demand)
        if routes[r_max_i].demand > self.info.capacity:
            rint = random.randrange(1, len(routes[r_max_i].route) - 1)
            routes[r_min_i].append_node(routes[r_max_i].route[rint])
            routes[r_max_i].remove_node(routes[r_max_i].route[rint])
            return True
        return False
    def simple_random_mutation(self, chromosome):
        r_i = random.randrange(0, len(chromosome.routes))
        while(len(chromosome.routes[r_i].route) == 2):
            r_i = random.randrange(0, len(chromosome.routes))
        c_i = random.randrange(1, len(chromosome.routes[r_i].route) - 1)
        node = chromosome.routes[r_i].route[c_i]
        chromosome.remove_node(node)
        if random.uniform(0, 1) < self.same_route_prob:
            _, best = self.best_route_insertion([node], chromosome.routes[r_i].route)
            best_i = (r_i, best)
        else:
            r_r_i = r_i
            while r_i == r_r_i:
                r_r_i = random.randrange(0, len(chromosome.routes))
            _, best = self.best_route_insertion([node], chromosome.routes[r_r_i].route)
            best_i = (r_r_i, best)
        chromosome.insert_route(best_i[0], best_i[1], [node])
    def biggest_overlap_crossover(self, c1, c2):
        child = copy.deepcopy(c1)
        sub_route = c2.random_subroute()
        routes = []
        for x in sub_route:
            child.remove_node(x)
        for i, route in enumerate(child.routes):
            x_min, x_max, y_min, y_max = self.info.bounding_box(route.route)
            sx_min, sx_max, sy_min, sy_max = self.info.bounding_box(sub_route)
            x_overlap = max(0, min(x_max, sx_max) - max(x_min, sx_min))
            y_overlap = max(0, min(y_max, sy_max) - max(y_min, sy_min))
            heapq.heappush(routes, (x_overlap * y_overlap, i))
        top3 = heapq.nlargest(6, routes)
        min_i = min((i[1] for i in top3), key = lambda x: child.routes[x].demand)
        _, best = self.best_route_insertion(sub_route, child.routes[min_i].route)
        child.insert_route(min_i, best, sub_route)
        return child
    #finds the index where the route is best inserted
        
    def best_route_insertion(self, sub_route, route):
        start = sub_route[0]
        end = sub_route[-1]
        best_payoff, best_i = 0, 0
        dist = self.info.dist
        i = 0
        for i in range(0, len(route) - 1):
            init_cost = dist[route[i]][route[i + 1]]
            payoff = init_cost - dist[route[i]][start] - dist[end][route[i + 1]]
            if payoff > best_payoff:
                best_payoff, best_i = payoff, i
        return best_payoff, i
    def temperature (self,f):
        return (f * self.alpha)
    def acceptance_probability(self,cost, new_cost, t):
        if new_cost < cost :
            return 1
        else :
           return numpy.exp(-(new_cost - cost) / t)
class CVRPSA(CVRPAlgorithm):
    def __init__(self, info, num_populations, total_iters):
        super(CVRPSA, self).__init__(info)

        self.populations = [SAPopulation(self.info, total_iters) for _ in range(num_populations)]
        self.pop_bests = [0 for _ in range(num_populations)]
    def step(self):
        for i, pop in enumerate(self.populations):
            self.pop_bests[i] = pop.step()
        self.best_solution = min(self.pop_bests, key = lambda x: x.cost)
        return self.best_solution


if __name__ == "__main__":
    print("Run cvrp_runner instead")

    
    