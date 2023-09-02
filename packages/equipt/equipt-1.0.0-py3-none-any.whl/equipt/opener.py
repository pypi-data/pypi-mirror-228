import pandas as pd
import numpy as np

def lc480_importer(ct_file):
    '''
    Imports excel or csv files output from a LightCycler 480
    for analysis.
    
    Param
    _____
    
    ct_file : str
        Path to qPCR data file
        
    Returns
    _______
    
    output : a dataframe
        a Pandas DataFrame containing the imported qPCR data
        
    '''
    if ct_file[-4:] == 'xlsx':
        return pd.read_excel(ct_file, 
                             header=1, 
                             usecols=['Pos','Cp'],
                             sep='\t')
    else:
        return pd.read_csv(ct_file, 
                             header=1, 
                             usecols=['Pos','Cp'],
                             sep='\t')

# Sample namer
def namer(ct_file,
         primers,
         samples,
         reps, 
         config='line',
         importer=None,
         **kwargs
         ):
    
    '''
    Imports qPCR data and adds sample and primer names. Additionally, adds
    dilutions if required. The output of namer() is used in all subsequent
    analysis tools.
    
    Params
    ______
    
    ct_file : str
        Path to a CSV or Excel file containing the qPCR data. Currently only
        data output from a Lightcycler 480 is supported, but the structure of 
        namer() allows for other importers to be written without disrupting the
        rest of the function.
        
    primers : list of strings
        A list, in order, of the primers. See documentation for supported plate
        arrangements.
        
    samples : list of strings
        A list, in order, or the sample names. See documentation for supported
        plate arrangements.
        
    reps : int
        Number of replicate wells. 2, 3, or 4.
        
    config : str
        A description of how the samples are arranged: 'square' or 'line'. See
        documentation for additional details. Default 'line'
        
    importer : a custom importer function or None
        A user-supplied function that imports data from their qPCR instrument 
        to a Pandas Dataframe with columns 'Pos', for the well position, and
        'Cp' for the Ct values. If None, namer() defaults to an importer for
        data from the Roche Lightcycler 480. Default None
        
    **kwargs : dictionary
        
        with_dil : list of strings
            List of names of samples that have dilution curves.
            
        dil_series : list of ints
            List of dilution factors in order on plate. Dilutions
            should be entered as integers (e.g. a 1:10 dilution 
            should be entered as 10).
            
        dil_rest : int or None
            The dilution of samples that do not have a dilution 
            series. If None, with_dil should contain all samples.
    '''
    
    # Check for valid replicate number
    valid_reps = [2,3,4]
    
    if reps in valid_reps:
        pass
    else:
        raise ValueError('Accepted replicate numbers are 2, 3, and 4.')
    
    
    # Check for invalid conformation
    if reps == 2 and config == 'square':
        ask = input('''You have entered only two technical replicates, 
        but have asserted they are arranged in a square. Would you like to: 
        \n 1) Proceed with line option setting
        \n 2) Cancel analysis and correct replicate number \n''')
        
        if ask == '1':
            config = 'line'
            print('\n Proceeding with line')
        elif ask == '2':
            return print('\n You have chosen to cancel. Please correct your technical replicates.')
        else:
            raise ValueError('''Please enter '1' or '2'.''')
            
    else:
        pass
    
    # Handle dilutions
    if kwargs:
        update_ls = []
        
        for i in samples:
            if i in kwargs['with_dil']:
                for j in kwargs['dil_series']:
                    update_ls.append('_'.join([i,str(j)]))
                            
            else:
                update_ls.append('_'.join([i,str(kwargs['dil_rest'])]))
        
        samples = update_ls
        
    else:
        pass
    
    # Read in the data
    if importer == None:
        ct_data = lc480_importer(ct_file)
    else:
        ct_data = importer(ct_file)
    
    # Drop empty wells
    ct_data.dropna(inplace=True, ignore_index=True)
    
    # Check that no wells were erroneously removed
    totalwells = len(primers) * len(samples) * reps
    
    if len(ct_data) == totalwells:
        pass
    else:
        raise Exception('''The total number of wells indicated differs from thenumber of wells with Ct values. This usually indicates that some wells did not produce enough PCR product to measure. 
        
        If you wish to proceed analyzing anyway, set the errant NaN values to "exclude". This will flag the wells for removal after naming is completed. Note that excluding entire primer-sample pairs may raise errors in downstreamanalyses.''')
    
    # Primer list (same regardless of configuration)
    primls = []
        
    for p in primers:
        for r in range(reps * len(samples)):
            primls.append(p)
            
    ct_data['Primer'] = primls
    
    # Line configuration
    if config == 'line':
        
        # Sample list
        names = []
        
        for s in samples:
            for r in range(reps):
                names.append(s)
                
        names = names * len(primers)
        
        ct_data['Name'] = names
     
    # Square configuration
    elif config == 'square':
        
        if reps == 3:
            names = list(np.zeros(len(samples)*reps))

            for i,s in enumerate(samples):
                z = 2*i
                s_inds = [z, z+1, z+2*len(samples)-i]

                for ind in s_inds:
                    names[ind] = s

            names = names * len(primers)
            
            ct_data['Name'] = names
            
        elif reps == 4:
            
           # Sample list
            names = []

            for s in samples:
                for r in range(2):
                    names.append(s)

            names = names * len(primers) * 2

            ct_data['Name'] = names 
            
    else:
        raise Exception('Unrecognized config. Choose "line" or "square".')
        
    ct_data['NamePrim'] = ct_data['Name'] + ct_data['Primer']
    
    ct_data = ct_data[ct_data['Cp'] != 'exclude']
    ct_data = ct_data.astype({'Cp':float})
        
    return ct_data
