import json
import xbmcvfs
import xbmcaddon
import os
from util import Logutil as log
from rcbexceptions import *
from file_scraper import FileScraper


class MAME_Scraper(FileScraper):
    """
    MAME_Scraper gets data from mame_full.json
    """
    _name = 'MAME'
    
    mame_data = {}
    _data_loaded = False

    def __init__(self):        
        self.load_mame_data()

    def load_mame_data(self, force_reload=False):        
        if self._data_loaded and not force_reload:
            return
        
        if self.path and xbmcvfs.exists(self.path):
            try:
                with xbmcvfs.File(self.path, "r") as f:
                    self.mame_data = json.load(f)
                log.info(f"MAME_Scraper: loaded {len(self.mame_data)} games from {self.path}")
                self._data_loaded = True
                return
            except Exception as e:
                log.error(f"MAME_Scraper: error reading {self.path}: {e}")
        
        addon = xbmcaddon.Addon("script.games.rom.collection.browser")
        addon_path = addon.getAddonInfo("path")
        addon_path = xbmcvfs.translatePath(addon_path)
        paths = [
            os.path.join(addon_path, "resources", "mame_full.json"),
            os.path.join(xbmcvfs.translatePath("special://profile/addon_data/script.games.rom.collection.browser/"), "mame_full.json")
        ]
        for path in paths:
            if xbmcvfs.exists(path):
                try:
                    with xbmcvfs.File(path, "r") as f:
                        self.mame_data = json.load(f)
                    log.info(f"MAME_Scraper: loaded {len(self.mame_data)} games from {path}")
                    self._data_loaded = True
                    return
                except Exception as e:
                    log.error(f"MAME_Scraper: error reading {path}: {e}")

        log.warn("MAME_Scraper: mame_full.json not found in any location.")
        self._data_loaded = True

    def search(self, gamename, platform=None):        
        if not self._data_loaded:
            self.load_mame_data()

        if gamename in self.mame_data:
            info = self.mame_data[gamename]            
            result = {
                'id': gamename,
                'Game': [info.get('title', gamename)],
                'ReleaseYear': [info.get('year', '')] if info.get('year') else [],
                'Publisher': [info.get('manufacturer', '')] if info.get('manufacturer') else [],
                'Developer': [info.get('manufacturer', '')] if info.get('manufacturer') else [],
                'Players': [info.get('players', '')] if info.get('players') else [],
                'Genre': [info.get('genre', '')] if info.get('genre') else [],
                'Description': [info.get('description', '')] if info.get('description') else [],
            }
            return [result]
        else:
            log.warn(f"MAME_Scraper: '{gamename}' JSON not found")
            return []

    def retrieve(self, gameid, platform):        
        if not self._data_loaded:
            self.load_mame_data()

        if gameid in self.mame_data:
            info = self.mame_data[gameid]
            result = {
                'Game': [info.get('title', gameid)],
                'ReleaseYear': [info.get('year', '')] if info.get('year') else [],
                'Publisher': [info.get('manufacturer', '')] if info.get('manufacturer') else [],
                'Developer': [info.get('manufacturer', '')] if info.get('manufacturer') else [],
                'Players': [info.get('players', '')] if info.get('players') else [],
                'Genre': [info.get('genre', '')] if info.get('genre') else [],
                'Description': [info.get('description', '')] if info.get('description') else [],
            }
            return result
        return {}