"""A set of general tools for use in working with data"""

import os
from pathlib import Path
import contextlib
from urllib.parse import urlparse
from git import Repo
from git.exc import NoSuchPathError
import numpy as np
import pandas as pd
from dataforge import config

@contextlib.contextmanager
def versioned_file_resource(filename, remote_url=None, repo_path=None, mode='r',
                            empty_ok=False, verbose=False):
    """Open versioned file and return corresponding file object
    
    Regular file object returned if remote_url and repo_path not specified.
    """
    _echo = print if verbose else lambda *a, **k: None
    repo = None
    if remote_url or repo_path:
        
        if not repo_path:
            repo_name = os.path.basename(urlparse(remote_url).path)
            repo_path = Path(os.path.join('tmp/git', repo_name)).with_suffix('')
        
        try:
            repo = Repo(repo_path)
            if remote_url:
                assert repo.remotes.origin.url == remote_url
            assert not repo.is_dirty(untracked_files=True)
            if repo.references:
                repo.remotes.origin.pull()
                _echo(f'Pulled latest changes from {remote_url} into {repo_path}')
            else:
                # Pulling into an empty repo yields git error
                _echo(f'Pull skipped because local repository {repo_path} is empty')
        except NoSuchPathError:
            repo = Repo.clone_from(remote_url, repo_path)
            _echo(f'Cloned {remote_url} into {repo_path}')
    
    file_path = os.path.join(repo_path, file) if repo_path else file
    # Use newline='' to disable universal newline support
    file_obj = open(file_path, mode, newline='')
    
    if not repo_path:
        print(f'WARNING: File {file_path} not under version control')
    
    try:
        yield file_obj
    
    except Exception as e:
        if repo:
            file_obj.close()
            repo.git.reset('--hard')
        raise e
    
    finally:
        file_obj.close()
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else None
        
        # Don't store empty file
        if not file_size and not empty_ok:
            with contextlib.suppress(FileNotFoundError):
                os.remove(file_path)
        
        if repo and repo.is_dirty(untracked_files=True):
            repo.git.add('--all')
            repo.index.commit('Commit by versioned_file_resource()')
            _echo(f'Changes to {file_path} committed to local repository {repo_path}')
            try:
                repo.remotes.origin.push()
                _echo(f'Changes pushed to remote {remote_url}')
            except Exception as e:
                repo.git.reset('--hard')
                repo.head.reset('HEAD~1', index=True, working_tree=True)
                raise e

def shift_dates(df, shift, date_cols=None, merge_on=None):
    """Shift dates around an index date or by an offset (in days)
    
    If shift is a date, then resulting columns will be integers representing
    the number of days from the index; if shift is an offset, then resulting
    columns will be dates. By default all date columns in data frame are
    shifted; this can be limited by use of date_cols.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Data frame containing date columns to be shifted
    shift : pandas.Series
        Series of type datetime64 or int
    date_cols : str or list of str, optional
        Name(s) of date column(s) to be shifted
    merge_on : str or list of str, optional
        Name(s) of column(s) and/or index levels containing key(s) for merging
        shift onto df; if None then df and shift must have the same index
    
    Returns
    -------
    pandas.DataFrame
        Data frame with shifted dates
    """
    
    # +/- operations below will likely yield undesired/unexpected results in
    # the presence of a non-unique index
    assert df.index.is_unique
    cols = df.columns.tolist()
    if merge_on:
        new_df = df.merge(shift, how='left', on=merge_on,
                          validate='many_to_one')
    else:
        new_df = df.merge(shift, how='left', left_index=True,
                          right_index=True, validate='many_to_one')
    shift_col = new_df.iloc[:,-1]
    
    if date_cols:
        date_cols = [date_cols] if isinstance(date_cols, str) else date_cols
    else:
        date_cols = [c for c, is_type in (new_df.dtypes=='datetime64[ns]').items()
                     if is_type]
    
    if shift_col.dtype=='datetime64[ns]':
        for col in date_cols:
            new_df[col] = (new_df[col] - shift_col).dt.days
    else:
        shift_col = pd.to_timedelta(shift_col, unit='days')
        for col in date_cols:
            new_df[col] = new_df[col] + shift_col
    
    return new_df[cols]

def date_offset(key, offset_file, offset_url=None, min_days=-182, max_days=183,
                seed=None, name='_offset'):
    """Generate and store random offset (in days) for use in shifting dates
    
    Parameters
    ----------
    key : pandas.Series or pandas.DataFrame
        One or more columns uniquely identifying entities for which offsets
        are to be generated; duplicates will be removed
    offset_file : str
        Name of file in which offsets are stored for future use
    offset_url : str, optional
        URL of bare git repository containing offset generation history
    min_days : int, default -182
        Minimum possible shift (in days)
    max_days : int, default 183
        Maximum possible shift (in days)
    seed : int, array_like[ints], SeedSequence, BitGenerator, Generator, optional
        A seed to initialize the BitGenerator
    name : str, default '_offset'
        Name of column in offset_file containing offsets
    
    Returns
    -------
    pandas.Series
        Series containing offsets with key as index
    """
    
    if not offset_url:
        offset_url = config['offset_url'].get(str)
    
    key = pd.DataFrame(key).drop_duplicates(ignore_index=True).dropna()
    rng = np.random.default_rng(seed=seed)
    
    with versioned_file_resource(offset_file, offset_url, mode='a+') as f:
        
        f.seek(0)
        try:
            offsets = pd.read_csv(f)
            add_header = False
        except pd.errors.EmptyDataError:
            offsets = pd.DataFrame(columns = key.columns.values.tolist() + [name])
            add_header = True
        
        offsets = (key
                   .merge(offsets, how='left', on=key.columns.values.tolist(),
                          validate='one_to_one', indicator=True)
                   .sort_values(by=key.columns.values.tolist())
                   .astype({name:'Int64'})
                   .pipe(lambda df: df.fillna(
                       pd.DataFrame(rng.integers(low=min_days, high=max_days+1,
                                                 size=len(df)), columns=[name])))
                  )
        
        if (offsets._merge=='left_only').any():
            (offsets.loc[offsets._merge=='left_only', offsets.columns!='_merge']
             .to_csv(f, index=False, header=add_header))
        
        return offsets.iloc[:,:-1].set_index(key.columns.values.tolist(),
                                             verify_integrity=True).squeeze()
