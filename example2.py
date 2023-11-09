import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

import simulator
import reward1 as re
import Q0

# engine = simulator.Engine(thread_num=1, write_mode="write", specified_run_name="test_env")

# engine.reset()
# engine.next_step()
# a = engine.get_individual_working_acq(1)  #
# print(a)


class Env:
    def __init__(self,engine):
        self.action_space = ['None','confine', 'quarantine', 'isolate', 'treat']
        self.n_actions = len(self.action_space)
        self.engine = engine
        # engine = simulator.Engine(thread_num=1, write_mode="write", specified_run_name="test1")
        # self._build_state(self.i)
        # engine.next_step()
    def all_area(self,j):
        all_area = self.engine.get_all_area_category()
        if j <= all_area[4]:
            id = 0
        elif all_area[4]< j <= all_area[8]:
            id = 1
        else :
            id = 2
        return id

    def live_risk(self,i):

        self.residential_in = self.engine.get_area_infected_cnt(i)  # 生活区域感染人数
        if self.residential_in == 0:
            p_r = 1
        elif 0 < self.residential_in <= 10:
            p_r = 2
        elif 10 < self.residential_in <= 100:
            p_r = 3
        elif 100 < self.residential_in <= 1000:
            p_r = 4
        else:
            p_r = 5


        return p_r

    def work_risk(self, i):
        # self.working = self.engine.get_individual_working_area(i)  # 工作区域
        self.working_in = self.engine.get_area_infected_cnt(i)  # 工作区域感染人数
        # 工作区风险等级
        if self.working_in == 0:
            p_w = 1
        elif 0 < self.working_in <= 10:
            p_w = 2
        elif 10 < self.working_in <= 100:
            p_w = 3
        elif 100 < self.working_in <= 1000:
            p_w = 4
        else:
            p_w = 5
        # print('风险评级:',p_r, p_w)
        return p_w

    def state(self,i):


        """感染和注射情况"""
        self.infection = self.engine.get_individual_infection_state(i)  # 感染情况
        self.intervention = self.engine.get_individual_intervention_state(i)  # 注射状态

        """风险等级"""
        self.residential = self.engine.get_individual_residential_area(i) # 居住区域
        p_r = self.live_risk(self.residential)
        self.working  = self.engine.get_individual_working_area(i)     # 工作区域
        p_w = self.work_risk(self.working)
        # self.residential_in = self.engine.get_area_infected_cnt(self.residential) # 生活区域感染人数
        # self.working_in = self.engine.get_area_infected_cnt( self.working)          # 工作区域感染人数
        # print('感染人数：',self.residential_in,self.working_in)
        aiid = self.engine.get_individual_visited_history(i)  # 过去5天，去过的区域的ID的一维列表
        # print(len(aiid),aiid[1],aiid)


        p_five = 1
        p_aiid = 1
        for i in range(len(aiid)):
            #判断一下
            id = self.all_area(aiid[i])
            if id == 0:
                p_aiid = self.live_risk(aiid[i])/15
            elif id == 1:
                p_aiid = self.work_risk(aiid[i])/15
            p_five = p_five*p_aiid



        """住院率"""
        in_hospital = self.engine.get_hospitalize_count()

        p_in_hospital = self.engine.get_hospitalize_count()/10000
        # print ('住院率:',self.engine.get_hospitalize_count(),p_in_hospital)

        # 集中隔离率
        in_isolate = self.engine.get_isolate_count()
        # 在家孤立
        in_quarantine = self.engine.get_quarantine_count()
        # 限制人数
        in_confine  = self.engine.get_confine_count()

        num_stranger = self.engine.get_stranger_count()
        # print(num_stranger)
        num_acquaintance = self.engine.get_acquaintance_count()

        self.acq = self.engine.get_individual_working_acq(i)   # 工作区联系人ID



        """区域"""
        # self.engine.get_area_visited_history(i)  # 过去5天中某个地区访问历史的二维列表



        """统计人数"""
        # self.contain = self.engine.get_area_contained_individual()  # 输出居住客户的ID
        # self.all = self.engine.get_all_area_category()

        # print(len(self.all),self.contain.keys())


        """时间"""
        # self.engine.get_current_time()
        # self.engine.get_current_hour()
        # self.engine.get_current_day()


        """定义状态"""
        state = [self.intervention, self.infection,
                 self.residential, p_r, self.working, p_w,
                 in_hospital,in_isolate, in_quarantine , in_confine,
                 num_stranger, num_acquaintance,
                 p_five]


        # print('state',state)
        # print('感染状态','注射状态',
        #        '住宅区域','住宅风险等级', '工作区域','工作区域风险等级',
        #        '医院人数','隔离人数','居家隔离人数','限制人数'
        #        '接触陌生人','接触熟人')
        return state



    def action1(self, num,action):
        # s = self.canvas.coords(self.rect)
        # base_action = np.array([0, 0])

        if action == 0:  # confine
                pass
        elif action == 1:
            self.engine.set_individual_confine_days({num: 5})  # {individualID: day}
        elif action == 2:   # quarantine
            self.engine.set_individual_quarantine_days({num: 5})  # {individualID: day}
        elif action == 3:     # isolate
            self.engine.set_individual_isolate_days({num: 5})  # {individualID: day}
        elif action == 4:                   # treat
            self.engine.set_individual_to_treat({num: 5})  # {individualID: day}
    def action(self, num, action):
        # s = self.canvas.coords(self.rect)
        # base_action = np.array([0, 0])
        if action[0] == 0:   #confine
            pass
        elif action[0] == 1:   # quarantine
            self.engine.set_individual_confine_days({num: action[1]})  # {individualID: day}
        elif action[0] == 2:   # quarantine
            self.engine.set_individual_quarantine_days({num: action[1]})  # {individualID: day}
        elif action[0] == 3:     # isolate
            self.engine.set_individual_isolate_days({num: action[1]})  # {individualID: day}
        elif action[0] ==4:                   # treat
            self.engine.set_individual_to_treat({num: action[1]})  # {individualID: day}

    def step(self, state):
        # s = self.canvas.coords(self.rect)
        # base_action = np.array([0, 0])
        state = state
        """如何更新状态，未完成"""
        next_state  =  state
        return next_state


    def reward(self):
        import os
        I_threshold = 1000
        Q_threshold = 100000
        Q_weight = 1
        time = 59  # The last day of our simulation


        import sys

        df = re.process_file("/Users/d/work/xin/starter-kit/examples/results/cnt_test.txt")
        I, Q = re.get_I_Q(df, time)
        least_Q_score = re.get_least_Q_score(I, Q, I_threshold)
        exp_score = re.get_exp_score(I, Q, I_threshold, Q_threshold, Q_weight)
        # print("输出得分:" , least_Q_score, exp_score)
        return  -exp_score

    def reset(self):


        # return observation
        return self.canvas.coords(self.rect)





if __name__ == '__main__':
    period = 840
    engine = simulator.Engine(thread_num=1, write_mode="write", specified_run_name="test3")
    engine.reset()
    from Q1 import QLearningTable
    env = Env(engine)

    RL = QLearningTable(actions=list(range(env.n_actions)))


    for i in range(period):
        engine.next_step()
        engine.get_current_time()
        # print(engine.get_current_day())
        for num in range(1):
            state = []
            action = 0
            next_state = []
            reward = 0
            if engine.get_current_hour() == 0:
                state = env.state(num)
                action = RL.choose_action(str(state))
                # print(action)
                env.action(num, action)
            if engine.get_current_hour() == 13:
                next_state = env.state(num)
            reward = env.reward()

            RL.learn(str(state), action, reward, str(next_state))
            # state = next_state

    del engine