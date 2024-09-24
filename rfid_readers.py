from typing import Union
from pirc522 import RFID
import yaml
from RPi.GPIO import cleanup

class UIDFileReader:
    """Relates cards to custom strings by reading their UIDs and via a lookup file."""
    def __init__(self):
        self.rdr = RFID(pin_irq=18)
        self.filename = 'db.yaml'
        
        # Load the UID lookup file
        try:
            with open(self.filename, 'r') as file:
                self.uid_db = yaml.safe_load(file)
        except FileNotFoundError:
            self.uid_db = {}

    def _save_uid_db(self):
        """Save the UID lookup file."""
        with open(self.filename, 'w+') as file:
            yaml.dump(self.uid_db, file)
        
    def _wait_for_uid(self) -> str:
        """Wait for a card to be present and return its UID as a string."""
        self.rdr.wait_for_tag()
        (error, tag_type) = self.rdr.request()
        if not error:
            (error, uid) = self.rdr.anticoll()
            if not error:
                # return int.from_bytes(uid, byteorder='big')
                return ''.join([f'{x:02x}' for x in uid])
        return None
    
    def read(self) -> str:
        """Get the custom string associated with a card."""
        uid = self._wait_for_uid()
        if uid is None:
            return ''
        return self.uid_db.get(uid, '')
    
    def write(self, custom_str: str):
        """Associate a card with a custom string."""
        uid = self._wait_for_uid()
        if uid is None:
            return
        self.uid_db[uid] = custom_str
        self._save_uid_db()
        
    def cleanup(self):
        """Cleanup the GPIO pins."""
        cleanup()
