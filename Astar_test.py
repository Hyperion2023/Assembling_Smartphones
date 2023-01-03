from Core import Agent
from Core.Utils.Data import create_Environment
import time
path = r"Dataset/d_tight_schedule.txt"

env = create_Environment(path)
# env.draw()
boomer = Agent(env)
# boomer.environment.show()
# boomer.deploy_arms("rand")
boomer.subdivide_in_districts(algorithm="hill_climbing", max_district_size=25, n_restart=1, max_iter=10)
boomer.plan_all_workers(planning_alg="astar", a_star_max_trials=1000, retract_policy="1/4")
boomer.schedule_plans()
boomer.run_schedule()



# t = time.time()
# boomer.running_workers[0].plan_with_astar(None, a_star_max_trials=1000, retract_policy="7/8")
# t = time.time() - t
# print("plan generated in ", t, "seconds")
# print("plan is", len(boomer.running_workers[0].plan), "long")
# input()
# boomer.run_plan([boomer.running_workers[0]])
