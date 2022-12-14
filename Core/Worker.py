import time

from Core import Environment, RoboticArm, Task, District
import types
if isinstance(District, types.ModuleType):
    District = District.District
from Core.Astar import State, a_star, goal_test, h, g
from Core.Utils.Dijkstra import create_district_graph_from_env
from Core.Utils.Dijkstra import dijkstra, shortest
from copy import deepcopy

class Worker:
    """
    The Worker class that controls an arm.

    Attributes
    ----------
    arm : Core.RoboticArm.RoboticArm
        The robotic arm assigned to this worker.
    task : Core.Task.Task
        The task assigned to this arm.
    task_points_done: int
        The number of task points done.
    plan: list[tuple[int, int]]
        The plan of the arm to follow.
    action_taken: bool
        Whether the action was taken.
    env: Core.Environment
        The environment in which the worker is running.


    """
    def __init__(self, arm: RoboticArm, task: Task, env: Environment, district: District):
        """
        Worker Class, it takes and arm and a task and performs all the required step to complete the task.
        :param arm: Robotic Arm to cotrol
        :type arm: RoboticArm
        :param task: Task to perform
        :type task: Task
        :param env: Environment in which the arm moves
        :type env: Environment
        """
        self.arm = arm
        self.task = task
        self.task_points_done = 0
        self.plan = []  # TODO: implement in future version
        self.value = None
        self.action_taken = False
        self.env = env
        self.district = district
        self.simple_plan = True
        #self.generate_optimal_path()

    # this is need for CSP solver that order a list for Minimum Remaining Values heuristic
    def __lt__(self, other):
        return str(self) < str(other)

    def my_description(self):
        print("Arm mounted in x: " + str(self.arm.mounting_point.x) + " y: " + str(self.arm.mounting_point.y))
        print("Task assigned with value: ", self.task.value)
        for i in self.task.points:
            print(" Passing through point x: ", i[0], " y: ", i[1])

    def take_action(self):
        self.action_taken = True

    def reset_action_taken(self):
        self.action_taken = False

    def retract_n_steps(self, n):
        if n < 1:
            raise ValueError("retract must be at least 1 move")
        if n >= len(self.arm.path):
            raise ValueError("retract must be non superior to arm path lenght")
        r_move = "W"
        head_position = self.arm.path[-1]
        for i in range(n):
            new_head_position = self.arm.path[-(i + 2)]
            if new_head_position == (head_position[0], head_position[1] + 1):
                r_move = "U"
            if new_head_position == (head_position[0], head_position[1] - 1):
                r_move = "D"
            if new_head_position == (head_position[0] + 1, head_position[1]):
                r_move = "R"
            if new_head_position == (head_position[0] - 1, head_position[1]):
                r_move = "L"
            self.arm.moves.append(r_move)
            head_position = new_head_position
        self.arm.path = self.arm.path[:-n]

    def retract_all(self):
        if len(self.arm.path) > 1:
            self.retract_n_steps(len(self.arm.path) - 1)

    def retract(self):
        if not self.arm.collision_check:
            if len(self.arm.path) > 1:

                return True, self.arm.path[-2]
            else:

                return False, self.arm.path[-1]

        else:
            return False, (0, 0)  # TODO: to modify for real collision_check

    def plan_with_astar(self, a_star_max_trials, retract_policy="1/2", max_time=30):
        starting_state = State(self.env.matrix, [self], retract_policy="soft_retract")
        finished = False
        t = time.time()
        timeout = False
        while not finished:
            if time.time() - t > max_time:
                timeout = True
                break
            final_state, finished = a_star(starting_state, goal_test, g, h, a_star_max_trials)
            if not finished:
                final_state.retract_policy = "hard_retract"
                if isinstance(retract_policy, int):
                    final_state.workers[0].retract_n_steps(retract_policy)
                elif isinstance(retract_policy, str):
                    split_retract_policy = retract_policy.split("/")
                    try:
                        step_to_retract = int((len(final_state.workers[0].arm.path) - 1) * int(split_retract_policy[0]) / int(split_retract_policy[1]))
                        if step_to_retract != 0:
                            final_state.workers[0].retract_n_steps(step_to_retract)
                    except (IndexError, ValueError) as e:
                        print(e)
                        raise ValueError("invalid retract policy")
                else:
                    raise ValueError("invalid retract policy")
                starting_state = final_state
        if timeout:
            self.plan = None
            return self
        final_state.workers[0].retract_all()
        self.plan = final_state.workers[0].arm.moves
        self.value = self.task.value / len(self.plan)
        return self

    def plan_with_dijkstra(self):
        if not self.district.graph:
            self.district.graph, starting_vertex = create_district_graph_from_env(self.env, self.district)
            self.district.graph = dijkstra(self.district.graph, starting_vertex)
        for task_point in self.task.points:
            target = self.district.graph.get_vertex((task_point[0], task_point[1]))
            self.arm.path = [task_point]
            shortest(target, self.arm.path)

            old_p = self.arm.path[0]
            for p in self.arm.path[1:]:
                if p == (old_p[0] + 1, old_p[1]):
                    self.arm.moves.append("R")
                elif p == (old_p[0] - 1, old_p[1]):
                    self.arm.moves.append("L")
                elif p == (old_p[0], old_p[1] + 1):
                    self.arm.moves.append("U")
                elif p == (old_p[0], old_p[1] - 1):
                    self.arm.moves.append("D")
                else:
                    self.arm.moves.append("W")
                old_p = p
            self.retract_all()
        self.plan = self.arm.moves
        self.arm.moves = []
        self.value = self.task.value / len(self.plan)
        return self





    def __deepcopy__(self, memodict={}):
        w = Worker(deepcopy(self.arm, memodict), self.task, env=self.env, district=self.district)
        w.task_points_done = self.task_points_done
        return w
