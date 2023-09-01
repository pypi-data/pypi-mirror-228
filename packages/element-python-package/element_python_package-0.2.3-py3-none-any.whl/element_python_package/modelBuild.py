from sklearn.preprocessing import StandardScaler



def zero_share(dt, col, zero_sh):
	'''
	Modulates the number of zeros in a dataset based on a specific column. 

	dt : pandas dataframe.
	col: column to monitor zero share on. 
	zero_sh: fraction of zeros to be included.
	'''
    dt_zeros = dt[dt[col] == 0]
    dt_pos = dt[dt[col] > 0]

    zero_mod = dt.sample(frac = zero_sh)
    ignored_zero = dt_zeros[~(dt_zeros.sfdc_customer_id.isin(zero_mod.sfdc_customer_id.unique()))]
    dt_zero_mod = pd.concat([dt_pos, zero_mod])
    
    return dt_zero_mod, ignored_zero

 def scale_data(dt, scaler_given = None):
 	'''
 	dt: pandas dataframe
 	scaler_given: existing scaler to transform data
 	'''
    num_cols = dt.dtypes[dt.dtypes != 'object'].index
    o_data = dt[[i for i in dt.columns if i not in num_cols]]
    n_data = dt[num_cols]
    if scaler_given == None: 
        scaler = StandardScaler()
        scaler_fit = scaler.fit(n_data)
    else:
        scaler_fit = scaler_given
        scaler = scaler_given
    
    scaled = scaler_fit.transform(n_data)
    scaled = pd.DataFrame(scaled)
    scaled.columns = n_data.columns
    scaled_dt = o_data.join(scaled)
    
    return scaled_dt, scaler