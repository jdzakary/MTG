import sqlite3
import pandas as pd


def find_new(df, table_name, engine, dup_cols, filter_continuous_col=None, filter_categorical_col=None):
    args = 'select {0} from {1}'.format(', '.join(['"{0}"'.format(col) for col in dup_cols]), table_name)
    args_filter, args_cat_filter = None, None
    if filter_continuous_col is not None:
        if df[filter_continuous_col].dtype == 'datetime64[ns]':
            args_filter = """ "%s" BETWEEN Convert(datetime, '%s') AND Convert(datetime, '%s')""" % (filter_continuous_col, df[filter_continuous_col].min(), df[filter_continuous_col].max())
    if filter_categorical_col is not None:
        args_cat_filter = ' "%s" in(%s)' % (filter_categorical_col, ', '.join(["'{0}'".format(value) for value in df[filter_categorical_col].unique()]))
    if args_filter and args_cat_filter:
        args += ' Where ' + args_filter + ' AND' + args_cat_filter
    elif args_filter:
        args += ' Where ' + args_filter
    elif args_cat_filter:
        args += ' Where ' + args_cat_filter
    df.drop_duplicates(dup_cols, keep='last', inplace=True)
    df = pd.merge(df, pd.read_sql(args, engine), how='left', on=dup_cols, indicator=True)
    df = df[df['_merge'] == 'left_only']
    df.drop(['_merge'], axis=1, inplace=True)
    return df


def data_insert(path_prefix: str):
    default = pd.read_csv(f'{path_prefix}default.csv')
    oracle = pd.read_csv(f'{path_prefix}oracle.csv')
    connection = sqlite3.connect(f'{path_prefix}main_database.db')

    new_default = find_new(oracle, 'oracle_entries', connection, ['oracle_id'])
    print(len(new_default))
    new_default.to_sql('oracle_entries', connection, if_exists='append', index=False)

    new_default = find_new(default, 'all_entries', connection, ['scryfall_uri'])
    print(len(new_default))
    new_default.to_sql('all_entries', connection, if_exists='append', index=False)
