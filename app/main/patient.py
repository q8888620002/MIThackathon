import os
import json
import cPickle as pickle


DATA_STORE_DIR = os.path.join(os.getcwd(), '__patient_data__')
if not os.path.exists(DATA_STORE_DIR):
    os.makedirs(DATA_STORE_DIR)
print DATA_STORE_DIR


def get_patient(_id):
    # Try to restore saved
    p = Patient(_id)
    try:
        p.restore()
    except IOError as e:
        print e
    return p

def get_all_patients():
    res = []
    for _id in os.listdir(DATA_STORE_DIR):
        res.append(get_patient(_id))
    return res

class Patient(object):
    '''A class representing a patient
    '''

    attributes = ['name', 'gender', 'age', '_diagnosis',
                  'location', '_location']
    def __init__(self, _id):
        # Unique id (NHS id)
        self._id = _id

        # Name
        self.name = None
        # Gender
        self.gender = None
        # Age 
        self.age = None

        # Infermedica diagnosis object as dict
        self._diagnosis = None

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
            
    def get_chatlog(self):
        with open(self._chatlog_path, 'a+') as f:
            text = f.read()
        return text

    @property
    def _savepath(self):
        path = os.path.join(DATA_STORE_DIR, self._id, 'obj')
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        return path
    
    def restore(self):
        with open(self._savepath, 'rb') as f:
            d = json.load(f)

        for a in self.attributes:
            setattr(self, a, d[a])

    def save(self):
        d = {a: getattr(self, a) for a in self.attributes}

        with open(self._savepath, 'wb') as f:
            json.dump(d, f)
