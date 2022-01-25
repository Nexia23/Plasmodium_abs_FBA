import json
import pandas as pd
import numpy as np
import tellurium as te
import roadrunner as rr


class Fit_Model:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.modelpath = "model_files/" + self.model_name + ".atm"
        self.model = te.loada(self.modelpath)
        # Data to load from .txt files
        self.datapath = "CMA_files/" + self.model_name + "/"

        self.data_ar = []  # array with all lit. values
        self.data_std = []  # array with stds. for each lit. value
        self.data_index_ar = [-1]  # index for data array
        '''
        Explainer:
        The data_index_ar is the index for the data so that values of the 
        same molecule at the same timepoint have the same index
        This index is used to enlarge comapre_ar with the simulation
        data, so that for each value in data_ar the corresponding 
        simulation data point is prepared.
        -> to enable simple array calculations for the residuals
        '''

        self.compare_ar = None
        self.timepoints = ["uninfected", "ring", "troph", "schizont"]
        self.observables = []  # str list with names of the observables

        self.test_data_dict = {}  # dict with lit. data
        self.test_data_names = None  # str list of molecules in test_data
        self.parameters = None  # current parameter set of the model 

        self.residuals = None  # maximum likelyhood residuals, distance from simulation data to lit.
        self.bias_ar = None  # str list names of molecules that have bias: here their residuals count more 
        # Optimization settings
        self.settings = {}
        if self.model_name.startswith("SS"):
            self.objective = self.objective_steady_state_function
        else:
            self.objective = self.objective_function

    def set_parameters(self, self_para_adjust: bool):
        """
        Function to get the parameters, which are fitted with their boundaries
        ----------
        Parameters
        ----------
        self_para_adjust: bool
            for multiple runs of estimator or when parameters self adjusted
            determines which parameter .txt file used
        self.datapath: string
            path to parameter .txt file, json dict file keys=names, values=value
        ---------
        """
        try:
            if self_para_adjust == 1:
                with open(self.datapath + 'whole_paras.txt', 'rb') as handle:
                    parameters = pickle.loads(handle.read())

        except FileNotFoundError:
            print('Using to_fit_parameter_set')
            with open(self.datapath + 'to_fit_para.txt', 'r') as handle:
                parameters = json.loads(handle.read())

        self.parameters = parameters

    def mke_test_dict(self):
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
        if self.model_name.startswith('SS'):
            self.timepoints = ["troph"]

        maierframe = pd.read_csv("Datasets/maierframe_muMolar.tsv",
                                 sep="\t", index_col=0)  # maier dataset
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
                               for a in self.model.getFloatingSpeciesIds()
                               if a in long_name_to_maier]]
        # parasite_vol = np.array([4.00**-1 * 1e-3, 26.7**-1 * 1e-3, 26.9**-1 * 1e-3])
        # extract the avs and give proper names

        maier_to_long_name = {v: k for k, v in long_name_to_maier.items()}
        for row in work_df.index:
            model_name = maier_to_long_name[row]

            for key in self.timepoints:
                values = work_df.loc[row, stage_dict[key]].tolist()
                stds = [work_df.loc[row, stage_dict[key]].std()] * len(values)

                self.data_ar.extend(values)
                self.data_index_ar.extend([self.data_index_ar[-1]+1]
                                          * len(values))
                self.data_std.extend(stds)
            self.observables.append(model_name)

        self.bias_ar = np.array(self.observables)
        self.data_index_ar = self.data_index_ar[1:]

        self.metabolomics_test_dict()

    def metabolomics_test_dict(self):
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

        metabolites = pd.read_csv("Datasets/metabolites_muMolar.tsv",
                                  sep="\t", index_col=0)
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
        intersection = list(set(metabolites.index) & set(self.model.getFloatingSpeciesIds()))

        work_df = metabolites.copy()
        model_names = intersection + [a for a in self.model.getFloatingSpeciesIds()
                                      if a in long_name]

        stage_dict = {"uninfected": ['uRBC', 'Std.'],        # uninfected
                      "ring": None,                  # ring
                      "troph": ['Parasite', 'Std..1'],  # trophozoite
                      "schizont": None}                  # schizont

        for observable in model_names:
            key = observable
            if observable in value_dict.keys():
                key = value_dict[observable]

            for keys in self.timepoints:

                if stage_dict[keys] is None:

                    self.data_ar.append(np.nan)
                    self.data_std.append(np.nan)

                    self.data_index_ar.append(self.data_index_ar[-1] + 1)

                else:
                    values = work_df.loc[key, stage_dict[keys][0]].astype('float').tolist()
                    stds = work_df.loc[key, stage_dict[keys][1]].tolist()
                    # test whether if values is float, if true make a list
                    if type(values) == float:
                        values = [values]
                        stds = [stds]

                    self.data_ar.extend(values)
                    self.data_index_ar.extend(
                        [self.data_index_ar[-1] + 1] * len(values))

                    self.data_std.extend(stds)

            self.observables.append(observable)

        # parasite_vol = np.array([4.00**-1 * 1e-3, 26.7**-1 * 1e-3, 26.9**-1 * 1e-3])
        self.observables = np.array(self.observables)
        self.data_ar = np.array(self.data_ar)
        self.data_std = np.array(self.data_std)

    def set_settings(self, cma_options: dict = {}):

        opt_args = {'tolx': 1.0e-8, 'tolfun': 1.0e-10, 'maxiter': 3300,
                    'tolfacupx': 1.0e9, 'popsize': 200
                    }
        opt_args.update(cma_options)

        self.settings = {"method": 'cma',
                         "n_lhs": 4,
                         "run_id": 0,
                         "cma_sigma0": 1.0e-2,
                         "optimizer_args": opt_args}

    def steady_state_calc(self):

        self.model.resetToOrigin()
        self.set_model_parameters()
        rr.Logger.disableConsoleLogging()
        try:
            # model.conservedMoietyAnalysis = True
            score = self.model.steadyState()
        except RuntimeError:
            return False, self.model

        return score

    def get_residuals(self):
        '''
        Function to calculate the residuals, here the maximum likelyhood is used.
        '''
        t = self.data_ar
        index = self.data_index_ar

        compare_ar = self.compare_ar
        data_std = self.data_std
        # compare array is elonged by index so that is matches in lenght t: 
        # lit data
        residuals_all = (t - compare_ar[index])**2 / data_std**2
        # summation of distances of the same molecule at the same timepoint
        # len() == len(data_ar) -> value for each datapoint
        residuals_time = np.bincount(index, residuals_all)
        # summation of every timepoint for the same molecule -> len == len(observables)
        self.residuals = np.nansum(residuals_time.reshape(len(self.timepoints), 12, order='F'), axis=0)

    def add_bias(self):
        '''
        Function to introduce bias in residuals, since Alex Maier data-set more trusted or
        to make objective value harder to reach
        '''
        # make mask for which values of bias_ar are in observables
        bias = np.in1d(self.observables, self.bias_ar)
        # where true value doubled
        self.residuals[bias] = self.residuals[bias] * 2
        # just factor because of fun
        self.residuals = self.residuals * 10

    def objective_steady_state_function(self, parameters, process_id, weight=1):

        self.parameters = parameters
        ss_found = self.steady_state_calc()
        if not ss_found:
            return 1e30

        else:
            try:
                res = self.model.simulate()
                res_p = self.simulation_to_panda(res)

                self.simulation_p_to_compare_ar(res_p)
                self.get_residuals()
                self.add_bias()

                residuals = self.residuals
                objective_value = residuals.sum() + residuals.std() * weight

            except RuntimeError:
                objective_value = 1e30

            return objective_value

    def objective_function(self, parameters, process_id, weight=1):

        self.parameters = parameters
        try:

            res = self.simulation_run()

        except RuntimeError:
            # print('Error simulating model for parameters %s' %parameter)
            return np.nan

        res_p = self.simulation_to_panda(res)

        self.simulation_p_to_compare_ar(res_p)
        self.get_residuals()
        self.add_bias()

        residuals = self.residuals
        objective_value = residuals.sum() + residuals.std() * weight

        # list of intersecting keys, as only those relevant
        # inter = dic_results.keys() & t_data.keys()
        # score_growth = check_growth(res_p[inter])
        # score_zero = check_zero(res_p)
        # score_conc = constrain_concentration(res_p)

        return objective_value  # + score_zero + score_growth

    def set_model_parameters(self, excluded_values=[]):
        no_names = excluded_values
        for param_id in self.parameters.keys():
            if any(x in param_id for x in no_names):
                continue
            else:
                try:
                    self.model[param_id] = self.parameters[param_id]
                    # print(param_id)
                    # print(model[param_id])
                except RuntimeError:
                    print('could not set parameter : {0}'.format(param_id))
                except TypeError:
                    # print('try to set {0} to {1}'.format(model[param_id]),params[param_id])
                    print(format(self.model[param_id]))  #
                    print(format(self.params[param_id]))

    def simulation_run(self):

        self.model.resetToOrigin()
        self.set_model_parameters()
        rr.Logger.disableConsoleLogging()
        sim_results = self.model.simulate(0, 48 * 3600, 3600)

        return sim_results

    def simulation_p_to_compare_ar(self, simulation_result_p):
        # TODO : all time points are used but what if looking at specific time
        s_panda = simulation_result_p

        times = {'uninfected': 2 * 3600,
                 'ring': 8 * 3600,
                 'troph': 36 * 3600,
                 'schizont': 48 * 3600}

        # find most similar timepoint in simulation_results
        can = []
        for item in self.timepoints:
            can.append(min(s_panda['time'], key=lambda x: abs(x - times[item])))

        # cut df to size of the matching time points
        s_panda = s_panda[s_panda['time'].isin(can)]

        # dict with molecule names as keys and value is list of values at the specified timepoints
        compare_df = s_panda[self.observables]

        self.compare_ar = compare_df.values.flatten('F')

    def simulation_to_panda(self, simulation_result, col=['time']):
        return pd.DataFrame(simulation_result, columns=col
                            + self.model.getFloatingSpeciesIds())

    def constrain_concentration(self, species_timecourse, factor=10**-1):
        """
        check whether [s] < 1.0
        :param species_timecourse: timecourse for chosen species
        :param factor: badness of negative growth
        :return: number of species which have neg growth * factorb
        """
        bool_constrain = species_timecourse < 1.0

        too_high_constrain = bool_constrain.any().sum()
        return too_high_constrain * factor

    def check_zero(self, species_timecourse, factor=10**-1):
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

    def check_growth(self, species_timecourse, factor=10**-1):
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
