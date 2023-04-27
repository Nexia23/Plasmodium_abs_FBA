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

        self.test_data_dict = {}
        self.test_data_names = None
        self.parameters = None

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

    def mke_test_dict(self, 
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
        if self.model_name.startswith('SS'):
            timepoints = ["troph"]

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
        new_dict = {}

        maier_to_long_name = {v: k for k, v in long_name_to_maier.items()}
        for row in work_df.index:
            model_name = maier_to_long_name[row]

            new_dict[model_name] = {'values': [], 'std': []}
            for key in timepoints:
                values = work_df.loc[row, stage_dict[key]].tolist()
                stds = [work_df.loc[row, stage_dict[key]].std()] * len(values)

                new_dict[model_name]['values'].append(values)
                new_dict[model_name]['std'].append(stds)

        self.test_data_dict.update(new_dict)
        self.metabolomics_test_dict(timepoints)

    def metabolomics_test_dict(self, timepoints=[]):
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
        self.test_data_dict.update(new_dict)

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

    def objective_steady_state_function(self, parameters, process_id, weight=1):
        
        self.parameters = parameters
        ss_found = self.steady_state_calc()
        if not ss_found:
            return 1e30

        else:
            try:
                res = self.model.simulate()
                res_p = self.simulation_to_panda(res)

                dic_results = res_p[-1::].to_dict('list')

                sqd_dis_ar = self.compute_sqd_distance(dic_results)

                objective_value = sqd_dis_ar.sum() + sqd_dis_ar.std() * weight
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

        dic_results = self.simulation_to_dict(res_p)

        sqd_dis_ar = self.compute_sqd_distance(dic_results)

        objective_value = sqd_dis_ar.sum() + sqd_dis_ar.std() * weight
        # list of intersecting keys, as only those relevant
        # inter = dic_results.keys() & t_data.keys()
        # score_growth = check_growth(res_p[inter])
        # score_zero = check_zero(res_p)
        # score_conc = constrain_concentration(res_p)

        return objective_value  # + score_zero  # + score_growth

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

    def simulation_to_dict(self, simulation_result_p):
        # TODO : all time points are used but what if looking at specific time
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

    def simulation_to_panda(self, simulation_result, col=['time']):
        return pd.DataFrame(simulation_result, columns=col
                            + self.model.getFloatingSpeciesIds())

    def compute_sqd_distance(self, simulation_result_dict, factor=10**1,
                             normalized=True):

        # list of intersecting keys, as only those relevant
        inter = simulation_result_dict.keys() & self.test_data_dict.keys()

        dist_ar = np.zeros(len(inter))

        alex_bias_lst = ['DAG', 'Phosphatidylserine_mem',
                         'Phosphatidylethanolamine_mem', 
                         'Phosphatidylcholine_mem']

        for ar_pos, molecule in enumerate(inter):
            if molecule == 'time':
                continue
            dist = 0.

            bias_fac = 1
            if molecule in alex_bias_lst:
                bias_fac = 2
            # iterate through the measured timepoints, thus finer evaluation of fit
            for i, values in enumerate(self.test_data_dict[molecule]['values']):
                for pos, value in enumerate(values):
                    # data entries empty as no literature value found, thus skipped
                    if np.isnan(value):
                        continue
                    if normalized:
                        dist += np.nansum(((value
                                - simulation_result_dict[molecule][i])**2  # noqa: E128
                                * bias_fac)  # noqa:E128
                                / self.test_data_dict[molecule]['std'][i][pos]**2)   # noqa: E128

                    else:
                        dist += np.nansum(bias_fac*(value
                                - simulation_result_dict[molecule][i])**2)  # noqa:E128
            dist_ar[ar_pos] = dist * factor

        return dist_ar

    def constrain_concentration(self, species_timecourse, factor=10**-1):
        """
        check whether [s] < 1.0
        :param species_timecourse: timecourse for chosen species
        :param factor: badness of negative growth
        :return: number of species which have neg growth * factor
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
