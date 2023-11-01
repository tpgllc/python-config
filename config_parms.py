#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config_parms.py
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>
#  Licensed under the Apache License, Version 2.0
#  http://www.apache.org/licenses/LICENSE-2.0

from src import config as cfg

if __name__ == '__main__':
    """ print the config parms"""
    print("beg config_parms")
    cfg.cp.run()
    cfg.cp.print_config_vars()
    print("end config_parms")


