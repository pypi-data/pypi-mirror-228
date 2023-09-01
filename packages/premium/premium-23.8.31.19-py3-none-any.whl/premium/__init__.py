from .metrics.metrix import Printer, prmetric

def lds(repo_name:str):
    # datasets.load_dataset shortcut
    from datasets import load_dataset
    return load_dataset(repo_name)

def ttsplit_df(df, *args, **kwargs):
    # dataframe train test split
    from sklearn.model_selection import train_test_split
    return train_test_split(df, *args, **kwargs)

def ttsplit(X,y, *args, **kwargs):
    from sklearn.model_selection import train_test_split
    return train_test_split(X,y, *args, **kwargs)