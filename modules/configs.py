"""
LakshApp - Stay Focused and Motivated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced TO-DOs and Project Management integrated with Live Sessions, Music and more for Focus and Productivity

Author: DevInfinix
Copyright: (c) 2024-present DevInfinix
License: Apache-2.0
Version: 1.0.0
"""

import os
import platform

class AppData:
    """
    Class to manage data directory and database path for cross-platform applications.
    """

    def __init__(self, app_name, file_name):
        """
        Initializes the class with the application name and database filename.
        """
        self.app_name = app_name
        self.file_name = file_name

    def get_data_dir(self):
        """
        Gets the appropriate data directory based on the operating system.
        """
        if platform.system() == "Linux":
            return os.path.join(os.path.expanduser("~"), f".{self.app_name}", "data")
        elif platform.system() == "Darwin":  # macOS
            return os.path.join(os.environ["HOME"], "Library", "Application Support", self.app_name, "data")
        elif platform.system() == "Windows":
            return os.path.join(os.environ["APPDATA"], self.app_name, "data")
        else:
            raise Exception("Unsupported operating system")

    def create_data_dir_if_needed(self):
        """
        Creates the data directory if it doesn't exist.
        """
        data_dir = self.get_data_dir()
        os.makedirs(data_dir, exist_ok=True)

    def get_file_path(self):
        """
        Returns the full path to the database file.
        """
        self.create_data_dir_if_needed()
        return os.path.join(self.get_data_dir(), self.file_name)
