### Goals
Use FBA to analyse lipid metabolic development during the asexual stages. Previously published GEM #ipfa or #ipfal21 is used and modified to represent the lipid metabolism adequately. As results resource, energy and carbon fluxes will be calculated so that a computationally reliable estimate on the metabolic burden on the parasite can be predicted. 
- #SLIMEr is implemented to facilitate lipid representation.
- Biomass function rewrite
- run different FBAs
	1. normal FBA for different stages
	2.  pFBA  
### GEMs
#### 1. iPfa #Chiappino-Pepe2017 et al.
Supporting information [here](https://doi.org/10.1371/journal.pcbi.1005397.s001)

#### 2. iPfal17-21 #Carey2017 et al.
Uses Gulati2015 lipid composition data as read from figure 1 time point unknown, values are in mol%
#### 3. Tewari et al.
Lots of papers but not cited by others use model from Plata et al. as base. 
Changes:
- the biomass composition to include more phospholipids and fatty acids same reference as #Chiappino-Pepe2017
- dry weight is defined by merozoite weight ~1,0017 pg (no reference) and multiplication rate of merozoite = * 24 thus growth rate over cell cycle is (24 -1)/48 g/h/gDW merozoite, here [paper](https://bmcsystbiol.biomedcentral.com/articles/10.1186/s12918-016-0291-2#MOESM1)
---------------------------------------------------------------------
## Comparison Table 

|  | ipfal21 | ipfa |
| -------- | -------- | -------- |
| MetnetX| no, problem with exchange reaction definitions| yes, quick overview analysis possible|
| ==biomass==|build from modified yeast biomass(previous model Plata 2010), updated in ipfal17 for lipids and tRNA  | build from Forth thesis, plasmodium falciparum metabolomics|
|lipid biomass|pseudo exchange reaction or pseudo lipid production reaction, not clear how the stoichiometric values are calculated  | each needed PL part of biomass; generalized FAs also part |
|lipid production|all known metabolic reactions in model but mostly exchange reactions preferred in solution, FBA linear optimization problem.<br> PS reaction in the model just not used|Cholesterol, most FAs and DAG even TAG produced by exchange reaction and then into biomass;<br> C16:0 produced by reduction of Palmitoyl-CoA producing ATP;<br> PC, PE and Sphingomyelin correct pathway;<br> PS produced by base exchange with PC(incorrect) #ipfa_lipid_prod|
|metabolic tasks|performs the same as first model|works better for metabolite depletion but purine blocking does not work -> maybe own lacking understanding|
|Medium|196 metabolites in medium mostly 1640RPMI and blood| much broader 242, all of RPMI and anything in blood|
|Reference|higher quality references (KEGG, BiGG, Metnetx,...)| internally high abides community standard, but only KEGG|
|Compatibility|lower, troublesome exchange reactions, but thus better standard|higher for web-hosted services|
|==Up-gradable==|Biomass function<br>pseudo lipid, and lipid production|lipid biomass<br>PS-production (PE-PS base exchange no Choline)<br>curate weird PG circle|

-------------------------------------------------------------------
## SLIMEr
### dry weight estimation: #questions 
- as of now linear growth of one merozoite to 24 merozoites during the asexual blood stage will be assumed
- big unknown is the lipid content in relation to the whole cell dry mass (beside the Forth measurement) making the use of relative data even more dodgy

- volume based assumption cannot capture the growth, since:
	- volume grows with a logistic function in S-shape curve
	- first one merozoite increases its volume to ring at the same time Maurer's clefts are built or exported from the parasitophorous vacuole
	- the volume swells until around 50 fl at the end of the trophozoite stage also organelles are built and their volume increases
	- in the schizont stage the volume plateaus but biomass should increase at least for lipids as the merozoites are formed  
### Stoichiometric values
#### Side chains:
- not every phospholipid's side chains are identified, e.g. PC 32:0, PC 38:7
	- to answer this, a permutation function is written, possible entries are for side chains are (14,16,18,20,22) most abounded probably only to this elongated and for unsaturation (0,1), same reasoning though side chain unsaturation only know to 1 (find reference #TODO)
		- PC 32:0 -> PC 14:0_18:0,  PC 16:0_16:0 
	- lipids that cannot be build through a allowed combination of side chains and unsaturation are filtered out and considered to be imported from the RBC
		- PC 38:7
	- the frequency of every possible combination is calculated and multiplied by the molecule abundance
- two exported files: column 'reaction' gives hint for which reaction in SLIMEr formalism used, also mean values for the three stages saved, here sum of all PC 34:0, e.g. PC (34:0) 14:0_20:0, PC (34:0) 16:0_18:0 match the subtracted mean value of the stage (mean_stage - mean_RBC) of the original data set value
	1. file: for each lipid produced or imported according to my system
	2. file: SLIMEr pseudo reactions values and imported lipids for biomass or pseudo reaction 
------------------------------------------------------------------
### Biomass
Nearly all metabolites of iPFA are included four missing since no metabolite found, the combination of both biomass reactions as of now not feasible as stoichiometric factors cannot be translated into another.
Updated biomass in iPbe has detailed excel file for biomass composition which is basically the same as in iPfa but new metabolites added, like iron. This will be used.
- Ring stage head group: 
	- 12.2366667 DAG + 75.1733333 PC + 75.8466667 PE + 2.6333333 PG + 2.5233333 PS + 6.9666667 TAG
- Trophozoite:
	- 123.9522222 DAG + 167.8877778 FreeChol + 629.7622222 PC + 324.9555556 PE + 32.1066667 PG + 90.9511111 PS + 35.1888889 TAG + 2.46 Cer + 1.0255556 DHSM + 17.4655556 SM'
- Schizont:
	- 329.83 DAG + 136.39 FreeChol + 1576.2333333 PC + 607.5966667 PE + 101.1633333 PG + 107.4766667 PS + 174.81 TAG + 1.53 Cer + 2.5 DHSM
Info on problem:[[Biomass trouble]]

Biomass composition of Thomas Forth used in iPfa
![[T_forth_biomass_distribution_table.png]]
![[t_forth_biomass_distribution_pie.png]]

----------------------------------------------------------------------------------------------------------------------------
### Work on GEMs
#Chiappino-Pepe2017 no lipid production at all, discussion [[Difference iPfal and own]]
#Carey2017 most reactions are in some way there
#### What is needed
- all phospholipids that are missing and their SLIMEr pseudo reactions
- correct PL build
	- in the Carey model FA are existent 
- FA elongation to 20 or 22 #recherche if that is experimentally valid
- desaturation
- import of reactions for Pls where reasonable doubt exists as to parasite capability of producing those FA, every unsaturation above 1 #recherche 
--------------------------------------------------------------------
## What is used
MW and chemical formula: https://pubchem.ncbi.nlm.nih.gov or human metabolome database
## Assumptions
Sphingomyelin and Ceramide all are built using C18:0 fatty acid in their backbone
## Discussion work
- Lipids that have a negative value are excluded from biomass in calculation using Alex data set. No clear hint to what is happening to them. This publication [labeled FA ](https://journals.biologists.com/jcs/article/117/8/1469/28271/Developmental-stage-specific-triacylglycerol) could be of interest
- Why use normal distribution
	- no clear evidence which FA used
	- looking at the data of [Hsiao](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1149929/?page=7) differences emerge if using this other distribution comparison is a must
- Quotient of FA sum / phospholipid sum in between 2 or 3 because phospholipids that are labeled transported are considered in head group calculations for pseudo SLIMEr but not in the FA calculations
### iPfa lipid distribution
![[ipfa_lipid_comp.png]]

## Alex data set lipid distribution
![[Pie_chart_meanring.png]]
![[Pie_chart_mean_troph.png]]
![[Pie_chart_mean schizont.png]]

---------------------------------------------------------------------
Table: Lipid distribution of Alex data set and iPfa 

| |mol% RING|mol% Troph|mol% Schizont|iPfa|
|:---|---:|---:|---:|-----:|
|CE||0,01|||
|DAG|6,70 |8,68 |10,85|15,0 %
|FreeChol||11,75 |4,49|15,0 %
|LPC||||
|PC|42,36 |44,09|51,87|34,0 %
|PE|41,57 |22,74|20,00|20,0 %
|PG|1,44 |2,25 |3,33 |3,0 %
|PS|3,85 |6,37|3,54 |4,0 %
|TAG|3,95 |2,46|5,75 |3,0 %
|Cer|0,11|0,17|0,05 |
|DHSM||0,07 |0,08 |
|SM|0,003|1,41|0,04|2,0 %
|Free FA||||2.0 %
|CL||||1,0 %
|PI||||1,0 %

| | Ring  | Troph  | Schizont  |
|--|---|---|---|
|Lipids with FA|182,446666666667|1260,93222222222|2902,45|
|FA sum|282,933333333333|1864,73|4923,16333333333|
|unknown FA imported|89,1733333333333|690,651111111111|1054,01666666667|
|Total FA|372,106666666667|2555,38111111111|5977,18|
|Quotient|2,03953666825008|2,02658086301229|2,05935675033162|

Table: Distribution of PL attached FA in Alex data set

|      |   Mol% Ring |Mol% Troph   |Mol% Schizont |
|:-----|------------:|------------:|-------------:|
| 14:0 |  9.17407    |  7.83222    |  7.51462     |
| 18:0 | 11.4766     | 13.8463     | 11.9418      |
| 16:0 | 12.479      | 16.6689     | 15.2947      |
| 14:1 |  7.98097    |  6.84995    |  7.63047     |
| 18:1 | 23.0045     | 21.2619     | 23.5024      |
| 16:1 | 13.424      | 12.4598     | 13.2013      |
| 20:0 |  9.10173    |  7.6948     |  7.50166     |
| 20:1 | 13.3156     | 12.2563     | 12.906       |
| 24:1 |  0.0117813  |  0.346193   |  0.00880193  |
| 24:2 |  0.0294533  |  0.140622   |  0.0154372   |
| 25:0 |  0.00235627 |  0.0298524  |  0.0066353   |
| 15:0 |            |  0.00113213 |             |
| 17:0 |            |  0.00804406 |  0.0009479   |
| 18:2 |            |  0.193057   |  0.457362    |
| 22:0 |            |  0.00923577 |  0.00169268  |
| 23:0 |            |  0.0203783  |             |
| 24:0 |            |  0.309845   |  0.00480721  |
| 24:3 |            |  0.00679276 |  0.000338536 |
| 25:1 |            |  0.00798447 |             |
| 26:0 |            |  0.0114404  |             |
| 26:1 |            |  0.0220467  |  0.00467179  |
| 26:2 |            |  0.0231788  |  0.00575511  |
| 19:0 |            |            |  0.000609364 |

  -------------------------------------------------------
Table: Comparison of Hsiao measurement data and own FA distribution in PLs. Own FA distribution assumes normal distribution for FAs (C14, C16, C18, C20) in PLs.

| | IEPM | Parasite | uRBC | Ring | Troph | Schizont |
|:-----|-------:|-----------:|-------:|-----------:|------------:|------------:|
| 14:0 | 1.46 | 0.87 | 0.31 | 9.17407 | 7.83222 | 7.51462 |
| 16:0 | 31.15 | 32.32 | 22.68 | 12.479 | 16.6689 | 15.2947 |
| 16:1 | 1.87 | 2.14 | 0.8 | 13.424 | 12.4598 | 13.2013 |
| 17:0 | 0.46 | 0.42 | 0.21 | 0 | 0.00804406 | 0.0009479 | 
| 18:0 | 13.87 | 13.27 | 14.2 | 11.4766 | 13.8463 | 11.9418 |
| 18:1 | 24.6 | 24.82 | 14.18 | 23.0045 | 21.2619 | 23.5024 |
| 18:2 | 10.1 | 12.33 | 12.67 | 0 | 0.193057 | 0.457362 |
| 20:0 | 0.15 | 0.69 | 0.1 | 9.10173 | 7.6948 | 7.50166 | 
| 22:0 | 1.12 | 1.16 | 2.39 | 0 | 0.00923577 | 0.00169268 | 
| 24:0 | 1.6 | 0.07 | 0.66 | 0 | 0.309845 | 0.00480721 | 
| 24:1 | 1.55 | 0.9 | 4.2 | 0.0117813 | 0.346193 | 0.00880193 |
| Sum | 87.93 | 88.99 | 72.4 | 78.6717 | 80.6304 | 79.4301 |