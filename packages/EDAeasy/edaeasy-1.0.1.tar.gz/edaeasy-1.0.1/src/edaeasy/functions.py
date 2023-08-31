import pandas as pd

def dataframe_summary(dataframe: pd.DataFrame):
    """Generate a summary DataFrame of the input DataFrame 'dataframe'.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The input DataFrame for which the summary needs to be generated.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing summary information for each column in 'df':
        - Type: Data type of the column.
        - Min: Minimum value in the column.
        - Max: Maximum value in the column.
        - Nan %: Percentage of NaN values in the column.
        - # Unique Values: Total number of unique values in the column.
        - Unique values: List of unique values in the column.

    Example
    -------
    >>> data = {
            'age': ['[40-50)', '[60-70)', '[70-80)'],
            'time_in_hospital': [8, 3, 5],
            'n_lab_procedures': [72, 34, 45],
            ...
        }
    >>> dataframe = pd.DataFrame(data)
    >>> result = dataframe_summary(df)
    >>> print(result)
               Type       Min        Max  Nan %  # Unique Values                                  Unique values
    Variables                                                                                                              
    age       object   [40-50)    [90-100)    0.0        3      ['[70-80)', '[50-60)', '[60-70)', '[40-50)', '[80-90)', ...
    time_in_hospital  int64    1           14    0.0        3        [8, 3, 5]
    n_lab_procedures  int64    1          113    0.0        3        [72, 34, 45]
    ...

    Note
    ----
    The function uses vectorized operations to improve performance and memory usage.
    """
    ret = pd.DataFrame(columns=['Type', 'Min', 'Max', 'Nan %', '# Unique Values', 'Unique values'])

    for col, content in dataframe.items():
        values = []
        dtype = content.dtype

        # Convert 'object' columns to appropriate data types
        if dtype == 'object':
            if col in ['Min', 'Max', 'Type']:
                # Clean and convert 'Min', 'Max', and 'Type' columns to strings
                content = content.astype(str)

        values.append(content.dtype)  # Data type after conversion

        try:
            values.append(content.min())  # Min
            values.append(content.max())  # Max
        except Exception:
            values.append('None')
            values.append('None')

        values.append(content.isnull().mean() * 100)  # % of NaN's
        # Calculate the number of unique values in the column
        num_unique_values = len(content.drop_duplicates())
        values.append(num_unique_values)  # Number of unique values
        # Handle the 'Unique values' column as a list of strings
        unique_values = content.drop_duplicates().astype(str).tolist()
        unique_values.sort()
        values.append(unique_values)
        ret.loc[col] = values

    ret.index.names = ['Variables']
    rows = dataframe.shape[0]
    columns = dataframe.shape[1]
    return ret, (rows, columns)