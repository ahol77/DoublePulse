"# DoublePulse" 

Functions:
LoadData - Read specs from syncdata
FitSeed - Fit Gaussians to the seeded region of the specs
FitSASE - Fit Guassians to the SASE region of the specs

CreateDataFrames - Produce good fits for both seeded and SASE regions
CombineAndEditData - Remove bad fits and merge datasets into one large one
	- will also split data by SASE and Seed energies

Correlations - Observe trends by binning data along different axis
FirstCorrelation - Look at first split data
LastCorrelation - Look at last split data
BadDataAnalysis - Look at averages and general trend of all good and bad data