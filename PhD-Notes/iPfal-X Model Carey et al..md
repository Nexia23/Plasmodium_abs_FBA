
## Biomass
From [Plata et al. 2010](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117):
As the _P. falciparum_ biomass objective function cannot be completely established based on the available literature, in our calculations we used a modified version of the yeast objective function reported in the iND750 model ([Duarte et al, 2004](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#b30)). The objective function modifications included the lipid composition, which was adjusted as reported for _Plasmodium_ ([Hsiao et al, 1991](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#b49)), and amino acid and nucleotide compositions adjusted based on the proteome and genome sequences weighted by available expression data ([Llinas et al, 2006](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#b79)). In particular, the percent prevalence of each ribonucleotide and amino acid across all open reading frames (ORFs) was calculated as the relative frequency of each monomer; the counts at each ORF were multiplied by the ORF's expression level (when available). The percent prevalence of the dNTPs was derived from the genome A+T content of 80.6%. These percentages were converted to mmol/gDW as described ([Chavali et al, 2008](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#b15)). Systems Biology Research Tool ([Wright and Wagner, 2008](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#b136)) was used to perform FBA ([Edwards et al, 1999](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#b31)) of the network, including single and double _in silico_ deletions of network enzymes. The reconstructed network was able to either synthesize or import all the biomass components presented in [Supplementary Table S1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#S1). The assembled metabolic model is available as an Excel spreadsheet ([Supplementary information](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#S1)) and in the Systems Biology Markup Language (SBML) format ([Supplementary information](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#S1)). The SBML model was submitted to the BioModels database ([Le Novere et al, 2006](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2964117/#b74)) with accession number MODEL1007060000.

No general revision of Biomass besides in the first implementation 2017, where especially the lipid biomass was updated. Data used is [Gulati et al. 2015](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4567697/) 
Profiling the essential nature of lipid metabolism in asexual blood and gametocyte stages of plasmodium falciparum. They use only relative values of total lipid content, thus even though PS is produced (according to Alex Maier's data-set) not as biomass component defined in model, since relatively lower than in uRBC  

### Lipid production
Lipid production can happen in two ways, either import of pseudo lipid for biomass or production of pseudo lipid through lipid metabolism. Import option has a better objective value (~5% difference).

**Production through lipid metabolism:**
- PC is properly produced by addition of cdpchol_c to dag_c (0.02%), rest imported
- PE is imported as 2agpe120_e (2-Acyl-sn-glycero-3-phosphoethanolamine (n-C12:0))
- DAG produced mainly by phosphatidylinositol phospholipase C(75.8%) and a quarter by sphingomyelin synthase (24.2%) 
	--> questionable at best since high DAG demand for production of PC, PE and PS in reality, here only 0.2% flux into PC
- Cholesterol imported during which ATP generated
- TAG produced using DAG
- Ceramid produced by imported human Sphingomyelin
- Sphingomyelin produced by Ceramid and either PC or CDP-Choline
- PI produced by CDP-DAG and inositol (0.2%), rest imported
- PG produced by Phosphatidylglycerol (ditetradec-7-enoyl, n-C14:1)
