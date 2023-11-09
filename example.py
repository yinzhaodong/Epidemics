import simulator
import os
import json

period = 840

engine = simulator.Engine(thread_num=1, write_mode="write", specified_run_name="test1")

engine.reset()
for i in range(period):
    engine.next_step()
    engine.get_current_time()
    engine.get_life_count()

    # a = engine.get_all_area_category()
    b = engine.get_current_day()
    c = engine.get_current_hour()
    d = engine.get_current_time()
    e = engine.get_individual_infection_state(1)
    # print('1', b, c,d,e)


    engine.get_individual_visited_history(1)
    engine.get_individual_infection_state(1)
    engine.get_individual_visited_history(1)
    engine.get_area_infected_cnt(1)
    # print(engine.get_area_infected_cnt(2))
    engine.set_individual_confine_days({1: 5}) # {individualID: day}
    engine.set_individual_quarantine_days({2: 5}) # {individualID: day}
    engine.set_individual_isolate_days({3: 5}) # {individualID: day}
    engine.set_individual_to_treat({4: True}) # {individualID: day}



del engine
