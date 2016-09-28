import infermedica_api
infermedica_api.configure(app_id='9cdabea1', app_key='787e7a0d2819c0c8d814386f8cc91ddf')

class ConvoBot(object):

    def __init__(self):
        self.age = None
        self.gender = None
        self.init_symptom = None
        self._state = None

        self.med_api = infermedica_api.get_api()
        self.current_diagnosis = None

    def _get_state(self):
        pass

    def greet(self):
        return "Hello!"

    def ask_init_symptom(self):
        return "What are your symptoms?"
    
    def ask_gender(self):
        return "What is your gender?"
    
    def ask_age(self):
        return "What is your age?"

    def speak(self, msg):
        '''Respond to message
        '''
        print msg
        print self.age
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
            print self._symps

        if "SYMPTOM_SEARCH" in self._state:
            if self._sym_i == len(self._symps):
                self._state = "DIAGNOSIS_END"
                return self.speak(msg)

            if self._state == 'SYMPTOM_SEARCH':
                sym = self._symps[self._sym_i]
                self._state = 'SYMPTOM_SEARCH:SYMPTOM_ANSWER'
                result = self.med_api.symptom_details(sym['id'])
                return result.question
            
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
            print self.diagnosis
            final_diagnosis = self.med_api.diagnosis(self.diagnosis)
            condition = final_diagnosis.conditions[0]['name']
            return "You may have {}. Please see a doctor.".format(condition)
            
        return "UNCAUGHT STATE!! Your message is {} characters long".format(len(msg))

    def get_next_question(self):
        pass

    def continue_diagnosis(self):
        pass

medbot = ConvoBot()
