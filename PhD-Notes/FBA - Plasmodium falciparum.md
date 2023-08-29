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
- dry weight is defined by merozoite weight ~1,0017 pg (no reference) and multiplication rate of merozoite = * 24 thus growth rate over cell cycle is (24 -1)/48 g/h/gDW merozoite
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
### Work on GEMs
#Chiappino-Pepe2017 no lipid production at all, discussion [[Difference iPfa and own]]
#Carey2017 most reactions are in some way there
#### What is needed
- all phospholipids that are missing and their SLIMEr pseudo reactions
- correct PL build
	- in the Carey model FA are existent 
- FA elongation to 20 or 22 #recherche if that is experimentally valid
- desaturation
- import of reactions for Pls where reasonable doubt exists as to parasite capability of producing those FA, every unsaturation above 1 #recherche 
--------------------------------------------------------------------
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

|   |   |   |   | |
|---|---|---|---|-----|
||mol% RING|mol% Troph|mol% Schizont|iPfa|
|CE|||||
|DAG|6,98 %|8,69 %|10,86 %|15,0 %
|FreeChol||11,78 %|4,49 %|15,0 %
|LPC||||
|PC|42,86 %|44,17 %|51,89 %|34,0 %
|PE|43,25 %|22,79 %|20,00 %|20,0 %
|PG|1,50 %|2,25 %|3,33 %|3,0 %
|PS|1,44 %|6,38 %|3,54 %|4,0 %
|TAG|3,97 %|2,47 %|5,76 %|3,0 %
|Cer||0,17 %|0,05 %|
|DHSM||0,07 %|0,08 %|
|SM||1,23 %||2,0 %
|Free FA||||2.0 %
|CL||||1,0 %
|PI||||1,0 %
||||
|14:0|9,54 %|7,98 %|7,59 %|
|18:0|11,86 %|12,83 %|11,95 %|
|16:0|11,98 %|16,88 %|15,28 %|
|14:1|8,30 %|6,98 %|7,71 %|
|18:1|21,04 %|21,36 %|23,50 %|
|16:1|13,96 %|12,69 %|13,33 %|
|20:0|9,47 %|7,84 %|7,57 %|
|20:1|13,85 %|12,49 %|13,04 %|
|15:0|0,00 %|0,00 %|0,00 %|
|17:0|0,00 %|0,01 %|0,00 %|
|22:0|0,00 %|0,01 %|0,00 %|
|23:0|0,00 %|0,02 %|0,00 %|
|24:0|0,00 %|0,32 %|0,00 %|
|24:1|0,00 %|0,35 %|0,00 %|
|24:2|0,00 %|0,14 %|0,02 %|
|24:3|0,00 %|0,01 %|0,00 %|
|25:0|0,00 %|0,03 %|0,01 %|
|25:1|0,00 %|0,01 %|0,00 %|
|26:0|0,00 %|0,01 %|0,00 %|
|26:1|0,00 %|0,02 %|0,00 %|
|26:2|0,00 %|0,02 %|0,01 %|


  -------------------------------------------------------
  
| | IEPM | Parasite | uRBC | Ring | Troph | Schizont |
|-------|--------|--------|------|--------|-------|--------|
|14:0| 1.46|0.87|0.31|9.541428|7.978994|7.590157|
|16:0|31.15|32.32|22.68|11.982490|16.875503|15.277703|
|16:1|1.87|2.14|0.80|13.961489|12.693284|13.333986|
|17:0|0.46|0.42|0.21|0.000000|0.008195|0.000274|
|18:0|13.87|13.27|14.20|11.862655|12.833263|11.946044|
|18:1|24.60|24.82|14.18|21.036428|21.363039|23.503057|
|20:0|0.15|0.69|0.10|9.466194|7.838999|7.572692|
|22:0|1.12|1.16|2.39|0.000000|0.007770|0.000000|
|24:0|1.60|0.07|0.66|0.000000|0.315652|0.000000|
|24:1|1.55|0.90|4.20|0.000000|0.352680|0.000000|
|Sum|77.83|76.66|59.73|77.850684|80.267378|79.223913|
