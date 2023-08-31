import pandas as pd
import numpy as np


def metodo_pivote(df, ix_multicol, last_index_col):
    '''
    df: dataframe a pivotear (Al leerlo header=None)
    ix_multicol: lista con el index de las filas a transformar
    last_index_col: Cantidad de columnas antes de realizar el melt
    '''
    aux =  np.array([df.loc[ix, :].values for ix in ix_multicol]).T
    aux = [';'.join([str(x) for x in item]) for item in aux]
    df.columns = aux
    df = df.drop(ix_multicol, axis=0)

    df = pd.melt(df, id_vars=df.columns[:last_index_col], value_vars=df.columns[last_index_col:], var_name='aux_var', value_name='aux_value')

    for ix in range( len(ix_multicol) ):
        df.insert(loc=last_index_col+ix, column='var_' + str(ix), value=df['aux_var'].apply(lambda x: x.split(';')[ix]))
    df = df.drop(columns=['aux_var'])

    return df
