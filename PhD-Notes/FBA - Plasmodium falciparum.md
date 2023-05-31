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
