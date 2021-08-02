"""
Small script to make for automated test dict, which has all relevant literature
values for the given tellurium model
"""
import tellurium as te
import pandas as pd
import numpy as np


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
    alex_factor = 602214.076  # avo/(10^9 cells and 10^9 nmol/mol
    # Translation dict keys=model_names, values=DataFrame_name
    long_name = {
        'Choline': 'avg Cho',
        'L_Serine': 'avg Ser',
        'Phosphatidylethanolamine': 'avg PE',
        'Phosphatidylcholine': 'avg PC'}
    # find matching values between dataframe and model
    intersection = list(set(metabolites.index) & set(model.getFloatingSpeciesIds()))

    work_df = metabolites.loc[metabolites.index.isin(intersection
                                              + [long_name[a]
                                              for a in model.getFloatingSpeciesIds()
                                              if a in long_name])].copy()

    model_names = intersection + [a for a in model.getFloatingSpeciesIds()
                                  if a in long_name]
    i=0
    new_dict = {}
    for row in work_df.index:
            model_name = model_names[i]
            i+=1
            new_dict[model_name] = {'mean':[work_df.loc[row, 'uRBC'] / alex_factor,
                                            np.nan,
                                            work_df.loc[row, 'Parasite'] / alex_factor,
                                            np.nan],
                                    'std':[work_df.loc[row, 'Std.'] / alex_factor,
                                            np.nan,
                                            work_df.loc[row, 'Std..1'] / alex_factor,
                                            np.nan]}

    # parasite_vol = np.array([4.00**-1 * 1e-3, 26.7**-1 * 1e-3, 26.9**-1 * 1e-3])
    # extract the avs and give proper names
    return new_dict


def mke_test_dict(model):
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
    maierframe = pd.read_excel('~/PhD/malaria_lipid_model/Lipid-Model/Datasets/RBC and asexual Pf lipidome.xlsx',
                               header=1, index_col=0)  # maier dataset
    metabolites = pd.read_excel("~/PhD/malaria_lipid_model/Lipid-Model/Datasets/metabolomics_test_data.ods",
                                sheet_name=2, header=1, index_col=0)

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
        new_dict[model_name] = {'mean': [],
                                'std': []}
        for key in stage_dict.keys():
            new_dict[model_name]['mean'].append(work_df.loc[row, stage_dict[key]].mean())
            new_dict[model_name]['std'].append(work_df.loc[row, stage_dict[key]].std())

    metas_dict = metabolomics_test_dict(model, metabolites)

    new_dict.update(metas_dict)

    return new_dict
