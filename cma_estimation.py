import pickle
import time
import os
import roadrunner as rr
import tellurium as te
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../Parameter_Sampler/')
import Estimator


def get_parameter_keys(self_para_adjust, datapath):
    """
    Function to get the names of the parameters, which are fitted
    ----------
    Parameters
    ----------
    self_para_adjust: bool
        for multiple runs of estimator or when parameters self adjusted
        determines which parameter txt file used
    datapath: string
        path to parameter .txt file, pickled dict file keys=names, values=value
    ---------
    returns p_keys: list
        list of parameter names to be fitted
    """
    try:
        if self_para_adjust == 0:

            print("Deleting Parameterset!")
            os.remove(datapath + "whole_paras.txt")

        with open(datapath + 'whole_paras.txt', 'rb') as handle:
            parametas = pickle.loads(handle.read())

    except FileNotFoundError:
        print('Using to_fit_parameter_set')
        with open(datapath + 'to_fit_para.txt', 'rb') as handle:
            parametas = pickle.loads(handle.read())

    p_keys = []

    for item in parametas.items():
        p_keys.append(item[0])

    return p_keys


def mk_bounds(parameter_names, log):

    param_bound = {}

    # here define bounds for the fitted params by their type
    for key in parameter_names:
        if key.startswith('E'):  # enzyme number bounds
            if log:
                param_bound[key] = (-5.7, 6, log)  # for log space
            else:
                param_bound[key] = (1.6605e-06, 1e6, log)  # for linear space
        if key.startswith('k'):  # mass action k bounds
            if log:
                param_bound[key] = (-10, 13, log)  # for log space
            else:
                param_bound[key] = (0, 1e13, log)  # for linear space
        if key.startswith('t12'):  # sigmoid half time, want betw 20 & 35h
            if log:
                param_bound[key] = (1.3, 5.1, log)
            else:
                param_bound[key] = (20 * 3600, 40 * 3600, log)
        if key.startswith('cm'):  # sigmoid max and min what do i want?
            if log:
                param_bound[key] = (-5.7797, 6, log)
            else:
                param_bound[key] = (1.6605e-06, 1e6, log)
        if key.startswith('s_'):  # sigmoid slope, in s
            if log:
                param_bound[key] = (-3, 4.5, log)
            else:
                param_bound[key] = (0, 36000, log)

    return param_bound


def metabolomics_test_dict(model, metabolites):
    """
    Function to create dict of metabolomics data from literature values
    -----------
    Parameters
    -----------
    model: te.model class
        tellurium model class, used to get species names of the model
    metabolites: pandas.DataFrame
        DataFrame of literature values except Alex Maier
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
    stage_dict = {'uninfected': ['uRBC', 'Std.'],
                  'troph_time': ['Parasite', 'Std..1']}

    for row in model_names:
        key = row
        if row in value_dict.keys():
            key = value_dict[row]

        new_dict[row] = {'values': [], 'std': []}
        for keys in stage_dict.keys():
            values = work_df.loc[key, stage_dict[keys][0]].astype('float').tolist()
            stds = work_df.loc[key, stage_dict[keys][1]].tolist()
            # test if values is float, if true make a list
            if type(values) == float:
                values = [values]
                stds = [stds]

            new_dict[row]['values'].append(values)
            new_dict[row]['std'].append(stds)

    # parasite_vol = np.array([4.00**-1 * 1e-3, 26.7**-1 * 1e-3, 26.9**-1 * 1e-3])
    # extract the avs and give proper names
    print(new_dict)
    return new_dict


def mke_test_dict(model, maierframe, metabolites):
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

    stage_dict = {'u_time': ['RBC1', 'RBC2', 'RBC3'],
                  'ring_time': ['Ring 1', 'Ring 2', 'Ring 3'],
                  'troph_time': ['Trophozoite 1', 'Trophozoite 2', 'Trophozoite 3'],
                  'schiz_time': ['Schizont 1', 'Schizont 2', 'Schizont 3']}

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
        for key in stage_dict.keys():
            values = work_df.loc[row, stage_dict[key]].tolist()
            stds = [work_df.loc[row, stage_dict[key]].std()] * len(values)

            new_dict[model_name]['values'].append(values)
            new_dict[model_name]['std'].append(stds)

    metas_dict = metabolomics_test_dict(model, metabolites)

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


def simulation_to_panda(model, simulation_result):
    return pd.DataFrame(simulation_result, columns=['time']
                        + model.getFloatingSpeciesIds())


def compute_sqd_distance(simulation_result_dict, data, factor=10**1,
                         normalized=True):

    dist = 0.
    # list of intersecting keys, as only those relevant
    inter = simulation_result_dict.keys() & data.keys()
    alex_bias_lst = ['DAG', 'Phosphatidylserine_mem',
                     'Phosphatidylethanolamine_mem', 'Phosphatidylcholine_mem']
    for molecule in inter:
        if molecule == 'time':
            continue
        # iterate through the measured timepoints, thus finer evaluation of fit
        for i, means in enumerate(data[molecule]['values']):
            for pos, mean in enumerate(means):
                bias_fac = 1
                # some data entries empty as no literature value found, thus skiped
                if np.isnan(mean):
                    continue
                if molecule in alex_bias_lst:
                    bias_fac = 2
                if normalized:
                    dist += np.nansum(((mean
                            - simulation_result_dict[molecule][i])**2  # noqa:E128
                            * bias_fac)  # noqa:E128
                            / data[molecule]['std'][i][pos]**2)   # noqa: E128

                else:
                    dist += np.nansum(bias_fac*(mean
                            - simulation_result_dict[molecule][i])**2)  # noqa:E128

    return dist * factor


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


def objective_function(parameter: dict, model, t_data: dict, process_id):

    try:

        res = simulation_run(model, parameter)

    except RuntimeError:
        # print('Error simulating model for parameters %s' %parameter)
        return np.nan

    res_p = simulation_to_panda(model, res)

    dic_results = simulation_to_dict(res_p)

    sqd_dis = compute_sqd_distance(dic_results, t_data)

    # list of intersecting keys, as only those relevant
    # inter = dic_results.keys() & t_data.keys()
    # score_growth = check_growth(res_p[inter])
    score_zero = check_zero(res_p)
    # score_conc = constrain_concentration(res_p)

    return sqd_dis + score_zero  # + score_growth


def steady_state_calc(model, parameter: dict):

    model.resetToOrigin()
    model = set_model_parameters(model, parameter)
    rr.Logger.disableConsoleLogging()
    try:
        score = model.SteadyState()
    except RuntimeError:
        return 1e40, model

    return score, model


def objective_SS_function(parameter: dict, model, t_data: dict, process_id):

    ss_score, model_in_SS = steady_state_calc(model, parameter)
    res = model_in_SS.getSteadyStateNamedArray()

    if ss_score == 1e40:
        return ss_score

    res_p = simulation_to_panda(model, res)
    dic_results = res_p.to_dict('list')

    sqd_dis = compute_sqd_distance(dic_results, t_data)

    return sqd_dis


if __name__ == '__main__':
    options = {1: "cPL_conc",
               2: "noV_cPL_conc",
               3: "pc_pe_PL",
               4: "PLModel"
               }
    entry = sys.argv[1]
    run_id = sys.argv[2]
    print(options)
    # entry = input("Name of the model to use: ")

    try:
        name = options[int(entry)]

    except:
        name = str(entry)

    modelpath = "model_files/" + name + ".atm"
    datapath = "CMA_files/" + name + "/"
    timestr = time.strftime("%Y%m%d-%H:%M:%S")

    model = te.loada(modelpath)
    model.resetAll()
    p_keys = get_parameter_keys(0, datapath)
    log = True

    maier_data = pd.read_csv("~/PhD/Trophozoit/Datasets/maierframe_muMolar.tsv",
                             sep="\t", index_col=0)  # maier dataset
    meta = pd.read_csv("~/PhD/Trophozoit/Datasets/metabolites_muMolar.tsv",
                       sep="\t", index_col=0)

    t_data = mke_test_dict(model, maier_data, meta)

    esta = Estimator.ParameterEstimator()
    esta.initialize(objective_function,
                    mk_bounds(p_keys, log),
                    {'model': model, 't_data': t_data})

    opt_args = {'tolx': 1.0e-8, 'tolfun': 1.0e-8, 'maxiter': 2500,
                'tolfacupx': 1.0e9, 'popsize_factor': 3}

    score_para = esta.run(method='cma', n_lhs=10, run_id=run_id,
                          cma_sigma0=1.0e0,
                          optimizer_args=opt_args)

    """score_para = esta.run(method='swarm', iterations=300,
                                      swarm_size=250)
                """
    with open(datapath + timestr + run_id + 'whole_paras.txt', 'wb') as handle:
        pickle.dump(score_para, handle)
