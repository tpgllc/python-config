#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  breakout_groups.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

# import os
# from pathlib import Path
# import math
# from itertools import combinations, chain
# import itertools as it

from src import config as cfg
from src.event import Event
from src import logger_setup 
import logging
log = logging.getLogger(__name__)

class BreakoutGroups():
    """ generate breakout groups """ 

    attendees_list = []

    n_attendees = 0
    group_size = 0
    n_groups = 0
    n_sessions = 0

    def __init__(self, seed=None) -> None:
        """setup"""
        self.n_attendees = cfg.n_attendees
        self.group_size = cfg.group_size
        self.n_groups = cfg.n_groups
        self.n_sessions = cfg.n_sessions
        self.attendees_list = cfg.attendees_list
        self.event = None
        self.seed = seed
        logger_setup.run()
        log.info("beg breakout-groups")

    def print_variables(self,):
        """print config variables"""
        print(f"         algorithm: {cfg.sys_group_algorithm}")
        print(f"   algoritim_class: {cfg.sys_group_algorithm_class}")
        print("")
        print(f"    attendees_list: {cfg.attendees_list}")
        print(f"         attendees: {cfg.n_attendees}")
        print(f"        group_size: {cfg.group_size}")
        print(f"groups_per_session: {cfg.n_groups}")
        print(f"          sessions: {cfg.n_sessions}")
        print("")

    def run(self,):
        """create breakout groups for event"""
        log.info("beg event processing")
        self.print_variables()
        self.event = Event(self.seed)
        self.event.run()
        self.event.show_sessions()

 
if __name__ == '__main__':
    """ create breakout goups for an event"""
    bg = BreakoutGroups()
    bg.run()
    log.info("end of breakout-groups")
    
    
