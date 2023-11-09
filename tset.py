import simulator
import os
import json
# import Q
period = 840

for round in range(10):
    if round == 0:
        engine = simulator.Engine(thread_num=1, write_mode="write", specified_run_name="test1")
    else:
        engine = simulator.Engine(thread_num=1, write_mode="append", specified_run_name="test1")

    engine.reset()
    for i in range(period):
        engine.next_step()

        engine.get_current_time()
        engine.get_individual_visited_history(1)
        engine.get_individual_infection_state(1)
        engine.get_individual_visited_history(1)
        engine.get_area_infected_cnt(1)
        a = engine.get_individual_residential_area(4)
        b = engine.get_individual_working_area(10)

        c = engine.get_individual_working_area(100)
        # print (a,b,c)
        d= engine.get_infect_count()
        print (d)

        engine.set_individual_confine_days({1: 5}) # {individualID: day}
        engine.set_individual_quarantine_days({2: 5}) # {individualID: day}
        engine.set_individual_isolate_days({3: 5}) # {individualID: day}
        engine.set_individual_to_treat({4: True}) # {individualID: day}

    del engine
