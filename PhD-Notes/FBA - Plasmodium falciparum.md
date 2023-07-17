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

#### 3. Tewari et al.
Lots of papers but not cited by others use model from Plata et al. as base. 
Changes:
- the biomass composition to include more phospholipids and fatty acids same reference as #Chiappino-Pepe2017
- dry weight is defined by merozoite weight ~1,0017 pg (no reference) and multiplication rate of merozoite = * 23 thus growth rate over cell cycle is (24 -1)/48 g/h/gDW merozoite
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

## SLIMEr
### dry weight estimation: #questions 
- as of now linear growth of one merozoite to 24 merozoites during the asexual blood stage will be assumed
- volume based assumption cannot capture the growth, since:
	- volume grows with a logistic function in S-shape curve
	- first one merozoite increases its volume to ring at the same time Maurer's clefts are built or exported from the parasitophorous vacuole
	- the volume swells until around 50 fl at the end of the trophozoite stage also organelles are built and their volume increases
	- in the schizont stage the volume plateaus but biomass should increase at least for lipids as the merozoites are formed  
### Stoichiometric values
#### Side chains:
- not every phospholipid's side chains are identified, e.g. PC 38:7
	- to answer this, a permutation function is written, possible entries are for side chains are (14,16,18,20) most abounded probably only to this elongated and for unsaturation (0,1,2,3), same reasoning though side chain unsaturation only know to 1 (find reference #TODO)
	- the frequency of every possible combination is calculated and multiplied by the molecule abundance times the number of side chains required, 
		-> since 30mmol PC 38:7 consists of 30mmol PC + 30mmol side chain A + 30mmol side chain B
	- lipids that cannot be build through a combination of side chains and unsaturation are filtered out and differently considered #TODO 
### Work on GEMs
#Chiappino-Pepe2017 no lipid production at all 
#Carey2017 most reactions are in some way there
#### What is needed
- all phospholipids that are missing and their SLIMEr pseudo reactions
- correct PL build
	- in the Carey model FA are existent 
- FA elongation to 20 or 22 #recherche if that is experimentally valid
- desaturation
- import of reactions for Pls where reasonable doubt exists as to parasite capability of producing those FA, every unsaturation above 1 #recherche 