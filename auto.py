from __future__ import print_function

import infermedica_api 

infermedica_api.configure(app_id='9cdabea1', app_key='787e7a0d2819c0c8d814386f8cc91ddf')

## method that search for the given symptom 
def search_symptoms(current_diagnosis, symptom):

    request =  api.search(symptom, sex = gender)
    
    for sym in request:
        result = api.symptom_details(sym['id'])

        answer = input(result.question+': ')
        if answer == "yes":
            current_diagnosis.add_symptom(sym['id'],'present')
        else:
            current_diagnosis.add_symptom(sym['id'],'absent')

    other_symptom = input('Do you have any other symptoms ? yes or no: ')

    ## if the patient has another symptoms call this function recursively  ##

    if other_symptom == "yes":
        other_symptom = input("what's your symptoms beside "+ symptom + ":")

        current_diagnosis = search_symptoms(current_diagnosis, other_symptom)

    return current_diagnosis
## method that ask if the patient has anotehr symptoms 


if __name__ == '__main__':
    api = infermedica_api.get_api()
    user_symptom = input("what's your symptoms: ")
    gender = input("what's your gender? : ")
    age = input("what's your age? :")
    
   ## init a diagnosis object ##

    diagnosis = infermedica_api.Diagnosis(sex=gender, age=age)

    ## get the result ##

    final_diag = search_symptoms(diagnosis, user_symptom)

    final_diag = api.diagnosis(final_diag)

    print("You may get "+final_diag.conditions[0]['name']
            + " with probability of "+ str(final_diag.conditions[0]['probability']) )

