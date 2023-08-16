### Stoichiometric factor
Neither #Carey2017 nor #Chiappino-Pepe2017 have a good documentation of the calculation for the biomass:
- #Carey2017 uses #Plata2010 who in turn uses #Chavali but updated the DNA, RNA and lipid compositions to plasmodium, dry weight composition might be the same no explanation 
- For #Chiappino-Pepe2017 from supplement I understood this:
	As example the phospholipid PC:  
	PC content in PL => c_PC = 56,7% mol PC/ mol phospholipids(PL); from Hsiao et al. ([https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1149929/?page=6](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1149929/?page=6))  
	PL concentration in parasite => c_PL = ~1.9 µmol PL/10⁹cells; from Palacpac et al.([https://doi.org/10.1242/jcs.00988](https://doi.org/10.1242/jcs.00988))   
	Parasite dry weight => m_DW = 10.5 10⁻¹² g; from Forth thesis  
	-> in newer [publication][https://www.sciencedirect.com/science/article/pii/S0092867419311808#mmc3] detailed biomass composition table
	-> in emails explained the choice of metabolites 
		Quote: "I didn’t include riboflavin in the biomass equation because its metabolic products FMN and FAD are included. I always tried to include in the biomass equation the last important product in a metabolic pathway."

### Metabolite inclusion
#Chiappino-Pepe2017 not included:
- 5-Methyltetrahydrofolate, #Carey2017 uses 5_10_Methylenetetrahydrofolate to directly produce Tetrahydrofolate not the intermediate step of 5-Methyltetrahydrofolate
- Biotin, KEGG has part of pathway documented (fatty acid biosynthesis) but not the enzymes close to biotin
	- biotin not so important doi: 10.1073/pnas.1800717115
- Methylcobalamin Vitamine B12 maybe later addition https://doi.org/10.1016/j.jinorgbio.2007.01.006
- Protein N6-(lipoyl)lysine' could be included possibly pyruvate dehydrogenase, a-ketoglutarate dehydrogenase, but grouped reaction in ipfal probably in protein biomass
	- doi: 10.1111/j.1365-2958.2007.05592.x
- UDP-D-galactose sugar bind for glyco-lipids/proteins should be added https://doi.org/10.1186/s12936-015-0949-z 
	- in iPFA used as substitute for all GPI
