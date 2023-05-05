Collection of the model #model #lipid_production

### Goal
Correct representation of the lipid metabolism through the asexual stage, as of now it will be the representation of the trophozoite stage. With this model different stress and deletions will be tested to understand network stability. #aim
### Pathway
![[pathway_lip_prod.png]]
##### Known Enzymes:
Enzyme folder on drive: https://drive.google.com/drive/folders/13mFy6LZf0qF1fuJfbAiq88SChSFrCS0M?usp=share_link #enzyme_folder
- #PfCCT => transfer CTP to P-Cho production of  CDP-Cho
- #PfCEPT => transfer CDP-Etn or CDP-Cho to a DAG produces PE or Pc and CMP 
- #PfCK => phosphorylation of choline, can also use ethanolamine as substrate
- #PfCT => transfer ery Cho over parasite plasma membrane, might not exist
- #PfECT => add CDP to P-Ethanolamine using CTP
- #PfEK => phosphorylation of ethanolamine
- #PfPMT => triple methylation of P-Etn to P-Cho
- #PfPSD => decarboxylation of PS to PE + $CO_2$
- #PfPSSbe => base exchange reaction of PE with Serine to PS + Ethanolamine and also suggested for synthesis of PS using CDP-DAG and Serine (couldn't be proven)
##### Disputes:
- Role of #Lyso-PC might be bigger than of #Choline uptake, but #PfGDPD might be in RBC cytosol which would mean that in the scope of the model the outside choline concentration is the only difference
- Lacking evidence of other reactions and no enzyme annotation (last one turned out to be #PfGDPD) suggests that #Serine enters the pathway only through #PSSbe base exchange reaction to produce PS, which in turn is decarboxylated to PE #Wein2018    
### Model
The model describes the trophozoite stage of Plasmodium falciparum during it's asexual blood development. In the model assumes only the parasite cytosol as place of production, while nutrients are imported or assumed to be over abounded thus not considered and final  products exported. The model assumes a quasi steady state for intermediate species. Reasoning is optimal usage of resources, as the cell optimized the utilization of intermediate species to produce membrane lipids. 

#### Parameters:
Parameters consist of starting values for the species concentration and the parameters for the reaction kinetics.
##### Concentration values:
Starting values and goal values from Maier groups lipid data whole cell:
- Phosphatidylethanolamine whole cell
- Phosphatidylcholine whole cell
- Phosphatidylserine whole cell
Other values are considered in quasi steady state, produced as much as used so no change.
Vo Duy #VoDuy2012
- P-Ethanolamine
- Serine
- Ethanolamine
- Choline
- P-Choline
- CDP-Choline
- CDP-Ethanolamine
- Phosphatidylcholine - cytosol
- Phosphatidylethanolamine - cytosol
##### Trouble:
No cytosolic PS concentration measured, after parameter estimation very low aboundance
Starting values and goal values from Maier groups lipid data whole cell:
- Phosphatidylethanolamine whole cell
- Phosphatidylcholine whole cell
- Phosphatidylserine whole cell
Other values are considered in quasi steady state, produced as much as used so no change.
Vo Duy #VoDuy2012
- P-Ethanolamine
- Serine
- Ethanolamine
- Choline
- P-Choline
- CDP-Choline
- CDP-Ethanolamine
- Phosphatidylcholine - cytosol
- Phosphatidylethanolamine - cytosol
##### Reaction equation definitions:
- Michaelis Menten -  $v(t)=\frac{v_{max} \cdot S(t)}{K_m + S(t)}$ 
	Example: R02055: Phosphatidylserine -> Phosphatidylethanolamine; vmax_R02055 * Phosphatidylserine / (km_Phosphatidylserine_R02055 * (1) + Phosphatidylserine) in cytoplasm
- Convenience Kinetics 	
- Mass action
	Example: SSTransportPS: Phosphatidylserine_mem => ; $k_{SSTransportPS_{mem}} * Phosphatidylserine_{mem}$ in cytoplasm
- Mass action with enzymes

Enzyme reaction constant values measured experimentally, used to shrink the parameter boundaries see in #enzyme_folder. Boundaries mostly  Value 10⁻³ < Value < Value 10³ 

### Outcomes
- not feasible whole cycle model as too little data
	- enzyme availability 
	- species concentration at different stages then trophozoite
- no cytosolic PS concentration measured, after parameter estimation very low aboundance, does high impact in jacobi matrix
1. Can estimate best possible score for estimation optimization function ~ 438.28
2. Michaelis Menten and Mass Action consistently reach around best parameter estimation function value
	- maybe easier to find with less parameters, but covariance should help with this
	- MM is a little bit better:
	![[plot_score_lip_prod.png]]
3. Parameter sensitivity tested Parameter value between value * [0.1,..., 1.9]
	1. For PS 
		 
	2. For P-Etn
		 
	3. For
		 
	4. For
4. Sensitivity analysis
	Reaction names are renamed instead of code, simple name
	1. Elasticity 
		1. Nothing  special to see reactions are positive to their Edukte
		2. Km and vmax values diametrical ![[elastic_coeff_lip_prod.png]]
	2. Control coefficient
		1. Not sure why colorbar below -1 or above 1![[control_coeff_lip_prod.png]]
		2. Flux control coefficient
			1. unscaled ![[control_coeff_unscaled_flx_lip_prod.png]]
			2. scaled ![[control_coeff_scaled_flx_lip_prod.png]]
		3. Scaled Concentration CC
			1. ![[control_coeff_scaled_conc_lip_prod.png]]
		4. Jacobi Matrix of system with numpy linag
			1. rank:  13
			2. reactions: 20
			3. trace:  -469160.9650226375 - cytosolic PS has big influence on this value
			4. determinate:  -3.4191815350211606e-82
		5. Full Eigenvalues by tellurium= [-4.69160965e+05 -4.01486412e-08 -9.22446474e-08 -1.32868239e-07 -2.01472708e-08 -7.26466874e-07 -1.01025503e-07 -2.38651314e-08 -2.02208999e-07 -1.78189396e-07 -1.16431683e-08 -1.00002026e-08 -1.00040967e-08]
### TODO #TODO
- Code:
	- The reactions are defined in Tellurium with ->, meaning they chould be reversible. What is actually wanted
	- rewrite output function more similar to jorins for parameter identifiability 
- Logic:
	- Serine pathways deletion except known, or better test case
	- check literature for enzyme characterization updates
- Science:
	- implement test cases for:
		- no Ethanolamine
		- deletion of disputed Serine Pathways
### Existing Models
Sen et al. #sen
