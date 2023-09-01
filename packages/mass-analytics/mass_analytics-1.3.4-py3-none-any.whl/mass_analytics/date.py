import pandas as pd
import numpy as np
import tqdm
import datetime
import os
from dateutil.parser import parse
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from .reader import read_data

    
def is_date(string):
    """
    Return whether the string can be interpreted as a date.

    Parameters:
        string (str): string to check for date
    """

    try:
        if type(string) is not str:
            return False
        parse(string, fuzzy=False)
        return True

    except ValueError:
        return False

def filter_date_only(serie):
    """
    
    """
    filter_dates_only = serie[serie.apply(lambda x: isinstance(x, datetime.datetime) or is_date(x))] 

    filter_dates_only = pd.Series(filter_dates_only.unique()) 

    if np.issubdtype(filter_dates_only.dtype, np.object_):
        try:
            filter_dates_only = pd.to_datetime(filter_dates_only)
        except:
            pass
        
    filter_dates_only = filter_dates_only.sort_values()

    return filter_dates_only

def get_date_columns(df):
    """
    Description
        Automatically determine the date column(s) in the DataFrame.

        The function analyzes the DataFrame columns and attempts to identify the column(s)
        containing date or datetime information. It returns either the name of the single
        date column as a string or a list of column names if multiple date columns are found.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be analyzed.

    Returns:
        Union[str, List[str]]: The name of the date column as a string if only one
        date column is found. If multiple date columns are detected, it returns a
        list of strings containing the names of all identified date columns.

    Raises:
        ValueError: If no date columns are found in the DataFrame.

    Example:
        >>> import pandas as pd
        >>> data = {
        ...     'Date': ['2023-07-01', '2023-07-02', '2023-07-03'],
        ...     'Temperature': [30, 32, 31],
        ...     'Humidity': [60, 65, 70],
        ... }
        >>> df = pd.DataFrame(data)
        >>> get_date_columns(df)
        'Date'

        >>> data = {
        ...     'Start_Date': ['2023-07-01', '2023-07-02', '2023-07-03'],
        ...     'End_Date': ['2023-07-05', '2023-07-06', '2023-07-07'],
        ... }
        >>> df = pd.DataFrame(data)
        >>> get_date_columns(df)
        ['Start_Date', 'End_Date']
    """
         
    # Result list
    date_columns = []
    
    NUMBER_OF_ROWS = df.shape[0]

    NUMBER_ROW_TO_CHECK = min(1000,NUMBER_OF_ROWS)
                    
    for column in df.columns:
        if np.issubdtype(df[column].dtype, np.datetime64):
            date_columns.append(column)
            continue
        elif np.issubdtype(df[column].dtype, np.object_):
            counter = 0
            index_range = np.random.choice(list(df.index),NUMBER_ROW_TO_CHECK,replace=False)
            for index in index_range:
                value = df[column][index]
                try:
                    pd.to_datetime(value)
                    counter += 1
                except:
                    continue
            
            if counter >= int(NUMBER_ROW_TO_CHECK * 0.50):
                date_columns.append(column)

    if len(date_columns) == 0:
        raise ValueError("No date columns found in the DataFrame.")
    if len(date_columns) == 1:
        return date_columns[0]
    else:
        return date_columns
        
def get_periodicity(df, *columns):
    """
    Description
        Determine the periodicity of the given DataFrame or specified columns.

        The function analyzes the DataFrame or specified columns and attempts to identify
        the data's periodicity, such as daily ('D'), weekly on Monday ('W-MON') or Saturday ('W-SAT'),
        or monthly ('M'). The function calculates the time interval between consecutive
        data points in the specified columns and returns the most likely periodicity based
        on the time differences.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be analyzed.
        *columns (str, optional): Names of the columns to consider when determining the periodicity.
                                If not provided, the entire DataFrame will be analyzed.

    Returns:
        dict: The periodicity identified in the DataFrame or specified columns.
            The returned value will be one of the following strings: 'D', 'W-MON', 'W-SAT', or 'M'.

    Raises:
        ValueError: If the specified column(s) do not exist in the DataFrame.

    Example:
        >>> import pandas as pd
        >>> data = {
        ...     'Date': ['2023-07-01', '2023-07-02', '2023-07-03'],
        ...     'Temperature': [30, 32, 31],
        ... }
        >>> df = pd.DataFrame(data)
        >>> get_periodicity(df, 'Date')
        {'Date': 'D'}

        >>> data = {
        ...     'Date': ['2023-07-01', '2023-07-08', '2023-07-15'],
        ...     'Temperature': [30, 32, 31],
        ... }
        >>> df = pd.DataFrame(data)
        >>> get_periodicity(df, 'Date')
        {'Date': 'W-SAT'}
    """

    if columns:
        for col in columns:
            if col not in df.columns:
                raise ValueError("The specified column(s) do not exist in the DataFrame.")
    else:
        columns = get_date_columns(df)
        if type(columns) is str:
            columns = [columns]

    periodicity = {} # Result variable

    for col in columns:
        col_serie = df[col]
            
        filter_dates_only = filter_date_only(col_serie)
        
        if filter_dates_only.size < 1000:
            range_slice = int(filter_dates_only.size / 3)
        else:
            range_slice = 333 
            
        periodicity_paterns = []
        start = 0
        len_to_check = 3
        for index in range(range_slice):
            try:
                periodicity_paterns.append(pd.infer_freq(filter_dates_only[start:start + len_to_check]))
            except:
                pass
            start += len_to_check
        
        if len(periodicity_paterns) > 0:
            periodicity[col] = max(set(periodicity_paterns), key = periodicity_paterns.count)
        else:
            periodicity[col] = 'None'

    return periodicity

def date_summary(path):
    """
    Description
        Generate a data frame summarizing the date-related information for each CSV, XLS, or XLSX file in the given path.

        Parameters:
        path (str): The directory path containing CSV, XLS, or XLSX files.

    Returns:
    pandas.DataFrame: A data frame with the following columns:
        - file_name (str): The name of the file.
        - date_columns (str): The column name that contain date-related data.
        - periodicity (str): The frequency of the date-related data (e.g., 'daily', 'monthly', 'yearly').
        - start_date : The earliest date found in the date-related columns.
        - end_date : The latest date found in the date-related columns.
        - prop_null % : The proportion of missing values (NaNs) in the date-related columns.
    Note:
       This function will only consider CSV, XLS, and XLSX files in the specified path.

    Example:
        >>> print(date_summary('.'))
          file_name date_columns periodicity  start_date    end_date  prop_null %
        0  data.csv        Date       daily  2023-07-01  2023-07-03          0.0
    """

    if os.path.isdir(path):
        for (dirpath, dirnames, filenames) in os.walk(path):
            break
    else:
        filenames = [os.path.basename(path).split('/')[-1]]

    new_df = {'file_name': [],
              'date_columns': [],
              'periodicity': [],
              'start_date': [],
              'end_date': [],
              'prop_null%': []
            }

    for file in tqdm.tqdm(filenames):
        try:
            if os.path.isdir(path):
                df = read_data(path+'/'+file)
            else:
                df = read_data(path)
        except Exception as e:
            print(e, file)
            continue  
        
        try:
            columns = get_date_columns(df)
        except Exception as e:
            print(e, file)
            continue
        
        if type(columns) is str:
            columns = [columns]

        #periodicity = get_periodicity(df)
        for col in columns:
            new_df['file_name'].append(file)
            new_df['date_columns'].append(col)
            new_df['periodicity'].append(get_periodicity(df,col)[col])
            col_serie = df[col]
            
            if np.issubdtype(df[col].dtype, np.object_):
                col_serie = col_serie[col_serie.apply(lambda x: isinstance(x, datetime.datetime) or is_date(x))]
                #col_serie = col_serie.astype('datetime64[ns]')
                col_serie = pd.to_datetime(pd.Series(col_serie), errors = 'coerce')
            
            new_df['prop_null%'].append("{:.2f}".format((1 - (col_serie.count() / df.shape[0])) * 100))
            try:
                new_df['start_date'].append(min(col_serie)._date_repr)
                new_df['end_date'].append(max(col_serie)._date_repr)
            except:
                new_df['start_date'].append('None')
                new_df['end_date'].append('None')

    return pd.DataFrame(new_df)

def get_categorical_cols(df):
    return [col for col in df.columns if is_string_dtype(df[col])]

def get_numerical_columns(df):
    return [col for col in df.columns if is_numeric_dtype(df[col])]

def daily_to_weekly(df, date_col, weekday, categorical_cols=None, output_starting=True, agg=None):
    """
     Convert a daily frequency DataFrame to a weekly frequency DataFrame by aggregating data.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing daily data.
    date_col (str): The name of the column containing date/time values.
    weekday (str): The target weekday for the weekly aggregation (e.g., 'MON', 'TUE', ...).
    categorical_cols (List[str], optional): List of column names to be included in grouping. Defaults to None.
    output_starting (bool, optional): If True, output the weekly DataFrame with dates aligned to the starting weekday. If False, align to ending weekday. Defaults to True.
    agg (Dict[str, str], optional): Custom aggregation methods for specific numerical columns. Keys are column names and values are aggregation functions. Defaults to None.

    Returns:
    pd.DataFrame: The resulting DataFrame with weekly aggregated data based on specified parameters.
    """

    new_df = df.copy(True)
    num_cols = get_numerical_columns(df)
    if categorical_cols is None:
        categorical_cols = []
    new_df = new_df[num_cols+[date_col]+categorical_cols]

    new_df[date_col] = pd.to_datetime(new_df[date_col])

    aggregation = {col: 'sum' for col in num_cols}

    if agg is not None:
        if not isinstance(agg, dict):
            raise ValueError('agg must be a dictionary!')
        elif not set(agg.keys()).issubset(set(aggregation.keys())):
            raise ValueError('Wrong keys for the agg variable')

        for key,val in agg.items():
            aggregation[key] = val
    
    days = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}
    day = days[weekday.upper()]

    if output_starting:
        new_df[date_col] = new_df[date_col].apply(lambda x: x - pd.to_timedelta(str(x.weekday())+' D') + pd.to_timedelta(str(day)+' D') if - x.weekday() + day <= 0 else x - pd.to_timedelta(str(x.weekday() + 7)+' D') + pd.to_timedelta(str(day)+' D'))
    else:
        new_df[date_col] = new_df[date_col].apply(lambda x: x - pd.to_timedelta(str(x.weekday() - 7)+' D') + pd.to_timedelta(str(day)+' D') if - x.weekday() + day < 0 else x - pd.to_timedelta(str(x.weekday())+' D') + pd.to_timedelta(str(day)+' D'))
    
    if categorical_cols is None:
        categorical_cols = []
    
    return new_df.groupby(by=categorical_cols+[date_col]).agg(aggregation).reset_index()

def daily_to_monthly(df, date_col, categorical_cols=None, agg=None):
    """
    Convert a daily frequency DataFrame to a monthly frequency DataFrame by aggregating data.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing daily data.
    date_col (str): The name of the column containing date/time values.
    categorical_cols (List[str], optional): List of column names to be included in grouping. Defaults to None.
    agg (Dict[str, str], optional): Custom aggregation methods for specific numerical columns. Keys are column names and values are aggregation functions. Defaults to None.

    Returns:
    pd.DataFrame: The resulting DataFrame with monthly aggregated data based on specified parameters.
    """

    new_df = df.copy(True)
    num_cols = get_numerical_columns(df)
    if categorical_cols is None:
        categorical_cols = []
    new_df = new_df[num_cols+[date_col]+categorical_cols]

    new_df[date_col] = pd.to_datetime(new_df[date_col])

    aggregation = {col: 'sum' for col in num_cols}

    if agg is not None:
        if not isinstance(agg, dict):
            raise ValueError('agg must be a dictionary!')
        elif not set(agg.keys()).issubset(set(aggregation.keys())):
            raise ValueError('Wrong keys for the agg variable')

        for key,val in agg.items():
            aggregation[key] = val

    new_df[date_col] = new_df[date_col].dt.to_period('M').dt.to_timestamp()

    if categorical_cols is None:
        categorical_cols = []

    return new_df.groupby(by=categorical_cols+[date_col]).agg(aggregation).reset_index()

def weekly_to_daily(df, date_col, categorical_cols=None, input_starting=True, agg=None):
    """
    Expand a DataFrame with weekly data into a daily granularity DataFrame.

    This function takes a DataFrame containing weekly data and converts it into a DataFrame with daily granularity.
    It replicates numerical values for each day within the week and repeats categorical values accordingly.
    Optionally, you can perform aggregation on numerical columns within each resulting group.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing weekly data.
    - date_col (str): The name of the column representing the date in the DataFrame.
    - categorical_cols (list, optional): List of column names to be treated as categorical variables.
    - input_starting (bool, optional): If True, assume the input data represents the starting date of each week.
                                        If False, assume the input data represents the ending date of each week.
    - agg (dict, optional): Dictionary specifying aggregation methods for numerical columns.
                           Keys are column names, and values are aggregation functions (e.g., 'sum', 'mean').

    Returns:
    - pd.DataFrame: A DataFrame with daily granularity, where numerical values are spread across the week
                    and categorical values are repeated for each day.

    Note:
    - If aggregation is specified, the returned DataFrame will be grouped by date and categorical columns,
      and the specified aggregation functions will be applied to the numerical columns within each group.

    Example:
    >>> weekly_data = pd.DataFrame({'date': ['2023-08-01', '2023-08-08'],
    ...                             'value': [70, 105]})
    >>> result = weekly_to_daily(weekly_data, 'date', ['category'], input_starting=True, agg={'value': 'sum'})
    >>> print(result)
         date   category  value
    0 2023-08-01     cat1    10
    1 2023-08-02     cat1    10
    2 2023-08-03     cat1    10
    ...   ...          ...    ...
    """

    new_df = df.copy(True)
    num_cols = get_numerical_columns(df)
    if categorical_cols is None:
        categorical_cols = []
    new_df = new_df[num_cols+[date_col]+categorical_cols]

    new_df[date_col] = pd.to_datetime(new_df[date_col])

    if input_starting:
        new_df[date_col] = new_df.apply(lambda x: pd.date_range(x[date_col], x[date_col] + pd.Timedelta(days=6)), axis = 1)
    else:
        new_df[date_col] = new_df.apply(lambda x: pd.date_range(x[date_col] - pd.Timedelta(days=6), x[date_col]), axis = 1)

    new_df = new_df.explode(date_col, ignore_index=True)

    new_df[num_cols] = new_df[num_cols] / 7
    
    aggregation = {col: 'sum' for col in num_cols}
    if agg is not None:
        for key,val in agg.items():
            aggregation[key] = val
    
    return new_df.groupby(categorical_cols+[date_col]).agg(aggregation).reset_index()

def monthly_to_daily(df, date_col, categorical_cols=None, agg=None):
    """
    Expand a DataFrame with monthly data into a daily granularity DataFrame.

    This function takes a DataFrame containing monthly data and converts it into a DataFrame with daily granularity.
    It replicates numerical values for each day within the month and repeats categorical values accordingly.
    Optionally, you can perform aggregation on numerical columns within each resulting group.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing monthly data.
    - date_col (str): The name of the column representing the date in the DataFrame.
    - categorical_cols (list, optional): List of column names to be treated as categorical variables. Defaults to None.
    - agg (dict, optional): Dictionary specifying aggregation methods for numerical columns.
                           Keys are column names, and values are aggregation functions (e.g., 'sum', 'mean'). Defaults to None.

    Returns:
    - pd.DataFrame: A DataFrame with daily granularity, where numerical values are spread across the month
                    and categorical values are repeated for each day.

    Note:
    - If aggregation is specified, the returned DataFrame will be grouped by date and categorical columns,
      and the specified aggregation functions will be applied to the numerical columns within each group.

    Example:
    >>> monthly_data = pd.DataFrame({'date': ['2023-08-01', '2023-09-01'],
    ...                              'value': [100, 150]})
    >>> result = monthly_to_daily(monthly_data, 'date', ['category'], agg={'value': 'sum'})
    >>> print(result)
            date  category  value
    0  2023-08-01     cat1    3.23
    1  2023-08-02     cat1    3.23
    2  2023-08-03     cat1    3.23
    ...   ...          ...    ...
    """

    new_df = df.copy(True)
    num_cols = get_numerical_columns(df)
    if categorical_cols is None:
        categorical_cols = []
    new_df = new_df[num_cols+[date_col]+categorical_cols]

    new_df[date_col] = pd.to_datetime(new_df[date_col])
    
    new_df[date_col] = new_df.apply(lambda x: pd.date_range(x[date_col] - pd.Timedelta(days=x[date_col].day - 1), x[date_col] - pd.Timedelta(days=x[date_col].day - 1) + pd.offsets.MonthEnd()), axis=1)
    new_df['nb_days'] = new_df.apply(lambda x: len(x[date_col]), axis=1)
    new_df = new_df.explode(date_col, ignore_index=True)
    
    for col in num_cols:
        new_df[col] = new_df[col] / new_df['nb_days']

    aggregation = {col: 'sum' for col in num_cols}
    if agg is not None:
        for key,val in agg.items():
            aggregation[key] = val
    
    return new_df.groupby(categorical_cols+[date_col]).agg(aggregation).reset_index()

def change_periodicity(df, date_col, output_freq, categorical_cols=None, input_starting=True, output_starting=True, agg=None):
    """
    Adjusts the periodicity of a time series DataFrame to the desired output frequency.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame containing time series data.
    date_col : str
        The name of the column in 'df' that contains the date or timestamp values.
    output_freq : str
        The desired output frequency for the time series data. 
        Valid values are 'D' (daily), 'W' (weekly), or 'M' (monthly).
    categorical_cols : list of str, optional
        A list of column names to be treated as categorical variables.
    input_starting : bool, optional
        Indicates whether the input data starts at the beginning or end of the period.
        Default is True, meaning the input data starts at the beginning of each period.
    output_starting : bool, optional
        Indicates whether the output data should start at the beginning or end of the period.
        Default is True, meaning the output data starts at the beginning of each period.
    agg : callable, optional
        A function to aggregate data when reducing frequency.
        For example, 'np.mean' or 'np.sum'. Default is None, meaning no aggregation.

    Returns:
    -------
    pandas.DataFrame
        A DataFrame with the adjusted periodicity according to the specified 'output_freq'.

    Raises:
    -------
    Exception
        If the 'periodicity' of the input DataFrame is neither 'D' (daily), 'W' (weekly), nor 'M' (monthly).

    Example:
    --------
    # Convert daily data to weekly data
    weekly_df = change_periodicity(daily_df, 'date_column', 'W')
    """

    periodicity = get_periodicity(df, date_col)[date_col]
    if periodicity == 'D':
        if output_freq.upper() in ['D', 'DAILY']:
            return df
        elif output_freq.upper()[0] == 'W':
            return daily_to_weekly(df, date_col, output_freq.upper()[2:], categorical_cols, output_starting, agg)
        elif output_freq.upper() in ['M', 'MONTHLY']:
            return daily_to_monthly(df, date_col, categorical_cols, agg)
    elif periodicity[0] == 'W':
        if output_freq.upper() in ['D', 'DAILY']:
            return weekly_to_daily(df, date_col, categorical_cols, input_starting, agg)
        elif output_freq.upper()[0] == 'W':
            new_df = weekly_to_daily(df, date_col, categorical_cols, input_starting, agg)
            return daily_to_weekly(new_df, date_col, output_freq[2:], categorical_cols, output_starting, agg)
        elif output_freq.upper() in ['M', 'MONTHLY']:
            new_df = weekly_to_daily(df, date_col, categorical_cols, input_starting, agg)
            return  daily_to_monthly(new_df, date_col, categorical_cols, agg)
    elif periodicity == 'M':
        if output_freq.upper() in ['D', 'DAILY']:
            monthly_to_daily(df, date_col, categorical_cols, agg)
        elif output_freq.upper()[0] == 'W':
            new_df = monthly_to_daily(df, date_col, categorical_cols, agg)
            return daily_to_weekly(new_df, date_col, output_freq[2:], categorical_cols, output_starting, agg)
        elif output_freq.upper() in ['M', 'MONTHLY']:
            return df
    else:
        raise Exception('Periodicity is neither daily, weekly, nor monthly.')

def today():
    print("today")