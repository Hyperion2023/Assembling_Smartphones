class Task:
    def __init__(self, value=0, n_points=0):
        self.value = value
        self.n_points = n_points
        self.points = []
        self.distance = 0

    @staticmethod
    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def add_point(self, x, y):
        if len(self.points) == self.n_points:
            raise ValueError("Number of points execeeded!")
        self.update_distance(x, y)  # update_distance must be called before adding point
        self.points.append((x, y))

    def update_distance(self, x, y):
        if len(self.points) == 0:
            return
        last_point = self.points[-1]
        self.distance += self.manhattan_distance(last_point, (x, y))

    def get_task_score(self, mounting_point):
        first_point = self.points[0]
        return self.value / (self.distance + self.manhattan_distance(first_point, mounting_point))