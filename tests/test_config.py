#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_config.py
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>
#  Licensed under the Apache License, Version 2.0
#  http://www.apache.org/licenses/LICENSE-2.0

import unittest
import os
from src import config as cfg

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
        cfg.cp.run()
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
        config = cfg.cp.read_config_file(cfg.config)
        # When experienting with different config value,
        #    might not pass.
        assert cfg.var1 == True
        assert cfg.m1 == 'textm1'


    def test_adding_new_data_item(self,):
        """test add new data item  """
        def prt_file(data_dir, flnm):
            with open(f"{data_dir}{flnm}", 'r') as cf:
               fdata = cf.read()
            print(fdata)

        # load the default values
        config = cfg.cp.read_config_file(cfg.config)
        orig_version = config.get("SYSTEM", "sys_cfg_version")
        # print("initial default ini file")
        prt_file(cfg.datadir, cfg.cfg_flnm)

        # remove items from config & change version
        new_version = "0.0.0"
        config.remove_option('MAIN', 'var2')
        config.remove_option("SYSTEM", "sys_var")
        config.set("SYSTEM","sys_cfg_version", new_version)
        cfg.cp.write_cfg(config)
        config = cfg.cp.set_config_variables(config)
        # confirm  var2 has been removed
        assert(config.has_option("MAIN", "var2") == False)
        assert(config.has_option("SYSTEM", "sys_var") == False)

        # read and build missing options
        config = cfg.cp.read_config_file(cfg.config)
        assert(orig_version == cfg.sys_cfg_version)
        assert(config.has_option("MAIN", "var2") == True)
        assert(config.has_option("SYSTEM", "sys_var") == True)

    def test_remove_default_comments(self,):
        """test remove_default_comments """
        # load the default values
        config = cfg.cp.set_default_config(cfg.config)
        comments = dict((k, v) for k, v in config['DATA'].items() if k.startswith('#'))
        cfg.cp.remove_default_comments(cfg.config)

        for k in comments.keys():
            assert(config.has_option("DATA", k) == False)

    def test_print_config_vars(self,):
        """test print of config vars """
        # load the default values
        config = cfg.cp.set_default_config(cfg.config)
        cfg.cp.remove_default_comments(cfg.config)
        cfg.print_config_vars(heading='test of print::no fileobj')
        # print without comments
        cfg.print_config_vars(heading='test of print::no comments', comments=False)

if __name__ == '__main__':
    # unittest.main()

    cf = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
    unittest.TextTestRunner(verbosity=2).run(cf)
