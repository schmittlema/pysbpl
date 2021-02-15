#!/usr/bin/env python
# An Example using pysbplyaml_path

import os
import map_util
import pysbpl, plot as gui

class Config:
    def __init__(self, **kwargs):
        self.env = pysbpl.EnvironmentNAVXYTHETALAT()
        self.start_id, self.goal_id = self.env.InitializeEnv(**kwargs)
        self.map = kwargs['map']
        print(self.start_id, self.goal_id)

class Planner:
    def __init__(self, config):
        self.planner = pysbpl.ARAPlanner(config.env)
        self.config = config
        
    def initialize(self, start_id, goal_id):
        self.planner.initialize(start_id, goal_id)
        
    def run(self):
        points, headings = self.planner.run()
        if points is None:
            return None, None
        points += self.config.map.origin[:2]
        return points, headings


def example_usage():

    src_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    params = {
        'map': map_util.Map(yaml_path='/home/schmittle/mushr/catkin_ws/src/mushr_sim/maps/sandbox.yaml'),
        'perimeter':[[-0.05, -0.05], [0.05, -0.05], [0.05, 0.05], [-0.05, 0.05]],
        'start':[5.21, 5.16, 0.0],
        'goal': [5.20, 50.16, 0.], # one loop
        'goal_tol':[0.5, 0.5, 0.1],
        'vel':0.5, 'time_45_deg':10,
        'mprim_path': (src_dir + '/mprim/pushr.mprim').encode('utf-8'),
        'obs_thresh': 200,
        'inscribed_thresh': 200,
        'possibly_circumscribed_thresh': 200,
    }

    c = Config(**params)
    p = Planner(c)
    p.initialize(c.start_id, c.goal_id)
    points, headings = p.run()
    if points is not None:
        g = gui.Window()
        g.display_map(params['map'])
        g.display_path(points)
        g.show()
        
if __name__ == '__main__':
    example_usage()
