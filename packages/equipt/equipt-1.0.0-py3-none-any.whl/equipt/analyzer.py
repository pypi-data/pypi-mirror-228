import pandas as pd
import numpy as np

from itertools import chain

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import bokeh.plotting as plt
from bokeh.layouts import gridplot

import pandas as pd
import numpy as np

from itertools import chain

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import bokeh.plotting as plt
from bokeh.layouts import gridplot

def avg_base(ct_data):
    '''
    Computes average Ct values and errors for sample-primer pairs
    from namer output
    
    Params
    ______
    
    ct_data : a dataframe
        Output of namer().
        
    Returns
    _______
    
    output : a dataframe
        A Pandas Dataframe containing average Ct values and standard deviation
        for sample-primer pairs  
    
    '''
    # Save unique sample-primer pairs
    uniques = np.unique(ct_data['NamePrim'])
    
    avgdf = pd.DataFrame(np.zeros([len(uniques),5]),
                        columns=['Primer','Name','NamePrim','AvgCt','StdCt'])
    
    # Iterate through primer-sample pairs to get averages
    for i, u in enumerate(uniques):
        # Subset dataframe
        subdf = ct_data[ct_data['NamePrim'] == u]
        
        # Update sample ID information on average dataframe
        avgdf.loc[i,'Primer'] = subdf.iloc[0]['Primer']
        avgdf.loc[i,'Name'] = subdf.iloc[0]['Name']
        avgdf.loc[i,'NamePrim'] = subdf.iloc[0]['NamePrim']
        
        # Calculate averages
        avgdf.loc[i,'AvgCt'] = np.mean(subdf['Cp'])
        avgdf.loc[i,'StdCt'] = np.std(subdf['Cp'])
        
    return avgdf

def averager(ct_data,
             reps,
             thresh=0.1,
             update_data=False):
    '''
    Runs avg_base and removes divergent replicate wells. Wells are removed 
    until each sample-primer pair has a standard deviation less than or equal
    to a user-specified threshold.
    
    Params
    ______
    
    ct_data : a dataframe
        Output of namer().
        
    reps : int
        The number of replicate wells in the sample. Used to flag sample-
        primer pairs where more than half the wells have been removed. Is
        not used if thresh == None.

    thresh : float or None
        Highest acceptable standard deviation for a set of sample-primer
        replicate wells. If set to None no wells are removed. Default 0.1
        
    update_data : Bool
        Whether to alter the input dataframe in place or to leave it unaffected.
        
    Returns
    _______
    
    output : a dataframe
        A Pandas Dataframe containing average Ct values and standard deviation
        for sample-primer pairs. Identical to the output of averager with
        replicates removed.
        
    droppedWells.txt : a text file
        A text file containing the number of replicates dropped for each sample
        -primer pair.
        
    '''
    
    x = 0
    dropped = []
    
    while x == 0:
        avg = avg_base(ct_data)
        
        if thresh == None:
            x += 1
            
        elif all([i <= thresh for i in avg['StdCt']]):
            x += 1
            
        else:
            avg = avg[avg['StdCt'] > thresh]['NamePrim']
            subdf = ct_data[ct_data['NamePrim'].isin(avg)].copy()
            subdf.reset_index(inplace=True)
            
            nameprim = np.unique(subdf['NamePrim'])
            dropped.append(nameprim)
            
            for n in nameprim:
                filtdf = subdf[subdf['NamePrim'] == n]
       
                arr = np.array(filtdf['Cp'])
                arrsize = len(filtdf)
                subtract = np.zeros((arrsize,arrsize))
                
                
                for i,v in enumerate(arr):
                    subtract[i] = arr - v
                    
                subtract = np.sum(subtract,1)
                subtract = np.abs(subtract)
                subtract = np.argmax(subtract)
                subtract = filtdf.iloc[subtract]['index']
                
                if update_data == False:
                    ct_data = ct_data.drop(subtract)
                else:
                    ct_data.drop(subtract,inplace=True)
    
    if len(dropped) == 0:
        pass
    else:
        dropped = list(chain.from_iterable(dropped))
        drop_txt = ['Outlier Wells Dropped:\n']
        drop_dict = {}

        for i in dropped:
            drop_dict[i] = dropped.count(i)
            drop_txt.append(i + ' - ' + str(drop_dict[i]) + '\n')
        
        drop_txt.append('\n')
        drop_txt.append('Samples Removed:' + '\n')
        
        for i in drop_dict:
            if drop_dict[i] >= 0.5*reps:
                avg = avg[avg['NamePrim'] != i]
                drop_txt.append(i + '\n')
            else:
                pass
            
        with open('droppedWells.txt', 'w') as f:
             f.writelines(drop_txt)
                
    return avg

def deltact(ct_data,
            housekeeping,
            reps,
            dilution=None,
            thresh=0.1,
            exp_ctrl=None,
            foldchange=False 
            ):
    '''
    Performs delta Ct, delta delta Ct, and/or fold change analysis on output of
    namer().
    
    Params
    ______
    
    ct_data : a dataframe
        Output of namer().
        
    housekeeping : list
        A list of housekeeping primers.
        
    reps : int
        The number of replicate wells per sample-primer pair in the experiment.
        
    dilution : int or None
        If all samples have the same dilution factor, set to None. If samples
        have different dilution factors, set to the dilution factor of samples
        to be included in the dCt analysis. Default None
        
    thresh : float or None
        Highest acceptable standard deviation of replicate wells. If None, no 
        thresholding is performed. If float, divergent wells are removed until
        replicate wells have acceptable deviation, and the number of removed 
        wells for each sample primer pair is sent to droppedWells.txt. 
        
    exp_ctrl : dictionary or None
        A dictionary containing pairs of experimental and control samples for
        ddCt analysis, e.g. {'+Drug1':'DMSO','+Drug2':'DMSO'}. If None, only
        dCt will be returned.
        
    foldchange : Bool
        Whether to convert ddCt values to fold change. Requires a valid
        dictionary for exp_ctrl.
        
    Returns
    _______
    
    output : a dataframe
        A Pandas DataFrame containing the specified calculations.
    
    '''
    # Create log file
    log = open('deltaCtLog.out','a')
    
    # Check for dilution
    if dilution == None:
        pass
    else:
        dil_ls = [i.split('_') for i in ct_data['Name']]
        ct_data['Dilutions'] = [int(i[-1]) for i in dil_ls]
        ct_data['Name'] = [''.join(i) for i in dil_ls]
        
        ct_data = ct_data[ct_data['Dilutions'] == dilution]
        
    # Check incompatible settings 
    if exp_ctrl == None and foldchange == True:
        raise Exception('''Fold change is calculated from ddCt. To calculate fold change, "exp_ctrl" must hold a dictionary.''')
    else:
        pass
    
    # Compute averages 
    avgdf = averager(ct_data,reps,thresh=thresh)
        
    # Check for appropriate housekeeping controls
    if len(housekeeping) == 1:
        ask = input('''Warning: Using only one housekeeping gene severely limits result accuracy.
                    \n Do you want to proceed? [Y/N]''')
        
        if ask == 'Y':
            log.write('Proceeded with only one housekeeping gene \n')
            log.write('\n')
            print('Proceeding with delta Ct analysis.')
            
        elif ask == 'N':
            return print('Analysis canceled.')
        
        else:
            raise ValueError('Please enter Y or N to the warning prompt.')
        
    else:
        pass
    
    
    # Batch together housekeeping genes
    names = np.unique(avgdf['Name'])
    
    log.write('Samples removed because housekeeping sample did not pass threshold:')
    
    for n in names:
        subdf = avgdf[avgdf['Name']==n]
        subdf = subdf[subdf['Primer'].isin(housekeeping)]
        
        # Drop samples where housekeeping genes did not pass threshold
        if len(subdf) < len(housekeeping):
            log.write('\n' + n)
            avgdf = avgdf[avgdf['Name'] != n]
        
        else:
            errorprop = 0.5 * np.sqrt(np.sum([i**2 for i in subdf['StdCt']]))

            series = pd.Series({'Name':n,
                               'Primer':'housekeeping',
                               'AvgCt':np.mean(subdf['AvgCt']),
                               'StdCt':errorprop
                                   })

            avgdf = pd.concat([avgdf,series.to_frame().T],ignore_index=True)
    
    # Regenerate names list after filtering
    names = np.unique(avgdf['Name'])
    
    # Make dictionary of empty lists
    dct_dict = {'Name':[],
               'Primer':[],
               'dCt':[],
               'StdErr':[]}
    
    for i, n in enumerate(names):
        # Subset df
        subdf = avgdf[avgdf['Name']==n]
        
        # Generate primers list and reset index
        primers = np.unique(subdf['Primer'])
        subdf.set_index('Primer',inplace=True)
        
        for p in primers:
            if p in housekeeping:
                pass
            elif p == 'housekeeping':
                pass
            else:
                # Calculate dCt and propagate error
                dct = subdf.loc[p,'AvgCt'] - subdf.loc['housekeeping','AvgCt']
                err = np.sqrt(subdf.loc[p,'StdCt']**2 + subdf.loc['housekeeping','StdCt']**2)
                
                # Update dictionary
                dct_dict['Name'].append(n)
                dct_dict['Primer'].append(p)
                dct_dict['dCt'].append(dct)
                dct_dict['StdErr'].append(err)
                
    # Convert dictionary to dataframe
    dct_df = pd.DataFrame(dct_dict)
    
    if exp_ctrl == None:
        return dct_df
    else:
        pass
    
    # Update log to keep track of ddCt analysis
    log.write('\nSamples dropped due to avgfilt thresholding:\n')
    
    log.write('\nPrimer\tExperimental\tControl')
    
    # Set index to nameprim for easy location
    dct_df['NamePrim'] = dct_df['Name'] + dct_df['Primer']
    dct_df.set_index('NamePrim',inplace=True)
    
    # Collect the names of the primers used
    dct_prims = np.unique(dct_df['Primer'])
    
    # Make dictionary of empty lists
    ddct_dict = {'Experimental':[],
                'Control':[],
                'Primer':[],
                'Exp dCt':[],
                'ddCt':[],
                'StdErr':[]}
    
    # Calculate delta delta Ct values (experimental dCt - control dCt)
    for e in exp_ctrl:
        # Identify control sample
        c = exp_ctrl[e]
        
        # Loop through primers
        for p in dct_prims:
            # Identify indices
            e_prim = e + p
            c_prim = c + p
            
            # Check that both still exist
            ind_ls = [i in dct_df.index for i in [e_prim,c_prim]]
            
            if all(ind_ls):
                # Calculate ddCt and propagate error
                ddct = dct_df.loc[e_prim,'dCt'] - dct_df.loc[c_prim,'dCt']
                err = np.sqrt(dct_df.loc[e_prim,'StdErr']**2 + dct_df.loc[c_prim,'StdErr']**2)

                # Update dictionary
                ddct_dict['Experimental'].append(e)
                ddct_dict['Control'].append(c)
                ddct_dict['Primer'].append(p)
                ddct_dict['Exp dCt'].append(dct_df.loc[e_prim,'dCt'])
                ddct_dict['ddCt'].append(ddct)
                ddct_dict['StdErr'].append(err)
                
            else:
                log.write('\n'+p+'\t'+e+'\t'+c+'\t')
            
    # Convert dictionary to dataframe
    ddct_df = pd.DataFrame(ddct_dict)
    
    # Calculate fold change if specified
    if foldchange == True:
        ddct_df['FoldChange'] = 2**(-1 * ddct_df['ddCt'])
    else:
        pass
    
    # Return dataframe
    return ddct_df

def efficiency(ct_in, # output from namer
              with_dil,
              returnmodel=False, # Whether or not to output the linear model in full
              **kwargs):    
    
    '''
    Calculates efficiency of qPCR primers based on a standard curve. Returns
    efficiency values and log-transformed plots of the dilution curves.
    
    Params
    ______
    
    ct_data : a dataframe
        Output of namer().
        
    with_dil : list of strings
        List of samples that have dilution series. Generally has only one value,
        but in specific cases multiple samples may have curves.
        
    returnmodel : Bool
        Whether to return a dataframe containing the linear regression model. 
        Default False
        
    **kwargs : dictionary
    
        thresh : float
            The acceptable standard deviation of replicate well Ct values. 
            averager() is used to identify wells to drop.
            
        reps : int
            Number of replicate wells loaded per sample.
        
    Returns
    _______
    
    plot_dict : a dictionary
        A dictionary in which the keys are samples and the value is a list of
        Bokeh plots for each primer tested.
        
    eff_df : a dataframe
        A dataframe containing the efficiency values and R^2 statistic
        calculated for each sample-primer pair. 
        
    model_df : a dataframe
        Only returned if returnmodel == True. A dataframe containing the
        intercept and slope of the linear model for each sample-primer pair.
            
    '''
    # Copy dataframe
    ct_data = ct_in.copy()
    
    # Filter outlier wells
    if kwargs:
        averager(ct_data,kwargs['reps'],thresh=kwargs['thresh'],update_data=True)
    else:
        pass
    
    # Generate dilution column and remove from names
    name_ls = [i.split('_') for i in ct_data['Name']]

    ct_data['Dilution'] = [1/int(i[-1]) for i in name_ls]
    ct_data['Name'] = ['_'.join(i[:-1]) for i in name_ls]

    # Filter for samples with dilution curves
    ct_data = ct_data[ct_data['Name'].isin(with_dil)]

    # Calculate log2 dilution
    ct_data['Log2Dil'] = np.log2(ct_data['Dilution'])

    # Initiate dictionaries for efficiency values and plots
    eff_dict = {'Name':[],
               'Primer':[],
               'Efficiency':[],
               'Rsquared':[]}
    
    model_dict = {'Name':[],
                 'Primer':[],
                 'Coefficient':[],
                 'Intercept':[]}

    plot_dict = {}

    # Set linear regression prediction range
    minpred = min(ct_data['Log2Dil'])
    maxpred = max(ct_data['Log2Dil'])

    # Perform linear regression and update plots and efficiencies
    for n in np.unique(ct_data['Name']):
        plot_dict[n] = []
      
        # Subset by name
        subdf = ct_data[ct_data['Name'] == n]
        # Loop through primers
        for p in np.unique(subdf['Primer']):
            
            primdf = subdf[subdf['Primer'] == p]
            predrange = np.linspace(minpred,maxpred,len(primdf))[::-1]

            # Set up plot for ct values and regression line
            plot = plt.figure(title=' '.join([n,p]), height=400, width=400,
                              x_axis_label = 'Log2Dil', y_axis_label='Ct',)

            plot.circle(primdf['Log2Dil'].values, primdf['Cp'].values)

            # Perform linear regression
            eff_ld = np.array(primdf['Log2Dil']).reshape(-1,1)
            eff_cp = np.array(primdf['Cp'])

            reg = LinearRegression()
            reg.fit(eff_ld, eff_cp)

            bf = reg.predict(predrange.reshape(-1,1))

            # Update plots and calculate efficiency
            plot.line(predrange, bf)
            eff = 2**(-1 / reg.coef_) - 1
            eff = round(eff[0],3)

            rsquared = r2_score(np.array(primdf['Cp']), bf.reshape(len(bf)))

            eff_dict['Name'].append(n)
            eff_dict['Primer'].append(p)
            eff_dict['Efficiency'].append(eff)
            eff_dict['Rsquared'].append(rsquared)
            
            model_dict['Name'].append(n)
            model_dict['Primer'].append(p)
            model_dict['Coefficient'].append(round(reg.coef_[0],3))
            model_dict['Intercept'].append(round(reg.intercept_,3))

            plot_dict[n].append(plot)
            
    # Convert dicts to dfs
    eff_df = pd.DataFrame(eff_dict)
    model_df = pd.DataFrame(model_dict)
    
    # Return efficiency values with or without model
    if returnmodel == True:
        return plot_dict, eff_df, model_df
    else:
        return plot_dict, eff_df
