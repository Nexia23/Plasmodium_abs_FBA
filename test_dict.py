"""
Small script to make for automated test dict, which has all relevant literature
values for the given tellurium model
"""
import tellurium as te
import pandas as pd
import numpy as np

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


def mke_test_dict(model, timepoints=["uninfected", "ring", "troph", "schizont"]):
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
    maierframe = pd.read_csv("Datasets/maierframe_muMolar.tsv",
                             sep="\t", index_col=0)  # maier dataset
    metabolites = pd.read_csv("Datasets/metabolites_muMolar.tsv",
                       sep="\t", index_col=0)

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