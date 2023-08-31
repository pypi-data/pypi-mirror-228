import pandas as pd
from copy import deepcopy
from intent_inference import apply_prediction
from persist_ext.extension.utils import between_pd_datetime_parts, get_time_unit_parts, compare_pd_datetime_parts
from sklearn.utils._testing import ignore_warnings

SELECTED = "__selected"

INTENT_SELECTED = "__intent_selected"

INVERT_SELECTED = "__invert_selected"

def apply_intent_selection(df, intent, row_id_label):
    with ignore_warnings():
        dimensions = deepcopy(intent["dimensions"])
        dimensions.append(row_id_label)
        newPredObj = apply_prediction(df[dimensions].dropna(), intent, row_id_label) 
    print(intent, dimensions)
    print(len(newPredObj["ids"]))
    df[SELECTED] = False
    df[INTENT_SELECTED] = False

    df[INTENT_SELECTED]  = df[row_id_label].isin(newPredObj["ids"])
    return df;

def apply_invert(df):
    if SELECTED not in df:
        df[SELECTED] = False

    df[INVERT_SELECTED] = ~df[SELECTED]

    df[SELECTED] = False

    return df

def apply_sort(df, interaction):
    direction = interaction["direction"]
    col = interaction["col"]

    df = df.copy()
    df = df.sort_values(col, ascending=(direction == 'ascending'))

    return df

def apply_reorder(df, interaction):
    newcols = interaction["value"]
    currCols = df.columns.tolist()

    df = df.copy()

    df = df[filter(lambda x: x in currCols, newcols)]

    return df

def apply_selection(df, interaction):
    new_df = df

    selection_type = interaction["select"]["type"]
    name = interaction['name']

    selected = interaction["selected"]


    if not selected:
        new_df[name] = False
    if selection_type == 'point':
        new_df = apply_point_selection(df, selected, name)
    elif selection_type == 'interval':
        new_df = apply_interval_selection(df,  selected, name)
    else:
        print("########", interaction)
    return new_df


# Point selections are always arrays
def apply_point_selection(df, selected, name):
    """
         All selections are maps between field names and initial values
         
         POINT SELECTIONS
         Array of such mappings e.g:
         [
           {"Cylinders": 4, "Year": 1981},
           {"Cylinders": 8, "Year": 1972}
         ]
    """
    df[name] = False # Start with everything selected
    value = selected["value"]
    encoding_types = selected["encodingTypes"]


    for sel_val in value: # each selected "POINT" is represented by a mapping
        existing = df[name] | True  # get selected points for one set of mapping; initially everything is selected

        for k,v in sel_val.items(): # get col_name, value for each entry in mapping
            timeunits = []

            if k not in df:
                if "_" not in k:
                    print("Something went wrong")
                    break
                k_parts = k.split("_")
                k = "_".join(k_parts[1:])
                timeunits = get_time_unit_parts(k_parts[0])
            
            is_column_datetime = True if k in encoding_types and "timeUnit" in encoding_types[k] else False

            if is_column_datetime:
                newMask = df[k].apply(lambda x: compare_pd_datetime_parts(x, v, timeunits)) # get mask for each entry in the mapping
            else:
                newMask = df[k] == v

            existing = existing & newMask # update by ANDing with existing mapping

        df[name] = df[name] | existing # update the dataframe by ORing with existing

    return df # return with added [name] column


def apply_interval_selection(df, selection, name):
    """
         INTERVAL SELECTIONS
         Single object with field names and value array. e.g:

         {"x": [55, 160], "y": [13, 37]}
    """

    df[name] = True # Start with all selected

    value = selection["value"]
    encoding_types = selection["encodingTypes"]

    for sel_key, _range in value.items(): # iterate over individual key-val pair
        timeunits = []
        if sel_key not in df:
            if "_" not in sel_key:
                print("Something went wrong")
                break
            k_parts = sel_key.split("_")
            sel_key = "_".join(k_parts[1:])
            timeunits = get_time_unit_parts(k_parts[0])

        is_column_datetime = True if sel_key in encoding_types and "timeUnit" in encoding_types[sel_key] else False

        existing = df[name] # get exising mask for 'name'

        if len(_range) == 2 and is_number(_range[0]) and is_number(_range[1]): # if the range is 2-long and numeric use between
            if is_column_datetime:
                _range = list(map(lambda x: pd.Timestamp(x, unit="ms"), _range))
                newMask = df[sel_key].apply(lambda x: between_pd_datetime_parts(_range[0], _range[1], x, timeunits))
            else:
                newMask = df[sel_key].between(_range[0], _range[1])  # get mask between range

            df[name] = existing & newMask # and both masks
        else: # for more than 2-long use any of
            if is_column_datetime:
                _range = list(map(lambda x: pd.Timestamp(x, unit="ms"), _range))
                newMask = df[sel_key].apply(lambda x: any([compare_pd_datetime_parts(x, k, timeunits) for k in _range]))
            else:
                newMask = df[sel_key].apply(lambda x: x in _range) # check if each value in the row in included in the range

            df[name] = existing & newMask # and both masks
    return df

def is_number(val):
    return isinstance(val, (int, float))
