#Chiappino-Pepe2017
## Model Description
Totally new build using FASTA data. The GEM iPfa presents an unbiased bottom-up reconstruction and an updated database of _P_. _falciparum_ metabolism.
Since steady state assumption no accumulation of hemozoin or Ca²⁺, in turn also means no lipid accumulate.
## Supporting information [here](https://doi.org/10.1371/journal.pcbi.1005397.s001)
Data used in the iPfa model important to know where it is coming from. 
To calculate these values they assumed a cell dry-weight for P. falciparum of 1.05•10⁻¹¹ gDW/cell according to Forth T. [Metabolic Systems Biology of the Malaria Parasite](https://etheses.whiterose.ac.uk/3739/1/T_Forth_Corrected_Thesis.pdf). 2012, which represents around 30% of the erythrocyte dry-weight - Mysliwski A, Lass P. Increase of size and dry mass of mouse erythrocytes depending on age of donors. 1985 PMID: 3974304. 
Growth rate estimated using $grwth=\frac{ln(\frac{N(t)}{N(0)})}{t}$, assuming 14-32 merozoits produced between 24-48hs. Doubling time measured as 12.3h for plasmodium falciparum experimentally - Liu J, Gluzman IY, Drew ME, Goldberg DE. The role of Plasmodium falciparum food vacuole plasmepsins. 2005 PMID: 15513918
### Uptake and secretions
#uptake
Host cells and blood stream, possible nutrients for uptake
	1. Insights Gained from _P. falciparum_ Cultivation in Modified Media [Sanjay A. Desai 2013](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3727134/) #RPMI1640
	3. Krebs HA. Chemical composition of blood plasma and serum. Annu Rev Biochem.  1950 (19):409-30. PubMed PMID: 14771836
Glucose  (set to 0.62 $\frac{mmol}{h\cdot gDW_{cell}}$ from asynchronous), lactate  (set to 0.76 $\frac{mmol}{h\cdot gDW_{cell}}$from asynchronous)
	7. Jensen MD, Conley M, Helstowski LD. Culture of Plasmodium falciparum: the role of pH, glucose, and lactate. J Parasitol. 1983;69(6):1060-7. https://www.jstor.org/stable/3280864?seq=6
			From paper: one glucose produces two lactose for the conversion calculation ![[ipfa_glucose_uptake_lactose_secretion.png]]
L-isoleucine (set to 0.053 $\frac{mmol}{h\cdot gDW_{cell}}$)
	8. Martin RE, Kirk K. Transport of the essential nutrient isoleucine in human  erythrocytes infected with the malaria parasite Plasmodium falciparum. Blood. 2007;109(5):2217-24 https://www.sciencedirect.com/science/article/pii/S0006497120419524?via%3Dihub
	Cite: P falciparum_–infected erythrocytes incorporated isoleucine into protein at a rate of approximately 170 µmol/(1012 cells · hour), and, although this rate is well below (and should therefore be supported comfortably by) the overall rate of isoleucine transport into parasitized cells [∼ 550 µmol/(1012 cells · hour)], it is significantly higher than the rate of isoleucine influx via endogenous mechanisms alone [∼ 110 µmol/(1012 cells · hour)] 
### Medium
[[Table_RPMI1640_content.pdf]]
#RPMI1640
![[Ions_RPMI1640.png]]
From paper: Insights Gained from _P. falciparum_ Cultivation in Modified Media [Sanjay A. Desai 2013](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3727134/)
iPfa has per definition a rich medium of 236 potential substrates, unless evidence was found to define a specific transport mechanism, transport of all molecules is allowed that do not incorporate phosphate, coenzyme A (CoA) and acyl-carrier proteins (ACP) in their molecular structures, and was assumed that transports occur through passive diffusion, probably NPPs. All substrates of RPMI1640 and human serum are included.

### Protein Location
Nearly 25% of the enzymes in iPfa were localized based on experimental evidence. The  
information on experimental localization of enzymes in P. falciparum was obtained from  
the online databases ApiLoc (last time updated in 2011) and from MPMP (last  
time accessed in March 2015). The remaining 75% of the enzymes were assigned to the  
intracellular compartments based on localization scores. These scores compare the  
protein sequences to be localized with the amino acid sequences that target the proteins  
to the specific intracellular compartments, such as the bipartite targeting sequence for the  
apicoplast in P. falciparum.
Digestive vacuole and Golgi apparatus are not compartments reactions occur in cytosol.
### Biomass
#biomass
- RNA
	- 5.9 +- 2.1 of biomass during schizont stage Forth T. [Metabolic Systems Biology of the Malaria Parasite](https://etheses.whiterose.ac.uk/3739/1/T_Forth_Corrected_Thesis.pdf). 2012, 
		 ![[RNA_biomass_forth_2012.png]]
- DNA 
	- 6.7 +-2.5 of biomass during schizont stage Forth T. [Metabolic Systems Biology of the Malaria Parasite](https://etheses.whiterose.ac.uk/3739/1/T_Forth_Corrected_Thesis.pdf). 2012, 
		![[DNA_forth_2012.png]]
- Amino acids/ Protein
	- 48 +- 9% of biomass during schizont stage Forth T. [Metabolic Systems Biology of the Malaria Parasite](https://etheses.whiterose.ac.uk/3739/1/T_Forth_Corrected_Thesis.pdf). 2012, 
		![[Amino_acid_forth_2012.png]]
- Lipid components
	- Table 1 in Palacpac et al.  [Developmental-stage-specific triacylglycerol biosynthesis, degradation and trafficking as lipid bodies in Plasmodium falciparum-infected erythrocytes.](https://cob.silverchair-cdn.com/cob/content_public/journal/jcs/117/8/10.1242_jcs.00988/4/1469.pdf?Expires=1686127288&Signature=EsqN1gPAzMwq~44sX~uK-cNbLhJfsUUARUdmrjm1MlqCQyUu1pfK2j5T97tVMDfA4V-N86fWlPWvJRhI946jJol8zvIL09zhZkY9QPt9yLaOBQWVgfS3XlXP~LW7Fqx42rpNhBfRV-AqlMDzlQJS~~IEEF4hYM9psDzGKPCXaCDxdW~3v9TaulSsipAoj2LuCZEZx4Htp6Gh54t7PVzl7jrZ1Rky9F16GBynKLflr~qo9ImeZrq5870pxcea0Qw1wM9XrnfrzwCbP4UgfEWRoPcWsNbLD55gD5nNLUm6klpXxY8Hqinj2xHN8ZdrW6WOirZdWKzJCbglCEk-U7xegQ__&Key-Pair-Id=APKAIE5G5CRDK6RD3PGA) 2004 PMID: 15020675. 
		- ![[Lipid_comp_2004_trpoh_schizont.png]]
	- Table 2 in strain Pf_FCR-3/A2 Hsiao et al. Modification of host cell membrane lipid composition by the intra-erythrocytic human malaria parasite Plasmodium falciparum.  . 1991 PMID: [2001227](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1149929/pdf/biochemj00165-0124.pdf) 
		- ![[lipid_comp_inprecent_inPMsep.png]]                  pure parasites used and IEPM means infected erythrocyte plasma membrane #asymmetry #asymmetry_model  
		Citation from paper: "The amount of phospholipid per cell is the same in non-parasitized and normal erythrocytes (- 3.4 tmol/101 cells). In parasitized cells, however, the amount of phospholipid per cell can be increased by up to eight times depending on the degree of parasitaemia and stage of infection. In a typical experiment, trophozoite-infected erythrocytes with 90 % parasitaemia contained 5.1 µmol of phospholipid/10¹⁰ cells, 1.5 times more than in uninfected cells. Of this, 1.53 µmol came from the parasite fraction and 3.08 µmol came from the IEPM fraction. Using these criteria, the recovery of IEPM from infected erythrocytes by lysis with 0.1 % saponin was 89 % and total lipid phosphate recovery was 88 %."  
- fatty acids 
	-  Hsiao et al. Modification of host cell membrane lipid composition by the intra-erythrocytic human malaria parasite Plasmodium falciparum.  . 1991 PMID: [2001227](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1149929/pdf/biochemj00165-0124.pdf) 
		  Table with pooled FAs actually also data for each PL
		![[fatty_acid_comp_in_per_cent_1991.png]]
	-  Mi-Ichi F et al. Intraerythrocytic Plasmodium falciparum utilize a broad range of serum-derived fatty acids with limited modification for their growth.  Parasitology. 2006 PMID: [16780611](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8C0EED41CD493EAE21D8A177058D3A60/S0031182006000540a.pdf/intraerythrocytic-plasmodium-falciparum-utilize-a-broad-range-of-serum-derived-fatty-acids-with-limited-modification-for-their-growth.pdf)
		- ![[fatty_acid_comp_2006_dodgy.png]]
- Carbohydrates
	- Only essential from Neidhardt FC, Ingraham J, Schaechter M. Physiology of the Bacterial Cell: A  Molecular Approach. Sunderland, Massachusetts: Sinauer Associates; 1990.
	- calculated by their frequency assuming a distribution proportional to the number of carbons present in their molecular composition

## Using iPfa to study its metabolism in the blood and liver stages. 
iPfa can be implemented to study the metabolism of P. falciparum during the blood and liver stages. Here, we suggest some modifications of iPfa that would render better context-specific  
predictions.  
For modeling of blood-stage specific metabolism, the protein N6-(lipoyl)lysine in apicoplast  
(whose metabolite ID in iPfa is C16237_a) should be removed from the biomass. This  
metabolite is a precursor of the lipoyl-ACP, which is a cofactor of the pyruvate  
dehydrogenase complex in apicoplast, and its production requires the fatty acid synthesis  
II (FAS II) pathway in this compartment to be active. This pathway has been  
experimentally observed as dispensable during the blood stages but essential during the  
liver stages [61] (S2 Table).  
For modeling the liver-stage specific metabolism, the uptake of hemoglobin (whose rxn ID  
in iPfa is T_c_to_e_C05781) should be prohibited and the reaction that represents the  
hemoglobin digestion (HBDG_c) should be blocked or erased, since this molecule is not  
supposed to be accessible inside the hepatocyte cell.