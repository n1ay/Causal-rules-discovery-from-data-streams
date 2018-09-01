from sklearn.model_selection import KFold

def kfold_data(df, folds:int=10):

    #no shuffle is a must - shuffling timeseries without timestamps is not what we want
    kf = KFold(n_splits=folds, shuffle=False)
    kf.get_n_splits(df)

    X_train, X_test = [], []
    for train_index, test_index in kf.split(df):
        X_train.append(df.iloc[train_index])
        X_test.append(df.iloc[test_index])

    return X_train, X_test