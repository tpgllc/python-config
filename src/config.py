#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
#     in each module, from src import config as cfg
#     access variables in this module as cfg.xxxxxx
#
#     the config file is created in the data directory and can be modified
#     for a specific run.
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

# import this module as the first application module:
#     import src.config as cfg

import configparser
from pathlib import Path
import os

cfg_flnm = 'test_config.cfg'
wkdir_path = None
wkdir = None
srcdir = None
datadir = None

# variables
var1 = True
var2 = 2
var3 = 3.4
m1 ='textm1'
m2 = ['m2-1', 'm2-2', 'm2-3']

# system variables
sys_cfg_version = '0.1'
sys_var = "sysvar test variable"

# values passed to ConfigParms
# dict key is the section, value is list of variable names and type
#   types are i-integer, f-float, b-boolean, s-string, l-list

cfg_values = {'MAIN': [('var1', 'b'), ('var2', 'i'), ('var3', 'f')],
              'DATA': [('m1', 's'), ('m2', 'l')],
              'SYSTEM': [('sys_cfg_version', 's'), ('sys_var', 's')],
              'comments': {'sys_cfg_version': ['changing the version number will cause file to be rewritten'],
                           'sys_var': ['sys var cmt1', 'sys var cmt2'],
                           'var1': ['this is a comment for var1'],
                           'm2': ['m2 comment 1', 'm2 comment 2']}
              }


# config obj
config = None
# variables passed to all modules
gen_var1 = []

class ConfigParms:
    """ read the config file and set cfg values
        if version changes, the cfg file is read and rewritten with the new changes reflected.
           The data values in the cfg file are perserved
    """

    def __init__(self, cfg_values, autorun=False):
        """ on init, load the directory paths, if autorun read the cfg file"""
        self.cfg_values = cfg_values

        global wkdir_path, wkdir, srcdir, datadir

        # set the directories
        if wkdir is None:
            wkdir_path = Path(__file__).parent.parent.resolve()
            srcdir = str(Path(__file__).resolve().parent) + os.sep
            wkdir = str(Path(srcdir).resolve().parent) + os.sep
            datadir = str(Path(wkdir).resolve()) + os.sep + 'data' + os.sep


        if autorun:
            self.run()


    def run(self,) -> None:
        """ read the config file, if not found, write the default file,
            set the values in the config module
        """
        global config
        config = configparser.ConfigParser(allow_no_value=True)
        config = self.read_config_file(config)

        self.set_config_variables(config)

        return

    def read_config_file(self, config):
        """read in the breakout_groups.ini file if exists or create it"""
        if Path(f"{datadir}{cfg_flnm}").is_file():
            config.read(f"{datadir}{cfg_flnm}")
        else:
            # create the default config file
            config = self.set_default_config(config)
            config = self.write_cfg(config)

        # if the sys_version is different, write out the new config file
        if not config.has_option('SYSTEM', 'sys_cfg_version') or sys_cfg_version != config.get('SYSTEM', 'sys_cfg_version'):
            self.set_config_variables(config)
            self.set_default_config(config)
            self.write_cfg(config)

        # remove comments from sections to be consistent with data from read
        self.remove_default_comments(config)
        return config

    def set_default_config(self, config):
        """define the default config file, adding varibles with default values """
        for sec, vars in self.cfg_values.items():
            # skip comments section
            if sec == 'comments':
                continue
            # create the section
            if not config.has_section(sec):
                config.add_section(sec)
            config[sec].clear()
            for var in vars:
                var_name = var[0]
                # check for comments and add them if they exists
                if var_name in self.cfg_values['comments']:
                    for c in self.cfg_values['comments'][var_name]:
                        config.set(sec, f"# {c}")

                if var_name == 'm2':
                    lm = str(globals()[var_name])
                    dm = str(globals()['cfg_values'])
                    a = True

                # add the variable
                if var[1] == 'l':
                    # process list
                    config.set(sec, var_name, ','.join(x for x in globals()[var_name]))
                else:
                    config.set(sec, var_name, str(globals()[var_name]))

        return config

    def remove_default_comments(self, config):
        """remove the comments set up in the defaults"""
        for s in config.sections():
            # the key is a tuple (key, value)
            for key in config[s].items():
                if key[0][:1] in config._comment_prefixes:
                    config.remove_option(s, key[0])

    def write_cfg(self, config):
        """ write the cfg file from the current cfg settings"""
        with open(f"{datadir}{cfg_flnm}", 'w') as configfile:
            config.write(configfile)
        return config

    def set_config_variables(self, config):
        """set the variables from config for consistant access"""
        for sec, vars in self.cfg_values.items():
            # skip comments section
            if sec == 'comments':
                continue

            for var in vars:
                var_name = var[0]
                # do not override the module version number
                if var_name == 'sys_cfg_version':
                    continue
                # set variable from config value
                match var[1]:
                    case 'b':
                        globals()[var_name] = config.getboolean(sec, var_name, fallback=globals()[var_name])
                    case 'f':
                        globals()[var_name] = config.getfloat(sec,var_name, fallback=globals()[var_name])
                    case 'i':
                        globals()[var_name] = config.getint(sec, var_name, fallback=globals()[var_name])
                    case 'l':
                        listitems = []
                        list_str = config.get(sec, var_name, fallback=globals()[var_name])
                        if type(list_str) == 'str':
                            listitems.append(list_str.split(','))
                        globals()[var_name] = listitems
                    case 's':
                        globals()[var_name] = config.get(sec, var_name, fallback=globals()[var_name])

        return config

    def debug_print(self, ):
        print("")
        print(f"    wkdir: {wkdir}")
        print(f"  inc dir: {srcdir}")
        print(f" data dir: {datadir}")
        print(f"file name: {cfg_flnm}")
        print("")

        print(f"sections: {config.sections()}")

        # print config variables
        for sec, vars in config.items():
            print(config[sec])
            for var, val in vars.items():
                print(f"   {var}: {val}")

"""
This module takes advantage of Python's behavior of importing the module the first time and for
every import after the first, only a reference is passed.

There are several ways to instantiate the ConfigParm class which reads the cfg file.  Pick an
approach that you like.

to autorun on the first import:
    cp = ConfigParms(cfg_values, autorun=True)
or
    cp = ConfigParms(cfg_values)
    cp.run()

to control the autorun, just instantiate the class in this module
    cp = ConfigParms(cfg_values)

and then in the application code, read the parm file:
    cfg.cp.run()
"""
cp = ConfigParms(cfg_values)
# cp.run()

