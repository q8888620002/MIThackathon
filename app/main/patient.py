import os
import cPickle as pickle


DATA_STORE_DIR = os.path.join(os.getcwd(), '__patient_data__')
if not os.path.exists(DATA_STORE_DIR):
    os.makedirs(DATA_STORE_DIR)
print DATA_STORE_DIR


def get_patient(_id=None):
    # Try to restore saved
    p = Patient(_id)


class Patient(object):
    '''A class representing a patient
    '''
    def __init__(self, _id):
        # Unique id (NHS id)
        self._id = _id

        # Name
        self.name = None
        # Gender
        self.gender = None
        # Age 
        self.age = None

        # List of symptoms (infermedica symptom ids)
        self._symptoms = None
        # List of conditions (infermedica condition ids)
        self._conditions = None

        # User provided location
        self.location = None
        # User location (lat, lng)
        self._location = None

    @property
    def _chatlog_path(self):
        path = os.path.join(DATA_STORE_DIR, self._id, 'chat')
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        return path

    def append_chatlog(self, text):
        with open(self._chatlog_path, 'a+') as f:
            f.write("{}\n".format(text))
            
    @property
    def _savepath(self):
        path = os.path.join(DATA_STORE_DIR, self._id, 'obj')
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        return path
    
    def save(self):
        with open(self._savepath, 'wb') as f:
            pickle.dump(self, f)
