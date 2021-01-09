import unittest
import maya.cmds as cmds


class TestCase(unittest.TestCase):
    pass
    # """Base class for unit test cases run in Maya.

    # Tests do not have to inherit from this TestCase but this derived TestCase contains convenience
    # functions to load/unload plug-ins and clean up temporary files.
    # """

    # # Keep track of all temporary files that were created so they can be cleaned up after
    # # all tests have been run
    # files_created = []

    # # Keep track of which plugins were loaded so we can unload them after all tests have been run
    # plugins_loaded = set()

    # @classmethod
    # def tearDownClass(cls):
    #     super(TestCase, cls).tearDownClass()
    #     cls.delete_temp_files()
    #     cls.unload_plugins()

    # @classmethod
    # def load_plugin(cls, plugin):
    #     """Load the given plug-in and saves it to be unloaded when the TestCase is finished.

    #     @param plugin: Plug-in name.
    #     """
    #     cmds.loadPlugin(plugin, qt=True)
    #     cls.plugins_loaded.add(plugin)

    # @classmethod
    # def unload_plugins(cls):
    #     # Unload any plugins that this test case loaded
    #     for plugin in cls.plugins_loaded:
    #         cmds.unloadPlugin(plugin)
    #     cls.plugins_loaded = []

    # @classmethod
    # def delete_temp_files(cls):
    #     """Delete the temp files in the cache and clear the cache."""
    #     # If we don't want to keep temp files around for debugging purposes, delete them when
    #     # all tests in this TestCase have been run
    #     if Settings.delete_files:
    #         for f in cls.files_created:
    #             if os.path.exists(f):
    #                 os.remove(f)
    #         cls.files_create = []

    # @classmethod
    # def get_temp_filename(cls, file_name):
    #     """Get a unique filepath name in the testing directory.

    #     The file will not be created, that is up to the caller.  This file will be deleted when
    #     the tests are finished.
    #     @param file_name: A partial path ex: 'directory/somefile.txt'
    #     @return The full path to the temporary file.
    #     """
    #     temp_dir = Settings.temp_dir
    #     if not os.path.exists(temp_dir):
    #         os.makedirs(temp_dir)
    #     base_name, ext = os.path.splitext(file_name)
    #     path = "{0}/{1}{2}".format(temp_dir, base_name, ext)
    #     count = 0
    #     while os.path.exists(path):
    #         # If the file already exists, add an incrememted number
    #         count += 1
    #         path = "{0}/{1}{2}{3}".format(temp_dir, base_name, count, ext)
    #     cls.files_created.append(path)
    #     return path
