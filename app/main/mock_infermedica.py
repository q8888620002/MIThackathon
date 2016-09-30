#A mock module to use in place of infermedica_api
null = None
def get_api():
    return MockAPI()

def Diagnosis(*args, **kwargs):
    return MockDiagnosisObject(*args, **kwargs)

def configure(*args, **kwargs):
    pass

class ExposedDict(dict):
    """Container object for datasets

    Dictionary-like object that exposes its keys as attributes.

    >>> b = Bunch(a=1, b=2)
    >>> b['b']
    2
    >>> b.b
    2

    """

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)


class MockAPI(object):
    def search(self, phrase, sex=None):
        return [{u'id': u's_385', u'label': u'bleeding skin'},
                {u'id': u's_111', u'label': u'bleeding gums'},
                {u'id': u's_1170', u'label': u'bleeding into joints'},
                {u'id': u's_1386', u'label': u'bleeding into muscles'},
                {u'id': u's_152', u'label': u'bleeding after sex'},
                {u'id': u's_115', u'label': u'bleeding from anus'},
                {u'id': u's_1440', u'label': u'bleeding between periods'},
                {u'id': u's_151', u'label': u'bleeding after menopause'}]

    def symptom_details(self, _id):
        for d in _symptoms:
            if d.id == _id:
                return d

    def diagnosis(self, diagnosis_request, case_id=None):
        return _diagnosis

class MockDiagnosisObject(object):
    def __init__(self, sex, age):
        self.sex = sex
        self.age = age

    def add_symptom(self, _id, state, time=None):
        pass

_symptoms = [ExposedDict(**{
    "category": "Signs and symptoms", 
    "children": [], 
    "extras": {}, 
    "id": "s_385", 
    "image_source": null, 
    "image_url": null, 
    "name": "Dry cracked skin, sometimes bleeds", 
    "parent_id": "s_241", 
    "parent_relation": "character", 
    "question": "Do you sometimes have dry, cracked skin that occasionally bleeds?", 
    "sex_filter": "both"
}),
ExposedDict(**{
    "category": "Signs and symptoms", 
    "children": [], 
    "extras": {}, 
    "id": "s_111", 
    "image_source": null, 
    "image_url": null, 
    "name": "Bleeding gums", 
    "parent_id": null, 
    "parent_relation": null, 
    "question": "Do your gums bleed?", 
    "sex_filter": "both"
}),
ExposedDict(**{
    "category": "Signs and symptoms", 
    "children": [], 
    "extras": {}, 
    "id": "s_1170", 
    "image_source": null, 
    "image_url": null, 
    "name": "Bleeding into joints", 
    "parent_id": null, 
    "parent_relation": null, 
    "question": null, 
    "sex_filter": "both"
}),
ExposedDict(**{
    "category": "Signs and symptoms", 
    "children": [], 
    "extras": {}, 
    "id": "s_1386", 
    "image_source": null, 
    "image_url": null, 
    "name": "Bleeding into muscles", 
    "parent_id": null, 
    "parent_relation": null, 
    "question": null, 
    "sex_filter": "both"
}),
ExposedDict(**{
    "category": "Signs and symptoms", 
    "children": [], 
    "extras": {}, 
    "id": "s_152", 
    "image_source": null, 
    "image_url": null, 
    "name": "Bleeding after intercourse", 
    "parent_id": null, 
    "parent_relation": null, 
    "question": "Do you have bleeding after intercourse?", 
    "sex_filter": "female"
}),
ExposedDict(**{
    "category": "Signs and symptoms", 
    "children": [], 
    "extras": {}, 
    "id": "s_115", 
    "image_source": null, 
    "image_url": null, 
    "name": "Bleeding from anus", 
    "parent_id": null, 
    "parent_relation": null, 
    "question": "Have you noticed bleeding from your anus or near your anus?", 
    "sex_filter": "both"
}),
ExposedDict(**{
    "category": "Signs and symptoms", 
    "children": [
        {
            "id": "s_1217", 
            "parent_relation": "character"
        }
    ], 
    "extras": {}, 
    "id": "s_1440", 
    "image_source": null, 
    "image_url": null, 
    "name": "Irregular menstruations", 
    "parent_id": null, 
    "parent_relation": null, 
    "question": "Do you have irregular (less than 21 or more than 35 days between) menstrual cycles?", 
    "sex_filter": "female"
}),
ExposedDict(**{
    "category": "Signs and symptoms", 
    "children": [], 
    "extras": {}, 
    "id": "s_151", 
    "image_source": null, 
    "image_url": null, 
    "name": "Postmenopausal vaginal bleeding", 
    "parent_id": null, 
    "parent_relation": null, 
    "question": "Have you had vaginal bleeding after menopause?", 
    "sex_filter": "female"
})]

_diagnosis = ExposedDict(**{
    "case_id": null, 
    "conditions": [
        {
            "id": "c_147", 
            "name": "Hemorrhoids", 
            "probability": 0.1129
        }, 
        {
            "id": "c_113", 
            "name": "Diverticulosis", 
            "probability": 0.0549
        }, 
        {
            "id": "c_275", 
            "name": "Anal fissure", 
            "probability": 0.0133
        }, 
        {
            "id": "c_276", 
            "name": "Anal cancer", 
            "probability": 0.0055
        }
    ], 
    "evaluation_time": null, 
    "extras": {}, 
    "extras_permanent": {}, 
    "lab_tests": [], 
    "patient_age": 30, 
    "patient_sex": "female", 
    "pursued": [], 
    "question": {
        "extras": {}, 
        "items": [
            {
                "choices": [
                    {
                        "id": "present", 
                        "label": "Yes"
                    }, 
                    {
                        "id": "absent", 
                        "label": "No"
                    }, 
                    {
                        "id": "unknown", 
                        "label": "Don't know"
                    }
                ], 
                "id": "s_249", 
                "name": "Itching around anus"
            }
        ], 
        "text": "Do you have itching around your anus?", 
        "type": "single"
    }, 
    "risk_factors": [], 
    "symptoms": [
        {
            "choice_id": "absent", 
            "id": "s_385"
        }, 
        {
            "choice_id": "absent", 
            "id": "s_111"
        }, 
        {
            "choice_id": "absent", 
            "id": "s_1170"
        }, 
        {
            "choice_id": "absent", 
            "id": "s_1386"
        }, 
        {
            "choice_id": "absent", 
            "id": "s_152"
        }, 
        {
            "choice_id": "present", 
            "id": "s_115"
        }, 
        {
            "choice_id": "absent", 
            "id": "s_1440"
        }, 
        {
            "choice_id": "absent", 
            "id": "s_151"
        }
    ]
})
