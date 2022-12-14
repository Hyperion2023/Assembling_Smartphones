from Core.Utils.Data import create_Environment
from Core import Agent
from Core.Astar.State import State
from Core.Astar.Astar import a_star
from Core.Astar.heuristic import *
from Core.Utils.Dijkstra import *
import time
from Core.Planner.Planner import Planner
import sys

if __name__ == "__main__":
    path = r"./Dataset/f_decentralized.txt"

    # state = State(None, 4)
    # state.get_children()

    env = create_Environment(path, district_size=50)
    #env.draw()
    boomer = Agent(env)
    #boomer.environment.show()
    boomer.deploy_arms("rand")
    boomer.assign_tasks()
    boomer.compute_paths()
    boomer.print_paths()

    print("DONE")
    # test=Planner(boomer.environment)
    # target=boomer.environment.districts[0][0].graphs[0].get_vertex(2)
    # Dpath = [target.get_id]
    # shortest(target,Dpath)
    #
    # print("The shortest path : %s", (Dpath[::-1]))
    # g=Graph()
    # g.create_graph_from_mat(boomer.environment.matrix)
    # print("Graph data:")
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print(vid, wid, v.get_weight(w))


    # list_of_graphs=create_graph_from_district(boomer.environment)
    # g=list_of_graphs[0]
    #
    #
    # print("# OF SUBGRAPHS: "+str(len(list_of_graphs)))
    # import time
    #
    # start = time.time()
    # dijkstra(g, g.get_vertex(1))
    # end = time.time()
    # print("Computing Djikstra: " + str(end - start))
    # target = g.get_vertex(14)
    # path = [target.get_id]
    # start = time.time()
    # shortest(target, path)
    # end = time.time()
    # print("Finding Path#1: " + str(end - start))
    # print("The shortest path : %s", (path[::-1]))
    #

    #boomer.running_workers[0].
    #starting_state = State(env.matrix, boomer.running_workers)

    #final_state = a_star(starting_state, goal_test, g, h)
    #boomer.run_plan(final_state.workers)
    # boomer.running_workers[0].my_description()
    # boomer.run_assembly()
