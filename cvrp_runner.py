from cvrp_info import CVRPInfo
from cvrp_advancedga import CVRPAdvancedGA
from GA_TS import CVRPGATS
from Whale import CVRPWhale
import os
import time
import signal
import sys

class CVRPRunner(object):

    def __init__(self, algorithm,  iterations):
        self.algorithm = algorithm
        self.print_cycle = 10
        self.num_iter = iterations
        #self.timings_file = open("timings/timings_{0}.txt".format(time.time()), "w")
        self.iter = 0
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        handling = True
        while handling:
            print("Iter:{0}\nPath:{1}\nWhat do? E for exec(), V for visualise, C to continue, S to save, X to exit".format(self.iter, self.best))
            c = raw_input()
            if c == "E":
                print("exec:")
                exec(raw_input())
            if c == "S":
                self.write_to_file("best-solution-{0}.part".format(self.iter))
            if c == "C":
                handling = False
            if c == "V":
                self.algorithm.info.visualise(self.best).show()
            elif c == "X":
                exit(0)

    def run(self):
        self.start_time = time.time()
        self.b_plt = []
        temp =200000
        self.opt_time = 0
        while self.iter < self.num_iter:
            best = self.algorithm.step()
            self.best = best
            self.b_plt += [self.best.cost]
            if self.best.cost < temp:
                temp = self.best.cost
                self.opt_time = time.time() - self.start_time
            if self.iter % self.print_cycle == 0:
                #self.timings_file.write("{0} at {1}s\n".format(best.cost, time.time() - self.start_time))
                print("iter : {0} best_cost : {1} ".format(self.iter, self.best.cost))
            self.iter += 1
            if time.time() - self.start_time > 1800 :
                self.write_to_file("best-solution-marking.txt")
                break
#            if self.iter % 10000:
#                 self.im = self.algorithm.info.visualise(self.algorithm.best_solution)
#                 self.im.save("images/"+str(self.algorithm.best_solution.cost) + ".png")
        itr_plt = list(range(0,self.iter))
        print("Best solution: \n" + str(best))
        print("Cost: " + str(best.cost))
        self.algorithm.info.visualise(self.best , self.b_plt , itr_plt)
        print("The Computational time is : ", self.opt_time)


    def write_to_file(self, file_name):
        text = os.linesep.join(["Name : Ahmed ElMousel",
                "Problem : X-n115-k10 ",
                "Whale Algorithm ",
                "cost : " + str(self.algorithm.best_solution.cost),
                "Routes : ",str(self.algorithm.best_solution),
                "best solutions : ",str(self.b_plt),
                "Computational time : " + str(self.opt_time -1)])
        with open(file_name, "w") as f:
            f.write(text)



if __name__ == "__main__":
    cvrp = CVRPRunner(CVRPWhale(CVRPInfo("validate/X-n190-k8.vrp", debug=True), 1, 200000), 200000)
    cvrp.run()
    cvrp.write_to_file("best-solution-marking.txt")
