import os
from pathlib import Path
from sys import _getframe
from typing import Iterator
import json
from logging import getLogger

logger = getLogger()


class Config:
    """A class for handling configuration settings for the aiomql package.

    Keyword Args:
        **kwargs: Configuration settings as keyword arguments.
        Variables set this way supersede those set in the config file.

    Attributes:
        record_trades (bool): Whether to keep record of trades or not.
        filename (str): Name of the config file
        records_dir (str): Path to the directory where trade records are saved
        win_percentage (float): Percentage of target profit to be considered a win
        login (int): Trading account number
        password (str): Trading account password
        server (str): Broker server
        path (str): Path to terminal file
        timeout (int): Timeout for terminal connection

    Notes:
        By default, the config class looks for a file named aiomql.json.
        You can change this by passing the filename keyword argument to the constructor.
        By passing reload=True to the load_config method, you can reload and search again for the config file.
    """
    login: int
    password: str
    server: str
    path: str
    timeout: int
    record_trades: bool
    filename: str
    win_percentage: float
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, **kwargs):
        self.login: int = kwargs.pop('login', 0)
        self.password: str = kwargs.pop('password', '')
        self.server: str = kwargs.pop('server', '')
        self.path: str = kwargs.pop('path', '')
        self.timeout: int = kwargs.pop('timeout', 60000)
        self.record_trades: bool = kwargs.pop('record_trades', True)
        self.filename: str = kwargs.pop('filename', 'aiomql.json')
        self.win_percentage: float = kwargs.pop('win_percentage', 0.85)
        self._load = 1
        self.records_dir = kwargs.pop('records_dir', (Path.home() / 'Documents' / 'Aiomql' / 'Trade Records'))
        self.records_dir.mkdir(parents=True, exist_ok=True)
        self.set_attributes(**kwargs)
        self.load_config(reload=False)
        
    @staticmethod
    def walk_to_root(path: str) -> Iterator[str]:
        
        if not os.path.exists(path):
            raise IOError('Starting path not found')
        
        if os.path.isfile(path):
            path = os.path.dirname(path)
        
        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir
    
    def find_config(self):
        current_file = __file__
        frame = _getframe()
        while frame.f_code.co_filename == current_file:
            if frame.f_back is None:
                return None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))
        
        for dirname in self.walk_to_root(path):
            check_path = os.path.join(dirname, self.filename)
            if os.path.isfile(check_path):
                return check_path
        return None
    
    def load_config(self, file: str = None, reload: bool = True):
        if not reload and self._load == 0:
            return

        self._load = 0

        if (file := (file or self.find_config())) is None:
            logger.warning('No Config File Found')
            return
        fh = open(file, mode='r')
        data = json.load(fh)
        fh.close()
        [setattr(self, key, value) for key, value in data.items()]

    def account_info(self) -> dict['login', 'password', 'server']:
        """Returns Account login details as found in the config object if available

           Returns:
               dict: A dictionary of login details
        """
        return {'login': self.login, 'password': self.password, 'server': self.server}
    
    def set_attributes(self, **kwargs):
        """Add attributes to the config object

        Keyword Args:
            **kwargs: Attributes to be added to the config object
        """
        [setattr(self, i, j) for i, j in kwargs.items()]
