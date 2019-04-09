def summarize_data(df):
    
    head_df = df.head()
    print(f'HEAD\n{head_df}', end='\n\n')
   
    tail_df = df.tail()
    print(f'TAIL\n{tail_df}', end='\n\n')

    shape_tuple = df.shape
    print(f'SHAPE: {shape_tuple}', end='\n\n')
    
    describe_df = df.describe()
    print(f'DESCRIPTION\n{describe_df}', end='\n\n')
    
    df.info()
    print(f'INFORMATION')
    

    print(f'VALUE COUNTS', end='\n\n')
    for col in df.columns:
        n = df[col].unique().shape[0]
        col_bins = min(n, 10)
        print(f'{col}:')
        if df[col].dtype in ['int64', 'float64'] and n > 10:
            print(df[col].value_counts(bins=col_bins, sort=False, dropna=False))
        else:
            print(df[col].value_counts(dropna=False))
        print('\n')