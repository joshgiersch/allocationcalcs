import pandas as pd

#Data from Reuters, using the "$10k reinvested" function to get a total-return series
file_list = ['eem', 'sti_usd', 'iwda']
timeseries = pd.DataFrame(data={"Date":[]})
timeseries = timeseries.set_index('Date')
returnseries = pd.DataFrame(data={"Date":[]})
returnseries = returnseries.set_index('Date')

for filename in file_list:
    with open(filename + ".csv") as f:
        temp_frame = pd.read_csv(f, index_col=0, parse_dates=[0])
        f.close()
        
        #uggghhh strip thousands separators
        temp_frame["Performance"] = temp_frame["Performance"].apply(lambda x: float(x.split()[0].replace(',', '')))
        
        temp_frame["Performance"] = temp_frame["Performance"].astype(pd.np.float64)
        timeseries = timeseries.join(temp_frame, rsuffix = "_" + filename, how="outer") 
        
        temp_frame["Return"] = temp_frame["Performance"].pct_change()
        temp_frame = temp_frame.drop("Performance", axis=1)
        returnseries = returnseries.join(temp_frame, rsuffix = "_" + filename, how="outer")  

print(returnseries.corr())

