import os
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
cwd='staining of induced aggregates\\'


BIP=r'BIP/PFF/tif'
Congo=r'Congo/PFF/tif'
HSP=r'HSP60/PFF/tif'
pasyn=r'pasyn/PFF/tif'


#%% Loop through samples and find PCC scores
data={}
for sample in [BIP, Congo, HSP, pasyn]:
    wells=list(set([file.split('_')[1] for file in os.listdir(sample)]))
    numbers=list(set([file.split('_')[2] for file in os.listdir(sample)]))
    endings=list(set([file.split('_',3)[3] for file in os.listdir(sample)]))
    
    for well in wells:
        well_data=[]
        for number in numbers:
            if 'Congo' in sample:
                cy2=plt.imread((sample+"\\"+'img_{}_{}_'.format(well, number)+endings[0]))
                cy5=plt.imread((sample+"\\"+'img_{}_{}_'.format(well, number)+endings[2]))
            else:
                cy2=plt.imread((sample+"\\"+'img_{}_{}_'.format(well, number)+endings[0]))
                cy5=plt.imread((sample+"\\"+'img_{}_{}_'.format(well, number)+endings[1]))
            well_data.append(pearsonr(cy2.ravel(), cy5.ravel())[0])
        data[well]=well_data
        
#%% Calculate averages and variance for each sample
     
BIP_wells=['B11','C11','D11']
Congo_wells=['E11','F11','G11']
HSP_wells=['E06','F06','G06']
pasyn_wells=['B06','C06','D06'] 

well_average_coloc={}
for name, _wells in zip(['pasyn','BIP','Congo','HSP'],[pasyn_wells,BIP_wells,Congo_wells,HSP_wells]):
    well_average_coloc[name]={}
    well_average_coloc[name]['mean']=np.nanmean([np.mean(data[_well]) for _well in _wells])
    well_average_coloc[name]['stdev']=np.nanstd([np.mean(data[_well]) for _well in _wells])
        
df=pd.DataFrame(well_average_coloc).T

#%% Plot PCC scores as barchart

fig1, ax=plt.subplots(figsize=(3,3), dpi=300)
ax.bar(df.index, df['mean'],yerr=df['stdev'],width=0.6, capsize=6, align='center', edgecolor='black')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylabel('PearsonR score \n (PCC)')
plt.tight_layout()
plt.savefig(cwd+'PCC_Barchart.eps', dpi=300)
