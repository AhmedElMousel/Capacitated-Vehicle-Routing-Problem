import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import itertools as itr
import scipy.spatial.distance as ssd
import ObjectFun as OB

### --> DYNAMIC TABU LIST WITH ASPIRATION BEST SO FAR and MULTI-RESTART WITH MUTATION <-- ###
### Returns back to the best-so-far after some iterations

print()
print("DYNAMIC TABU LIST WITH ASPIRATION BEST SO FAR and MULTI-RESTART WITH MUTATION ")

# X coordinates
X_Coordinations = np.array([82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 96, 50, 49, 13, 29, 58, 84, 14, 2, 3, 5,
                            98, 84, 61, 1, 88, 91, 19, 93, 50, 98, 5, 42, 61, 9, 80, 57, 23, 20, 85, 98])

# Y coordinates
Y_Coordinations = np.array([76, 76, 76, 76, 76, 76, 76, 76, 76, 76, 44, 5, 8, 7, 89, 30, 39, 24, 39, 82, 10,
                            52, 25, 59, 65, 51, 2, 32, 3, 93, 14, 42, 9, 62, 97, 55, 69, 15, 70, 60, 5])

# Stack them on top of each other
X_Y_Coordinations = np.column_stack((X_Coordinations, Y_Coordinations))

# Create a distance matrix from the Euclidean distance
Distance_Matrix = ssd.cdist(X_Y_Coordinations, X_Y_Coordinations, 'euclidean')

Capacities = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8, 14, 21, 16, 3, 22, 18,
                       19, 1, 24, 8, 12, 4, 8, 24, 24, 2, 20, 15, 2, 14, 9])

# Create a distance dataframe
Dist_Dataframe = pd.DataFrame(Distance_Matrix, columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                                        14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                                                        25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
                                                        36, 37, 38, 39, 40, 41],
                              index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                     14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                                     25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
                                     36, 37, 38, 39, 40, 41])
# Create a capacity dataframe
Cap_Dataframe = pd.DataFrame(Capacities,
                             columns=["Capacity"], index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                                          14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                                                          25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
                                                          36, 37, 38, 39, 40, 41])

# Initial solution to start with
X0 = [24, 26, 22, 31, 11, 16, 25, 30, 34, 12, 14, 1, 20, 39, 15, 5, 36, 13, 18, 19, 32,
      38, 28, 10, 9, 23, 33, 21, 7, 4, 40, 35, 2, 17, 8, 6, 37, 3, 29, 27, 41]

### For Documentation ###
Initial_For_Final = [24, 26, 22, 31, 11, 16, 25, 30, 34, 12, 14, 1, 20, 39, 15, 5, 36, 13, 18, 19, 32,
                     38, 28, 10, 9, 23, 33, 21, 7, 4, 40, 35, 2, 17, 8, 6, 37, 3, 29, 27, 41]
rnd_sol_1 = X0[:]
P_Mutation = 0.2

Total_Distance_Initial = OB.Complete_Distance_Not_Random(rnd_sol_1)
print " Total Initial Distance :", Total_Distance_Initial
T0 = 2000
M = 1000
N = 100
Alpha = 0.9


# For visualization
Temp = []
Min_Distance = []
for i in range(M):
    print "The Iteration : ",i
    for j in range(N):
        # To generate random integers in order to swap cities
        Random_1 = np.random.rand()  # Take a random number to mutate
        Xtemp = []
        if Random_1 <= P_Mutation:  # Probablity is less than the probablity of mutation
            '''
            if Mod_Iterations == 0:
            '''
            Mutated_Solution_in_Hand = []

            # ["2000","2","5","6","9","1"]

            Ran_Mut_1 = np.random.rand()  # Probablity to Mutate
            Ran_Mut_2 = np.random.randint(1, len(X0) + 1)  # Random integer in the length of the solution
            Ran_Mut_3 = np.random.randint(1, len(X0) + 1)

            A1 = Ran_Mut_2  # A1 is a random integer
            A2 = Ran_Mut_3  # A2 is a random integer

            while A1 == A2:
                A2 = np.random.randint(1, len(X0) + 1)  # If A1 is equal to A2, repeat

            if A1 < A2:  # If A1 comes before A2
                A2 = A2 + 1
                Rev_1 = X0[:]
                Rev_2 = list(reversed(X0[A1:A2]))  # Reverse the order
                t = 0
                for i in range(A1, A2):
                    Rev_1[i] = Rev_2[t]
                    t = t + 1

                Mutated_Solution_in_Hand = Rev_1[:]

            else:
                A1 = A1 + 1
                Rev_1 = X0[:]
                Rev_2 = list(reversed(X0[A2:A1]))  # Reverse the order
                t = 0
                for i in range(A2, A1):
                    Rev_1[i] = Rev_2[t]
                    t = t + 1

                Mutated_Solution_in_Hand = Rev_1[:]

            Ran_1 = np.random.randint(1, len(X0) + 1)  # Random integers in length of solution
            Ran_2 = np.random.randint(1, len(X0) + 1)
            Ran_3 = np.random.randint(1, len(X0) + 1)
            Ran_4 = np.random.randint(1, len(X0) + 1)

            Xt = []
            A1 = Mutated_Solution_in_Hand[Ran_1]  # Get a random integer in the mutated solution
            A2 = Mutated_Solution_in_Hand[Ran_2]  # Get a random integer in the mutated solution

            # Making a new list of the new set of nodes
            T_Temp = Mutated_Solution_in_Hand

            w = 0
            for i in T_Temp:
                if T_Temp[w] == A1:
                    Xt = np.append(Xt, A2)
                elif T_Temp[w] == A2:
                    Xt = np.append(Xt, A1)
                else:
                    Xt = np.append(Xt, T_Temp[w])
                w = w + 1

            Mutated_Solution_in_Hand = Xt

            # Same nodes gets switched

            Xt = []
            A1 = Mutated_Solution_in_Hand[Ran_1]
            A2 = Mutated_Solution_in_Hand[Ran_3]

            # Making a new list of the new set of nodes
            w = 0
            for i in Mutated_Solution_in_Hand:
                if Mutated_Solution_in_Hand[w] == A1:
                    Xt = np.append(Xt, A2)
                elif Mutated_Solution_in_Hand[w] == A2:
                    Xt = np.append(Xt, A1)
                else:
                    Xt = np.append(Xt, Mutated_Solution_in_Hand[w])
                w = w + 1
            Xtemp=Xt
            Xtemp = list(Xtemp)
            Cost_X0 = OB.Complete_Distance_Not_Random(X0)
            P1_X0 = OB.Penalty_1(X0,1000)
            P2_X0 = OB.Penalty_2(X0,600,400)
            P3_X0 = OB.Penalty_3(X0, 400)
            Len_X0 = Cost_X0 + P1_X0 + P2_X0 + P3_X0

            Cost_Xtemp = OB.Complete_Distance_Not_Random(Xtemp)
            P1_Xtemp = OB.Penalty_1(Xtemp, 1000)
            P2_Xtemp = OB.Penalty_2(Xtemp, 600, 400)
            P3_Xtemp = OB.Penalty_3(Xtemp, 400)
            Len_Xtemp = Cost_Xtemp + P1_Xtemp + P2_Xtemp + P3_Xtemp

            rand_num = np.random.rand()  # RN for the formula below
            form_1 = 1 / (np.exp((Len_Xtemp - Len_X0) / T0))  # The formula to accept moves

            if Len_Xtemp <= Len_X0:  # If the OF of the potential solution was better (less)
                X0 = Xtemp

            elif rand_num <= form_1:  # If the RN was less than the formula
                X0 = Xtemp

            else:  # Don't accept the potential solution and stay where you are
                X0 = X0
    Temp = np.append(Temp, T0)  # Append temps. for visualization
    Min_Distance = np.append(Min_Distance, Len_Xtemp)  # Append costs for visualization
    T0 = Alpha * T0  # Decrease the temp
Without_Penalty_Cost = OB.Complete_Distance_Not_Random(X0)
print
print
print "Final Solution is: "
for i in range(len(X0)):
    print X0[i]
print "Minimized Distance at Final Solution is: ", Len_X0
print("The Lowest Distance Without Penalties is:", Without_Penalty_Cost)
plt.plot(Temp, Min_Distance)
plt.title("Distance vs. Temperature", fontsize=20, fontweight='bold')
plt.xlabel("Temperature", fontsize=18, fontweight='bold')
plt.ylabel("Distance", fontsize=18, fontweight='bold')
plt.xlim(2000, 0)
plt.xticks(np.arange(min(Temp), max(Temp), 100), fontweight='bold')
plt.yticks(fontweight='bold')
plt.show()
