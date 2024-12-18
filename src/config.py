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
#  Copyright 2023 cswaim <cswaim@jcrl.net>
#  Licensed under the Apache License, Version 2.0
#  http://www.apache.org/licenses/LICENSE-2.0

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
m2 = ['m2-1','m2-2','m2-3']

# system variables
sys_cfg_version = '0.1'
sys_var = "sysvar test variable"

# values passed to ConfigParms
# dict key is the section, value is list of variable names and type
#   types are i-integer, f-float, b-boolean, s-string, l-list

cfg_values = {'MAIN': [('var1', 'b'), ('var2', 'i'), ('var3', 'f')],
              'DATA': [('m1', 's'), ('m2', 'l')],
              'SYSTEM': [('sys_cfg_version', 's'), ('sys_var', 's')],
              }
cfg_comments = {'sys_cfg_version': ['changing the version number will cause file to be rewritten'],
                'sys_var': ['sys var cmt1', 'sys var cmt2'],
                'var1': ['this is a comment for var1'],
                'm2': ['m2 comment 1', 'm2 comment 2'],
                'DATA': ['sec comment 1', 'sec comment 2']
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

    def __init__(self, cfg_values=cfg_values, cfg_comments=cfg_comments, autorun=False):
        """ on init, load the directory paths, if autorun read the cfg file"""
        self.cfg_values = cfg_values
        self.cfg_comments = cfg_comments

        global wkdir_path, wkdir, srcdir, datadir

        # set the directories
        if wkdir is None:
            wkdir_path = Path(__file__).parent.parent.resolve()
            srcdir = str(Path(__file__).resolve().parent) + os.sep
            wkdir = str(Path(srcdir).resolve().parent) + os.sep
            datadir = str(Path(wkdir).resolve()) + os.sep + 'data' + os.sep

        global config
        config = configparser.ConfigParser(allow_no_value=True)

        if autorun:
            self.run()


    def run(self,) -> None:
        """ read the config file, if not found, write the default file,
            set the values in the config module
        """
        global config
        # the config is a ConfigParser object, and can be
        # updated by read_config_file, so it is returned
        config = self.read_config_file(config)

        self.set_config_variables(config)

        return

    def read_config_file(self, config):
        """read in the config file if exists or create it"""
        if Path(f"{datadir}{cfg_flnm}").is_file():
            config.read(f"{datadir}{cfg_flnm}")
        else:
            # create the default config file
            config = self.set_default_config(config)
            self.write_cfg(config)

        # if the sys_version is different, write out the new config file
        if not config.has_option('SYSTEM', 'sys_cfg_version') or sys_cfg_version != config.get('SYSTEM', 'sys_cfg_version'):
            self.set_config_variables(config)
            self.set_default_config(config)
            self.write_cfg(config)

        # verify all attributes are present in config
        self.verify_config_attributes(config)

        # remove comments from sections to be consistent with data from read
        self.remove_default_comments(config)
        return config

    def write_cfg(self, config):
        """ write the cfg file from the current cfg settings"""
        with open(f"{datadir}{cfg_flnm}", 'w') as configfile:
            config.write(configfile)
        return

    def set_default_config(self, config):
        """define the default config file, adding varibles with default values """
        for sec, vars in self.cfg_values.items():
            # create the section
            if not config.has_section(sec):
                config.add_section(sec)
            config[sec].clear()
            self.check_for_comments(sec)

            for var in vars:
                var_name = var[0]
                # check for comments and add them if they exists
                self.check_for_comments(sec, var_name)

                # add the variable
                if var[1] == 'l':
                    # process list - convert to string
                    listitems = (globals()[var_name])
                    list_str = ",".join(x for x in listitems)
                    config.set(sec, var_name, list_str)
                else:
                    config.set(sec, var_name, str(globals()[var_name]))

        return config

    def set_config_variables(self, config):
        """set the variables from config for consistant access"""
        for sec, vars in self.cfg_values.items():
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
                        # convert string to list
                        listitems = []
                        list_str = config.get(sec, var_name, fallback=globals()[var_name])
                        if isinstance(list_str, str):
                            listitems = list_str.split(',')
                        else:
                            # if list_str not str, then it is the fallback list
                            listitems = list_str
                        globals()[var_name] = listitems
                    case 's':
                        globals()[var_name] = config.get(sec, var_name, fallback=globals()[var_name])

        return config

    def check_for_comments(self, sec, var_name=None):
        """set comments in config, if they exist for a sec or variable,
            comments are set after a section and before a variable
            comments will be written to file, then removed from config later
        """
        if var_name is None:
            if sec in self.cfg_comments.keys():
                for c in self.cfg_comments[sec]:
                    config.set(sec, f"# {c}")
        else:
            if var_name in self.cfg_comments.keys():
                for c in self.cfg_comments[var_name]:
                    config.set(sec, f"# {c}")

    def remove_default_comments(self, config):
        """remove the comments set up in the defaults"""
        for s in config.sections():
            # the key is a tuple (key, value)
            for key in config[s].items():
                if key[0][:1] in config._comment_prefixes:
                    config.remove_option(s, key[0])

    def verify_config_attributes(self, config):
        """verify all attributes are present in config"""
        for sec, vars in self.cfg_values.items():
            # create the section
            if not config.has_section(sec):
                config.add_section(sec)

            for var in vars:
                var_name = var[0]
                # if variable does not exist
                if not config.has_option(sec, var_name):
                    # add the variable
                    if var[1] == 'l':
                        # process list - convert to string
                        listitems = (globals()[var_name])
                        list_str = ",".join(x for x in listitems)
                        config.set(sec, var_name, list_str)
                    else:
                        config.set(sec, var_name, str(globals()[var_name]))

def print_config_vars(heading=None, comments=True, fileobj=None ):
    print("", file=fileobj)
    if heading is not None:
        print(f"--- {heading} ---", file=fileobj)

    print(f"    wkdir: {wkdir}", file=fileobj)
    print(f"  inc dir: {srcdir}", file=fileobj)
    print(f" data dir: {datadir}", file=fileobj)
    print(f"file name: {cfg_flnm}", file=fileobj)
    print("", file=fileobj)

    print(f"sections: {config.sections()}", file=fileobj)

    # print config variables
    for sec, vars in config.items():
        if comments:
            print_cfg_var_comments(sec, sec=True, fileobj=fileobj)
        print(config[sec], file=fileobj)
        for var, val in vars.items():
            if comments:
                print_cfg_var_comments(var, fileobj=fileobj)
            print(f"   {var}: {val}", file=fileobj)

def print_cfg_var_comments( var, sec=False, fileobj=None):
    """look for comments for the var (sec or var)"""
    if var in cfg_comments.keys():
            for c in cfg_comments[var]:
                if sec:
                    print(f"# {c}", file=fileobj)
                else:
                    print(f"   # {c}", file=fileobj)

"""
This module takes advantage of Python's behavior of importing the module
the first time and for every import after the first, only a reference is passed.

There are several ways to instantiate the ConfigParm class which reads the
cfg file.  Pick an approach that you like.

Note that setting the autorun may effect tests as the defaults from the
config file are loaded and the test defaults must be reset.

to autorun on the first import:
    cp = ConfigParms(cfg_values, cfg_comments, autorun=True)
or
    cp = ConfigParms(cfg_values, cfg_comments)
    cp.run()

to control the autorun, just instantiate the class in this module
    cp = ConfigParms(cfg_values, cfg_comments)

and then in the application code, read the parm file:
    cfg.cp.run()
"""
cp = ConfigParms(cfg_values, cfg_comments)

