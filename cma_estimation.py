import json
import time
import os
import roadrunner as rr
import tellurium as te
import pandas as pd
import numpy as np
import tester_Fit_Model
import sys
sys.path.insert(0, '../Parameter_Sampler/')
import Estimator


def get_parameters(self_para_adjust, datapath_p):
    """
    Function to get the parameters, which are fitted with their boundaries
    ----------
    Parameters
    ----------
    self_para_adjust: bool
        for multiple runs of estimator or when parameters self adjusted
        determines which parameter txt file used
    datapath_p: string
        path to parameter .txt file, jsond dict file keys=names, values=value
    ---------
    returns p_keys: list
        list of parameter names to be fitted
    """
    try:
        if self_para_adjust == 0:

            print("Deleting Parameterset!")
            os.remove(datapath_p + "whole_paras.txt")

        with open(datapath_p + 'whole_paras.txt', 'rb') as handle:
            parametas = json.loads(handle.read())

    except FileNotFoundError:
        print('Using to_fit_parameter_set')
        try:
            with open(datapath_p + 'to_fit_para.txt', 'rb') as handle:
                parametas = json.loads(handle.read())            
        except:
            with open(datapath_p + 'to_fit_para.txt', 'r') as handle:
                parametas = json.loads(handle.read())

    return parametas


def metabolomics_test_dict(model, metabolites, timepoints=[]):
    """
    Function to create dict of metabolomics data from literature values
    -----------
    Parameters
    -----------
    model: te.model class
        tellurium model class, used to get species names of the model
    metabolites: pandas.DataFrame
        DataFrame of literature values except Alex Maier
    timepoints: list
        specifies time points for which data stored in test_dict
    -----------
    returns new_dict: dict
        test dict with correct data, each data literature value and it's std
    """
    # Factor to change DataFrame unit[partical number/cell] to [nmol/10^9 cells]
    # alex_factor = 602214.076  # avo/(10^9 cells and 10^9 nmol/mol
    # Translation dict keys=model_names, values=DataFrame_name
    long_name = {
        'Choline': 'avg Cho',
        'L_Serine': 'avg Ser',
        'Phosphatidylethanolamine': 'avg PE',
        'Phosphatidylcholine': 'avg PC'}
    value_dict = {
        'Choline': ['Choline_vo', 'Choline_t14'],
        'L_Serine': ['Serine_t14', 'Serine_vo'],
        'Phosphatidylethanolamine': ['PE_t09', 'PE_t14'],
        'Phosphatidylcholine': ['PC_t14', 'PC_t09']
    }
    # find matching values between dataframe and model
    intersection = list(set(metabolites.index) & set(model.getFloatingSpeciesIds()))

    work_df = metabolites.copy()
    model_names = intersection + [a for a in model.getFloatingSpeciesIds()
                                  if a in long_name]
    new_dict = {}
    stage_dict = {"uninfected": ['uRBC', 'Std.'],        # uninfected
                  "ring": None,                  # ring
                  "troph": ['Parasite', 'Std..1'],  # trophozoite
                  "schizont": None}                  # schizont

    for row in model_names:
        key = row
        if row in value_dict.keys():
            key = value_dict[row]

        new_dict[row] = {'values': [], 'std': []}
        for keys in timepoints:

            if stage_dict[keys] is None:
                new_dict[row]['values'].append([np.nan])
                new_dict[row]['std'].append([np.nan])

            else:
                values = work_df.loc[key, stage_dict[keys][0]].astype('float').tolist()
                stds = work_df.loc[key, stage_dict[keys][1]].tolist()
                # test whether if values is float, if true make a list
                if type(values) == float:
                    values = [values]
                    stds = [stds]

                new_dict[row]['values'].append(values)
                new_dict[row]['std'].append(stds)

    # parasite_vol = np.array([4.00**-1 * 1e-3, 26.7**-1 * 1e-3, 26.9**-1 * 1e-3])
    # extract the avs and give proper names

    return new_dict


def mke_test_dict(model, maierframe, metabolites, 
                  timepoints=["uninfected", "ring", "troph", "schizont"]):
    """
    Function to create test_dict for objective function
    -----------
    Parameters
    -----------
    model: te.model class
        tellurium model class, used to get species names of the model
    maierframe: pd.DataFrame
        DataFrame of experimental data Alex Maier
    metabolites: pandas.DataFrame
        DataFrame of literature values except Alex Maier
    """
    long_name_to_maier = {
        '1,2-Diacyl-sn-glycerol': 'DG',
        'DAG': 'DG',
        'Phosphatidylserine_mem': 'PS',
        'Phosphatidylethanolamine_mem': 'PE',
        'Phosphatidylcholine_mem': 'PC'}

    stage_dict = {"uninfected": ['RBC1', 'RBC2', 'RBC3'],
                  "ring": ['Ring 1', 'Ring 2', 'Ring 3'],
                  "troph": ['Trophozoite 1', 'Trophozoite 2', 'Trophozoite 3'],
                  "schizont": ['Schizont 1', 'Schizont 2', 'Schizont 3']}

    # now we make datadf
    work_df = maierframe.copy()
    work_df = work_df.loc[[long_name_to_maier[a]
                           for a in model.getFloatingSpeciesIds()
                           if a in long_name_to_maier]]
    # todo: clever weighting and such
    # parasite_vol = np.array([4.00**-1 * 1e-3, 26.7**-1 * 1e-3, 26.9**-1 * 1e-3])
    # extract the avs and give proper names
    new_dict = {}
    # todo: clever weighting and such
    maier_to_long_name = {v: k for k, v in long_name_to_maier.items()}
    for row in work_df.index:
        model_name = maier_to_long_name[row]

        new_dict[model_name] = {'values': [], 'std': []}
        for key in timepoints:
            values = work_df.loc[row, stage_dict[key]].tolist()
            stds = [work_df.loc[row, stage_dict[key]].std()] * len(values)

            new_dict[model_name]['values'].append(values)
            new_dict[model_name]['std'].append(stds)

    metas_dict = metabolomics_test_dict(model, metabolites, timepoints)

    new_dict.update(metas_dict)

    return new_dict


def set_model_parameters(model, params, excluded_values=[]):
    no_names = excluded_values
    for param_id in params.keys():
        if any(x in param_id for x in no_names):
            continue
        else:
            try:
                model[param_id] = params[param_id]
                # print(param_id)
                # print(model[param_id])
            except RuntimeError:
                print('could not set parameter : {0}'.format(param_id))
            except TypeError:
                # print('try to set {0} to {1}'.format(model[param_id]),params[param_id])
                print(format(model[param_id]))  #
                print(format(params[param_id]))
    return model


def simulation_run(model, parameter: dict):

    model.resetToOrigin()
    model = set_model_parameters(model, parameter)
    rr.Logger.disableConsoleLogging()
    sim_results = model.simulate(0, 48 * 3600, 3600)

    return sim_results


def simulation_to_dict(simulation_result_p):

    s_panda = simulation_result_p

    u_time = 2 * 3600
    ring_time = 8 * 3600
    troph_time = 36 * 3600
    schiz_time = 48 * 3600

    measure_points = [u_time, ring_time, troph_time, schiz_time]
    # find most similar timepoint in simulation_results
    can = []
    for item in measure_points:
        can.append(min(s_panda['time'], key=lambda x: abs(x - item)))

    # cut df to size of the matching time points
    s_panda = s_panda[s_panda['time'].isin(can)]

    # dict with molecule names as keys and value is list of values at the specified timepoints
    return s_panda.drop('time', axis=1).to_dict('list')


def simulation_to_panda(model, simulation_result, col=['time']):
    return pd.DataFrame(simulation_result, columns=col
                        + model.getFloatingSpeciesIds())


def compute_sqd_distance(simulation_result_dict, data, factor=10**1,
                         normalized=True):

    # list of intersecting keys, as only those relevant
    inter = simulation_result_dict.keys() & data.keys()

    dist_ar = np.zeros(len(inter))

    alex_bias_lst = ['DAG', 'Phosphatidylserine_mem',
                     'Phosphatidylethanolamine_mem', 'Phosphatidylcholine_mem']

    for ar_pos, molecule in enumerate(inter):
        if molecule == 'time':
            continue
        dist = 0.

        bias_fac = 1
        if molecule in alex_bias_lst:
            bias_fac = 2
        # iterate through the measured timepoints, thus finer evaluation of fit
        for i, values in enumerate(data[molecule]['values']):
            for pos, value in enumerate(values):
                # data entries empty as no literature value found, thus skipped
                if np.isnan(value):
                    continue
                if normalized:
                    dist += np.nansum(((value
                            - simulation_result_dict[molecule][i])**2  # noqa: E128
                            * bias_fac)  # noqa:E128
                            / data[molecule]['std'][i][pos]**2)   # noqa: E128

                else:
                    dist += np.nansum(bias_fac*(value
                            - simulation_result_dict[molecule][i])**2)  # noqa:E128
        dist_ar[ar_pos] = dist * factor

    return dist_ar


def constrain_concentration(species_timecourse, factor=10**-1):
    """
    check whether [s] < 1.0
    :param species_timecourse: timecourse for chosen species
    :param factor: badness of negative growth
    :return: number of species which have neg growth * factor
    """
    bool_constrain = species_timecourse < 1.0

    too_high_constrain = bool_constrain.any().sum()
    return too_high_constrain * factor


def check_zero(species_timecourse, factor=10**-1):
    """
    check whether [s] >= 0
    :param species_timecourse: timecourse for chosen species
    :param factor: badness of negative growth
    :return: number of species which have neg growth * factor
    """

    bool_growthdf = species_timecourse.iloc[:] < 0
    # no. of species w negative growth, +1 per species
    decreasing_growth = bool_growthdf.any().sum()
    return decreasing_growth * factor


def check_growth(species_timecourse, factor=10**-1):
    """
    check whether d[s]/dt >= 0
    :param species_timecourse: timecourse for chosen species
    :param factor: badness of negative growth
    :return: number of species which have neg growth * factor
    """
    diffdf = (species_timecourse.iloc[1:].values -
              species_timecourse.iloc[:-1])  # delta x

    bool_growthdf = diffdf < 0
    # no. of species w negative growth, +1 per species
    decreasing_growth = bool_growthdf.any().sum()
    return decreasing_growth * factor


def objective_function(parameter: dict, model, t_data: dict, process_id,
                       weight=1):

    try:

        res = simulation_run(model, parameter)

    except RuntimeError:
        # print('Error simulating model for parameters %s' %parameter)
        return np.nan

    res_p = simulation_to_panda(model, res)

    dic_results = simulation_to_dict(res_p)

    sqd_dis_ar = compute_sqd_distance(dic_results, t_data)

    objective_value = sqd_dis_ar.sum() + sqd_dis_ar.std() * weight
    # list of intersecting keys, as only those relevant
    # inter = dic_results.keys() & t_data.keys()
    # score_growth = check_growth(res_p[inter])
    # score_zero = check_zero(res_p)
    # score_conc = constrain_concentration(res_p)

    return objective_value  # + score_zero  # + score_growth


def steady_state_calc(model, parameter: dict):

    model.resetToOrigin()
    model = set_model_parameters(model, parameter)
    rr.Logger.disableConsoleLogging()
    try:
        # model.conservedMoietyAnalysis = True
        score = model.steadyState()
    except RuntimeError:
        return False, model

    return score, model


def objective_steady_state_function(parameter: dict, model, t_data: dict, process_id,
                                    weight=1):

    ss_found, model_in_SS = steady_state_calc(model, parameter)
    if not ss_found:
        return 1e30

    else:
        try:
            res = model_in_SS.simulate()
            res_p = simulation_to_panda(model, res)

            dic_results = res_p[-1::].to_dict('list')

            sqd_dis_ar = compute_sqd_distance(dic_results, t_data)

            objective_value = sqd_dis_ar.sum() + sqd_dis_ar.std() * weight
        except RuntimeError:
            objective_value = 1e30

        return objective_value


if __name__ == '__main__':
    options = {1: "cPL_conc",
               2: "noV_cPL_conc",
               3: "pc_pe_PL",
               4: "PLModel",
               5: "SS_PLModel_ConKin",
               6: "SS_PLModel_E_MA",
               7: "SS_PLModel_MA",
               8: "SS_PLModel_MM"}

    entry = sys.argv[1]
    run_id = sys.argv[2]
    timepoint_lst = list(sys.argv[3])
    print(options)

    # entry = input("Name of the model to use: ")

    try:
        name = options[int(entry)]

    except:
        name = str(entry)

    print(name)

    to_fit_model = tester_Fit_Model.Fit_Model(name)
    tester_Fit_Model.timepoints = timepoint_lst
    to_fit_model.mke_test_dict()

    datapath = to_fit_model.datapath
    timestr = time.strftime("%Y%m%d-%H:%M:%S")

    to_fit_model.load_parameters(0)

    ps = {'PS': 500.0}
    to_fit_model.extra_species_amount = ps

    ps_test = {'Phosphatidylserine': {'values': [[500.0]],
               'std': [[200.0]]}
               }
    to_fit_model.set_species_test_dict(ps_test)    

    esta = Estimator.ParameterEstimator()
    esta.initialize(to_fit_model.objective,
                    to_fit_model.parameters
                    )

    to_fit_model.set_settings()

    score_para = esta.run(**to_fit_model.settings)
    score_para.append(timepoint_lst)
    
    with open(datapath + timestr + run_id + 'whole_paras.json', 'w') as handle:
        json.dump(score_para, handle, indent=4)
