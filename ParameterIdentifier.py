import copy
import sys
import json
import multiprocessing
from collections import OrderedDict
import pandas as pd
from scipy.stats import chi2
import numpy as np
import os
import logging as lg
import tellurium as te
import tester_Fit_Model

sys.path.insert(0, '../Parameter_Sampler/')
import Estimator


class ParameterIdentifier:

    def __init__(self, model_name, p_estimation_results):

        self.obj_model = tester_Fit_Model(model_name)
        self.obj_model.load_parameters(0)
        self.estimation_results = p_estimation_results

        self.p_esti_results = p_estimation_results[1]
        self.p_space = self.obj_model.parameters
        self.par_values = None
        
        self.profiling_results = None

    def single_estimation_run(self, fixed_para, fixed_para_val):

        # Build general estimation model 
        self.obj_model.mke_test_dict()
        
        self.obj_model.set_settings()

        # Set fixed parameter
        estimation_space = {i: self.p_space[i]
                            for i in self.p_space if i != fixed_para}                   
        self.obj_model.model.setValue(fixed_para, fixed_para_val)
        model_fixed_par = te.loada(self.obj_model.model.getCurrentAntimony())
        
        # Set estimation model with fixed parameter 
        self.obj_model.model = model_fixed_par
        self.obj_model.parameters = estimation_space

        try:
            esta = Estimator.ParameterEstimator()
            esta.initialize(self.obj_model.objective,
                            self.obj_model.parameters
                            )
            score_para = esta.run(**self.obj_model.settings)
            del esta
        except RuntimeError:
            score_para = np.nan

        return score_para

    def get_profile_likelihood(self, fixed_parameter, n=5):
        
        if self.par_values is None:
            self.get_par_value_list(fixed_parameter, n)
        pool = multiprocessing.Pool(len(self.par_values))
        name_values = [(fixed_parameter, val) for val in self.par_values]
        results = pool.starmap(self.single_estimation_run, name_values)
        self.profiling_results = results
        pool.close()
    
    #TODO use the whole parameter space right selection for me?
    def get_par_value_list(self, fixed_parameter, n):
        space_for_param = self.p_space[fixed_parameter]
        if space_for_param[2]:
            log_par_values = np.linspace(np.log10(space_for_param[0]),
                                         np.log10(space_for_param[1]),
                                         n)
            par_values = 10**log_par_values
        else:
            par_values = np.linspace(space_for_param[0], space_for_param[1], n)
        self.par_values = par_values
