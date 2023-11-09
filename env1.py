import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

import simulator

UNIT = 40   # pixels
MAZE_H = 4  # grid height
MAZE_W = 4  # grid width
# engine = simulator.Engine(thread_num=1, write_mode="write", specified_run_name="test_env")

# engine.reset()
# engine.next_step()
# a = engine.get_individual_working_acq(1)  #
# print(a)


class Env:
    def __init__(self, i):
        self.action_space = ['confine', 'quarantine', 'isolate', 'treat']
        self.n_actions = len(self.action_space)

        engine = simulator.Engine(thread_num=1, write_mode="write", specified_run_name="test1")
        self.i = i
        # self._build_state(self.i)
        engine.reset()
        engine.next_step()

        """个人"""
        self.infection = engine.get_individual_infection_state(i)  # 感染情况
        self.intervention = engine.get_individual_intervention_state(i)  # 注射状态

        self.residential = engine.get_individual_residential_area(i) # 居住区域
        self.working  = engine.get_individual_working_area(i)     # 工作区域


        self.acq = engine.get_individual_working_acq(i)   # 工作区联系人ID

        engine.get_individual_visited_history(i)  # 过去5天，去过的区域的ID的一维列表


        """区域"""
        engine.get_area_visited_history(i)  # 过去5天中某个地区访问历史的二维列表
        engine.get_area_infected_cnt(i)      # 有症状和严重的人数

        """统计人数"""
        self.contain = engine.get_area_contained_individual()  # 输出居住客户的ID

        print(type(self.contain))
        print(len(self.contain),self.contain.key)
        engine.get_life_count()             # 不再医院的人数
        engine.get_hospitalize_count()      # 在医院的人数
        engine.get_isolate_count()          # 熟人隔离人数
        engine.get_quarantine_count()       # 非熟人隔离人数

        engine.get_confine_count()          # 受限总人数
        engine.get_stranger_count()         # 接陌生人人数
        engine.get_acquaintance_count()     # 接触熟人人数

        """时间"""
        engine.get_current_time()
        engine.get_current_hour()
        engine.get_current_day()

        state = [self.intervention, self.infection, self.residential, self.working,
                 ]

        # state.append()
        # state.append(self.residential)
        # state.append(self.working)
        print('state',state)




    def step(self, action):
        # s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action[0] == 0:   #confine
            engine.set_individual_confine_days({1: action[1]})  # {individualID: day}
        elif action[0] == 1:   # quarantine
            engine.set_individual_quarantine_days({2: action[1]})  # {individualID: day}
        elif action[0] == 2:     # isolate
            engine.set_individual_isolate_days({3: action[1]})  # {individualID: day}
        elif action[0] ==3:                   # treat
            engine.set_individual_to_treat({4: action[1]})  # {individualID: day}





        # reward function
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
            s_ = 'terminal'
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:
            reward = -1
            done = True
            s_ = 'terminal'
        else:
            reward = 0
            done = False

        return s_, reward, done

    def reset(self):
        self.update()

        # return observation
        return self.canvas.coords(self.rect)





if __name__ == '__main__':
    env = Env(1)
