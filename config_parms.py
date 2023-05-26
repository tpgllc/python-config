#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config_parms.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

from src import config as cfg


class ConfigParms():
    """ config parms model """

    def __init__(self, seed=None) -> None:
        """setup"""
        self.n_attendees = cfg.n_attendees
        self.group_size = cfg.group_size
        self.n_groups = cfg.n_groups
        self.n_sessions = cfg.n_sessions
        self.attendees_list = cfg.attendees_list
        self.event = None
        self.seed = seed


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
        print("beg event processing")
        self.print_variables()
        cfg.debug_print()


if __name__ == '__main__':
    """ print the config parms"""
    print("beg config_parms")
    # cp = ConfigParms(cfg.cfg_values)
    # cp.run()
    cfg.cp.debug_print()
    print("end config_parms")


