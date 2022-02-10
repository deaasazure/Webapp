import logging
import traceback
import pandas as pd


class ExploreClass:
    
    def get_dataset_statistics(self,data_df):
        #? Logical Code Begins
        try:
            # data_df=spark_df.toPandas()
            data_df.reset_index(drop=True,inplace = True)
            
            added_col = False
            if (type(data_df) is pd.Series):
                arr = [0]*len(data_df)
                series = pd.Series(arr)
                data_df = pd.DataFrame([data_df, series], columns = [data_df.name, 'auto_generated_column'])
                added_col = True

            #? Getting Statistics
            stats_df = data_df.describe(include = 'all')
            stats_df = stats_df.T
            
            #? Changing The Column Names
            stats_df.rename(columns = {'unique':'Unique Values'}, inplace = True)    
            stats_df.rename(columns = {'count':'Non-Null Values'}, inplace = True)  
            stats_df.rename(columns = {'mean':'Mean'}, inplace = True)
            stats_df.rename(columns = {'std':'Std'}, inplace = True)    
            stats_df.rename(columns = {'min':'Min Value'}, inplace = True)    
            stats_df.rename(columns = {'max':'Max Value'}, inplace = True)    

            try:
                #? Removing unnecessary columns
                stats_df.drop('top',axis=1, inplace=True)
                stats_df.drop('freq',axis=1, inplace=True)
            except:
                #? If the column wasn't already there then
                pass

            #? Changing Column Datatypes
            stats_df['Mean'] = stats_df['Mean'].astype(float)
            stats_df['Std'] = stats_df['Std'].astype(float)
            stats_df['Min Value'] = stats_df['Min Value'].astype(float)
            stats_df['Max Value'] = stats_df['Max Value'].astype(float)
            stats_df['25%'] = stats_df['25%'].astype(float)
            stats_df['50%'] = stats_df['50%'].astype(float)
            stats_df['75%'] = stats_df['75%'].astype(float)

            #? Defining All the Columns that are not in the DataFrame.describe() method but are needed for the exploration page
            stats_df["Null Values"] = len(data_df) - stats_df['Non-Null Values']
            stats_df["Null Values"] = stats_df['Null Values'].astype(int)
            stats_df["Non-Null Values"] = stats_df['Non-Null Values'].astype(int)
            stats_df["DataCount"] = len(data_df)
            stats_df["Missing Values %"] = stats_df["Null Values"] / ((stats_df["Null Values"] + stats_df["Non-Null Values"]) * 100)

            stats_df['1 Column Name'] = 0
            i = 0
            axislist = []
            IQR = stats_df['75%']-stats_df['25%']
            stats_df['open'] = stats_df['25%']-1.5 * IQR
            stats_df['close'] = stats_df['75%']+1.5 * IQR
            stats_df['open'] = stats_df['open'].astype(float)
            stats_df['close'] = stats_df['close'].astype(float)
            stats_df['1 Column Name']=stats_df.index

            # Outlier detection
            outliers_list = []
            for col in data_df.columns:
                # print(col)
                s = data_df[col]
                if s.dtype!='object':
                    q1 = s.quantile(0.25)
                    q3 = s.quantile(0.75)
                    iqr = q3 - q1
                    iqr_lower = q1 - 1.5 * iqr
                    iqr_upper = q3 + 1.5 * iqr
                    outliers = dict(s[(s < iqr_lower) | (s > iqr_upper)])
                    outliers_list.append(str(outliers))
                else:
                    outliers_list.append('NaN')
            stats_df['Outliers'] = outliers_list

            # Finding data type of columns
            dtypes_list = []        
            for col in data_df.columns:
                if data_df[col].dtype=="object":
                    dtypes_list.append("categorical")
                else:
                    dtypes_list.append("numerical")
            stats_df['Column_dtypes'] = dtypes_list        

            # Finding total number of duplicate entries
            num_of_duplicates_list = []
            for col in data_df.columns:
                num_of_duplicates_list.append(data_df[col].duplicated().sum())
            stats_df['Duplicates'] = num_of_duplicates_list

            # Finding duplicate entries
            duplicates_list = []
            for col in data_df.columns:
                duplicates_list.append(data_df[data_df[col].duplicated()==False][col].values.tolist())    
            stats_df['Duplicate_entries'] = duplicates_list

            # Finding correlation between columns
            corr_val_list = []
            for col in data_df.columns:
                if data_df[col].dtypes!='object':
                    corr_val_list.append(str(data_df.corr()[col].to_dict()))
                else:
                    corr_val_list.append("{}")
            stats_df['Correlation'] = corr_val_list

            # value counts (Number of time elements occurs in the column)
            value_counts_list = []
            for col in data_df.columns:
                if data_df[col].dtypes!='object':
                    value_counts_list.append(str(data_df[col].value_counts().to_dict()))
                else:
                    value_counts_list.append("{}")
            stats_df['Value_counts'] = value_counts_list

            stats_df = stats_df.reindex(columns=sorted(stats_df.columns))
            stats_df.rename(columns = {'1 Column Name':'column_name'}, inplace = True)
            stats_df.rename(columns = {'25%':'percent_25'}, inplace = True)
            stats_df.rename(columns = {'50%':'percent_50'}, inplace = True)
            stats_df.rename(columns = {'75%':'percent_75'}, inplace = True)
            stats_df.rename(columns = {'DataCount':'data_count'}, inplace = True)
            stats_df.rename(columns = {'Max Value':'max_val'}, inplace = True)
            stats_df.rename(columns = {'Mean':'mean_val'}, inplace = True)
            stats_df.rename(columns = {'Min Value':'min_val'}, inplace = True)
            stats_df.rename(columns = {'Missing Values %':'missing_val'}, inplace = True)
            stats_df.rename(columns = {'Non-Null Values':'non_val'}, inplace = True)
            stats_df.rename(columns = {'Null Values':'null_val'}, inplace = True)
            stats_df.rename(columns = {'Outliers':'outliers_val'}, inplace = True)
            stats_df.rename(columns = {'Std':'std_dev'}, inplace = True)
            stats_df.rename(columns = {'Unique Values':'unique_val'}, inplace = True)
            stats_df.rename(columns = {'close':'close_val'}, inplace = True)
            stats_df.rename(columns = {'open':'open_val'}, inplace = True)
            stats_df.rename(columns = {'Column_dtypes':'columns_dtypes'}, inplace = True)
            stats_df.rename(columns = {'Duplicates':'duplicates_val'}, inplace = True)
            stats_df.rename(columns = {'Duplicate_entries':'duplicate_entries_val'}, inplace = True)
            stats_df.rename(columns = {'Correlation':'correlation_val'}, inplace = True)
            stats_df.rename(columns = {'Value_counts':'value_counts_val'}, inplace = True)

            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
#             print(stats_df.head())
            return stats_df  
        except Exception as exc:
            logging.info("Error has been occurred as ", str(exc))
            return 0

