import pandas as pd
def load_df():
    df = pd.read_json('static/camping_sites_flat.json')
    return df

def get_df():
    try:
        df
    except NameError:
        df = load_df()
    return df


# remove empty comlumns or solumns with only 1 unique value
def skip_irrelevant_col(all_columns):
    df = get_df()
    skip_columns = []
    for column in all_columns:
        duplicates = df.duplicated(subset=[column]).sum()
        number_of_rows = len(df) - 1  # subtract 1 because first occurrance doesn't count as a duplicate
        if duplicates == number_of_rows:
            skip_columns.append(column)
    return skip_columns


# ignore the amenity features if skip_irrelevant is set to True
def ignore_amenities(all_columns):
    skip_columns = []
    amenity_features = [column for column in all_columns if 'description.amenityFeature.' in column]
    for elem in amenity_features:
        skip_columns.append(elem)
    # not skipping total amenitites
    skip_columns.remove('description.amenityFeature.total')
    return skip_columns


# ignore prices without ignoring relevant columns
def ignore_price(all_columns):
    keep = ['price.categories', 'price.max', 'price.median', 'price.min']
    skip_column = [column for column in all_columns if 'price.' in column if column not in keep]
    return skip_column


# return data frame
def return_df(return_columns):
    new_df = df[return_columns].copy()
    return new_df


def get_columns(category, skip_irrelevant=True, return_df=False):
    # exit function if a wrong category is entered.
    if category not in ['description', 'price', 'tax', 'all']:
        raise Exception('Category not valid. Please use description, price, tax or all.')

    # Variables required for function to work
    skip_columns = []
    df = get_df()
    all_columns = df.columns.values.tolist()
    return_columns = []

    # set correct
    if skip_irrelevant == True:
        skip_columns = skip_irrelevant_col(all_columns)
        if category == 'description':
            skip_columns = skip_columns + ignore_amenities(all_columns)
        elif category == 'price':
            skip_columns = skip_columns + ignore_price(all_columns)
        elif category == 'all':
            skip_columns = skip_columns + ignore_amenities(all_columns) + ignore_price(all_columns)

    # add columns to return columns if they should not be skipped
    if category == 'all':
        return_columns = [column for column in all_columns if column not in skip_columns]
    else:
        return_columns = [column for column in all_columns if category + '.' in column if column not in skip_columns]

    if return_df == True:
        return return_df(return_columns)
    elif return_df == False:

        return return_columns

