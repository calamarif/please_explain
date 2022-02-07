__author__ = 'Callum'
# -*- coding: utf-8 -*-
#Python 3.8
#please_explain.py - Generate explainability and feature effects
#Version: 0.1
#Date: 28th Jan 2022
################ USAGE OF THE  PROGRAM #####################################
# Short Description:
## Automatically gernerate the prediction explanations and feature effects of top model of each project

import sys, sched, time, datetime
import datarobot as dr

#*****************THESE ARE YO VARIABLES - YOU NEED TO EDIT THESE *******
# Set how frequently the Scheduler should run
scheduler_frequency_seconds = 86400
scheduler_time_setting = 1

# number of models to generatee explainations on
models_to_generate_explanations= 3
days_to_look_back = 180

#function to generate feature explanations and prediction explanations
def generate_fe_and_pe(dr):
    dr.Client(config_path = 'drconfig.yaml')
    project_list = dr.Project.list()
    counter_number_of_projects_kicked_off=0
    for project in project_list:
        print (project.id)
        delta = datetime.datetime.now() - project.created.replace(tzinfo=None)
        if delta.days < days_to_look_back:
            # get all models for a project
            models = project.get_models()
            #generate explanations for n top models:
            i = 0
            for model in models:
                if i < models_to_generate_explanations:
                    feature_effects = model.get_or_request_feature_effect(source='validation')
                    # Initialise prediction explanations
                    dr.PredictionExplanationsInitialization.create(project.id, model.id)
                    i += 1
            counter_number_of_projects_kicked_off+=1
    return counter_number_of_projects_kicked_off
        



########### Running the program below on a loop for specified time in variable:scheduler_frequency_seconds ################
def mainProgram(sc):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    projects_processed = generate_fe_and_pe(dr)    

    sc.enter(scheduler_frequency_seconds,scheduler_time_setting, mainProgram, (sc,))
s = sched.scheduler(time.time, time.sleep)
s.enter(scheduler_frequency_seconds,scheduler_time_setting,mainProgram, (s,))
s.run()

##########################################################################
### End of the program                                                ####
##########################################################################
