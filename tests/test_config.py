#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_config.py
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>

import unittest
import os
from src import config as cfg
from numpy import testing as npt

class TestConfig(unittest.TestCase):
    """ tests for the """

    testfile_path = "tests/testfiles/"

    @classmethod
    def setUpClass(cls):
        """class set up"""
        print("\n ------- \nTesting module - test_config.py")
        if not os.path.exists(cls.testfile_path):
           os.mkdir(cls.testfile_path)

        cfg.datadir = cls.testfile_path
        return

    @classmethod
    def tearDownClass(cls):
        """class tear down"""
        if os.path.exists(cls.testfile_path):
            for pth, dir, files in os.walk(cls.testfile_path):
                for fl in files:
                     os.remove(f"{cls.testfile_path}{fl}")
            os.rmdir(cls.testfile_path)
        return

    def setUp(self):

        return

    def tearDown(self):

        return

    def test_update(self):

        pass

    def test_default_config(self,):
        """test set_default_config """

        # load the default values
        config = cfg.read_config_file(cfg.config)
        # When experienting with different config value,
        #    might not pass.
        assert cfg.n_attendees == 11
        assert cfg.group_size == 3
        assert cfg.n_groups == 3
        assert cfg.n_sessions == 4


    def test_adding_new_data_item(self,):
        """test add new data item  """
        print("test adding")
        def prt_file(data_dir, flnm):
            with open(f"{data_dir}{flnm}", 'r') as cf:
               fdata = cf.read()
            print(fdata)

        # load the default values
        config = cfg.read_config_file(cfg.config)
        orig_version = config.get("SYSTEM", "sys_version")
        # print("initial default ini file")
        prt_file(cfg.datadir, cfg.flnm)

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

    def test_remove_default_comments(config_defaults):
         """test remove_default_comments """
         pass

    def test_write_ini(config_defaults):
      """test write on ini_file"""
      pass


if __name__ == '__main__':
    # unittest.main()

    cf = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
    unittest.TextTestRunner(verbosity=2).run(cf)
