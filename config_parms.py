#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config_parms.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

from src import config as cfg

if __name__ == '__main__':
    """ print the config parms"""
    print("beg config_parms")
    cfg.cp.run()
    cfg.cp.print_config_vars()
    print("end config_parms")


