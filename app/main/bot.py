#-*- coding: utf-8 -*-

#import infermedica_api
import infermedica_api
from flask import session
from flask_socketio import emit


import googlemaps
import diagnosis

infermedica_api.configure(app_id='9cdabea1', app_key='787e7a0d2819c0c8d814386f8cc91ddf')

class ConvoBot(object):

    def __init__(self):
        self.age = None
        self.gender = None
        self.init_symptom = None
        self._state = None

        self.med_api = infermedica_api.get_api()
        self.current_diagnosis = None

        self.gmaps = googlemaps.Client(key='AIzaSyCO_q7P79_HQmnApoRlhWi_-3cRwzd86A8')

        self.user_location = None

    def _get_state(self):
        pass

    def set_gender(self,gender):
        self.gender = gender
        return "Your gender is <strong>" + gender+"<strong/>"

    def greet(self ):
        return "Hello! "

    def ask_user_location(self):
        return "Where would you like me to start my search for clinics? (e.g. workplace, home)"

    def get_nearby_clinics(self, location=None, clinic_type='clinic'):
        if not location:
            location = self.user_location
        res = self.gmaps.places_nearby(location=self.user_location, radius=5000, keyword=clinic_type)
        names = '\n'.join([x['name'].encode('utf-8') for x in res['results']])
        self._nearby_clinics = res['results']
        return names 


    def ask_init_symptom(self):
        return "Okay, Now tell me about your symptoms."

    def ask_gender(self):
        return "What is your gender?"
    
    def ask_age(self):
        return "How old are you?"

    def ask_clinic(self, place_id):
        place_info = self.gmaps.place(place_id)['result']
        key_label = [('name', 'Name'),
                     ('formatted_address', 'Address'),
                     ('formatted_phone_number', 'Phone'),
                     ('website', 'Website')]
        s = []
        for k, l in key_label:
            try:
                value = place_info[k]
            except KeyError:
                continue
            s.append(u'{label}: {value}'.format(label=l, value=value))   
        s = u'\n'.join(s)
        
        question = u"Would you like to make an appointment at this clinic?\n{}".format(s)
        return question


    def speak(self, msg, state=None):
        '''Respond to message
        '''

        if state is not None:
            self._state = state
            return self.speak(msg)

        if self._state == 'SELECTED_CLINIC':
            self._state = 'ASKING_CLINIC'
            self._clinic = msg
            return self.ask_clinic(place_id=msg)

        if self._state == 'ASKING_CLINIC':
            if msg.lower() in ['y', 'yes', 'yep', 'true']:
                self._state = 'FINISHED'    
                return "Appointment made!"
            else:
                self._clinic = None
                self._state = None
                return ''

        if self.age is None:
            if self._state == "ASKING_AGE":
                try:
                    self.age = int(msg)
                except ValueError:
                    self.age = None
                    return self.ask_age()
                else:
                    self._state = None
            else:
                self._state = "ASKING_AGE"
                return self.ask_age()

        while self.gender is None:
            if self._state == "ASKING_GENDER":
                try:
                    self.gender = msg
                except ValueError:
                    self.gender = None
                    return self.ask_gender()
                else:
                    self._state = None
            else:
                self._state = "ASKING_GENDER"
                return self.ask_gender()

        while self.init_symptom is None:
            if self._state == "ASKING_INIT_SYMPTOM":
                try:
                    self.init_symptom = msg
                except ValueError:
                    self.init_symptom = None
                    return self.ask_init_symptom()
                else:
                    self._state = None
            else:
                self._state = "ASKING_INIT_SYMPTOM"
                return self.ask_init_symptom()
       
        # Start inquiry
        if self._state is None:
            self.diagnosis = infermedica_api.Diagnosis(sex=self.gender,
                                                       age=self.age)
            request = self.med_api.search(self.init_symptom,
                                          sex=self.gender)

            self._state = "SYMPTOM_SEARCH"
            self._symps = request
            self._sym_i = 0

        if "SYMPTOM_SEARCH" in self._state:
            if self._sym_i == len(self._symps):
                self._state = "DIAGNOSIS_END"
                return self.speak(msg)

            if self._state == 'SYMPTOM_SEARCH':
                sym = self._symps[self._sym_i]
                self._state = 'SYMPTOM_SEARCH:SYMPTOM_ANSWER'
                result = self.med_api.symptom_details(sym['id'])
                if result.question:
                    return result.question
                else:
                    return "Do you sometimes have {}?".format(result.name.lower())
            
            elif 'SYMPTOM_ANSWER' in self._state:
                sym = self._symps[self._sym_i]
                self._sym_i += 1
                if msg.lower() in ['y', 'yes', 'yep', 'true']:
                    self.diagnosis.add_symptom(sym['id'], 'present')
                else:
                    self.diagnosis.add_symptom(sym['id'], 'absent')
                self._state = 'SYMPTOM_SEARCH'
                return self.speak(msg)

        if self._state == 'DIAGNOSIS_END':
            final_diagnosis = self.med_api.diagnosis(self.diagnosis)
            self.final_diagnosis = final_diagnosis
            self._state = 'RECOMMEND_CLINIC'
            return self.speak(msg)

        if self._state == 'RECOMMEND_CLINIC':
            if not self.user_location:
                self._state = 'GET_LOCATION'
                return self.speak(msg)

            condition = self.final_diagnosis.conditions[0]['name']

            specialty = diagnosis.clinics.get(condition)
            if specialty is None:
                for k, v in diagnosis.iteritems():
                    if condition in k.lower():
                        specialty = v
                        break
            self._state = 'FINISHED'

            clinic_names = str(self.get_nearby_clinics(clinic_type=specialty))
            places = self._nearby_clinics
            center = {'lat': self.user_location[0],
                      'lng': self.user_location[1]}
            room = session.get('room')
            emit('showmap', {'center': center, 'places': places}, room=room)
            return "You probably have "+ condition+". I can refer you to a {} clinic.\n(Clinics shown on the map.)".format(specialty)
            
        if self._state == 'GET_LOCATION':
            self._state = 'GET_LOCATION:ASKED'
            return self.ask_user_location()

        if self._state == 'GET_LOCATION:ASKED':
            msg = msg.strip().strip('(').strip(')').replace(',', ' ')
            lat, lng = msg.split()
            self.user_location = (float(lat), float(lng))
            self._state = 'RECOMMEND_CLINIC'
            return "OK"

        if self._state == 'FINISHED':
            pass
            
        return "UNCAUGHT STATE!! Your message is {} characters long".format(len(msg))

medbot = ConvoBot()
