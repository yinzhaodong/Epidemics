import simulator
import os
import json

period = 840

for round in range(10):
    if round == 0:
        engine = simulator.Engine(thread_num=1, write_mode="write", specified_run_name="test")
    else:
        engine = simulator.Engine(thread_num=1, write_mode="append", specified_run_name="test")

    engine.reset()

    for i in range(period):
        engine.next_step()

        for num in range(10000):
            engine.get_individual_infection_state(num)

            engine.get_current_time()
            engine.get_individual_visited_history(num)
            engine.get_individual_infection_state(num)
            engine.get_individual_visited_history(num)
            engine.get_area_infected_cnt(num)

            if engine.get_individual_infection_state(num) == 1 :
                engine.set_individual_confine_days({num: 5}) # {individualID: day}
            elif engine.get_individual_infection_state(num) == 2:
                engine.set_individual_quarantine_days({num: 5})  # {individualID: day}
            elif engine.get_individual_infection_state(num) == 3:
                engine.set_individual_isolate_days({num: 5}) # {individualID: day}
            elif engine.get_individual_infection_state(num) ==4:
                engine.set_individual_to_treat({num: True}) # {individualID: day}

    del engine
