#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_config.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

"""PyTest - basic operation and concepts.

HOW TO RUN THE TESTS
--------------------
1. Run all tests in a directory
% cd directory
% pytest


2. Run all tests in a file
% pytest test_file.py


3. Run a specific test
% pytest test_file.py::test_specific_one

4. Run all tests with a specific marker associated with some tests
Any of the above commands but with the -m parameter
% pytest -m "end-to-end" 



HANDY COMMAND LINE OPTIONS
--------------------------
-s   Output from all python print() statements is written to console
-v   verbose output.  Lists each test


FIXTURES
--------
Syntactically, these are just Python decorators.  They play many roles
1. Replace start-up and tear_down
2. Paramtrize inputs to tests
3. Global variables, but in a sane manner



ORGANIZATION OF A TEST SUITE
----------------------------
I typically do not create a class for the test cases.
Test cases must begin witht the string "test_" or pytest will ignore them.
Test cases and helper methods may be included, in any order in the file.

The file "conftest.py" plays many roles.
1. It is often the home for all the fixtures used by this suite.
2. Simplifies importing code to be tested - code that is in scr directory



DIFFERENCES FROM UnitTest
-------------------------
There is no explicit setup and tear down methods.  Rather fixtures
   do those tasks.  More on Fixtures later.


HANDY PYTEST FEATURES
---------------------
1. Do you know about brekpoint() and the pytest debugger?
2. Pytest has its own set commands to handle temporary directories.
   The come and go with each test run.  See the fixture named
   "setup_directories"

"""   
import os
from src import config as cfg
import pytest

# Simple example of pytest temporary directories.
# tmp_dir is a built_in fixture
# ToDo move this fixture to conftest.py
# Also, this is an example of a pytest marker
def test_make_temp_directory(tmp_path):
   """test make temp dir"""
   base_dir = tmp_path / "breakout_groups"
   base_dir.mkdir()
   # does the directory exist?
   assert base_dir.exists()
   assert base_dir.is_dir()


# ToDo Convert to a fixture so that config info is available everywhere
def test_default_config(config_event_defaults, tmp_path):
   """test set_default_config """
   base_dir = tmp_path / "breakout_groups" 
   base_dir.mkdir()
   cfg.datadir = str(base_dir) + os.sep
   # load the default values
   config = cfg.read_config_file(cfg.config)
   # When experienting with different config value, 
   #    might not pass.
   assert cfg.n_attendees == 11
   assert cfg.group_size == 3
   assert cfg.n_groups == 3
   assert cfg.n_sessions == 4     

def test_build_session_labels():
   """ test the building of the session labels"""
   cfg.build_group_labels()
   res0 = ['group1', 'group2', 'group3', 'group4', 'group5']
   res2 = ['Portales', 'Santa Fe', 'Taos', 'Chama', 'Cuba']
   assert cfg.group_labels[0] == res0 
   assert cfg.group_labels[2] == res2 

def test_adding_new_data_item(config_event_defaults, tmp_path):
   """test add new data item  """
   print("test adding")
   def prt_file(base_dir, flnm):
      fp = base_dir.joinpath(flnm)
      with open(base_dir.joinpath(flnm), 'r') as cf:
         fdata = cf.read()
      print(fdata)

   base_dir = tmp_path / "breakout_groups" 
   base_dir.mkdir()
   cfg.datadir = str(base_dir) + os.sep
   # load the default values
   config = cfg.read_config_file(cfg.config)
   orig_version = config.get("SYSTEM", "sys_version")
   # print("initial default ini file")
   # prt_file(base_dir, cfg.flnm) 

   # remove items from config & change version
   new_version = "0.0.0"
   config.remove_option('EVENT', 'n_attendees')
   config.remove_option("SYSTEM", "sys_group_algorithm")
   config.set("SYSTEM","sys_version", new_version)
   config = cfg.write_ini(config)
   config = cfg.set_event_variables(config)
   # print("ini file with missing variables")
   # prt_file(base_dir, cfg.flnm)
   # confirm ini file version has been reset and n_attendees removed
   assert(config.has_option("EVENT", "n_attendees") == False)
   assert(config.has_option("SYSTEM", "sys_group_algorithm") == False)

   # read and build missing options
   config = cfg.read_config_file(cfg.config)
   # print("rebuild with new variable")
   # prt_file(base_dir, cfg.flnm)
   # confirm options are added back when missing
   assert(orig_version == cfg.sys_version)
   assert(config.has_option("EVENT", "n_attendees") == True)
   assert(config.has_option("SYSTEM", "sys_group_algorithm") == True)


@pytest.mark.skip(reason="pending")
def test_remove_default_comments(config_defaults):
        """test remove_default_comments """
        pass

@pytest.mark.skip(reason="pending")
def test_write_ini(config_defaults):
   """test write on ini_file"""
   pass