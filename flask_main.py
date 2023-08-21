# import python libraries
from flask import Flask, render_template
from pandas.api.types import is_numeric_dtype

# import code from .py files
from data import get_df, get_columns
from plot_geo import plot_geo

app = Flask(__name__)

# load Data Frame with the data
df = get_df()

@app.route('/')
def landing_page():
    return render_template('main.html')

@app.route('/corr')
def correlation_page():
    # Data as JSON for output on page
    dfJSON = df.to_json(orient='columns')

    # get numeric columns
    columns = []
    for column in get_columns(category='all'):
        if is_numeric_dtype(df[column]):
            columns.append(column)

    return render_template('corr.html', title="Correlations", content='hello world!', dfJSON=dfJSON, columns=columns)

@app.route('/sites')
def sites_page():
    # Data as JSON for output on page
    dfJSON = df.to_json(orient='index')

    # Load graph from file
    graphJSON = plot_geo(df)
    return render_template('sites.html', title="Camping Sites", graphJSON=graphJSON, dfJSON=dfJSON)

@app.route('/histograms')
def histograms_page():
    # Data as JSON for output on page
    df_histograms = df.fillna(0)
    dfJSON = df_histograms.to_json(orient='columns')

    columns = [column for column in get_columns(category='all')]
    columns.remove('description.amenities')
    columns_hist = []
    for column in columns:
        if is_numeric_dtype(df[column]):
            columns_hist.append(column)
        elif len(df[column].unique()) < 40:
            columns_hist.append(column)

    return render_template('histograms.html', title="Camping Sites", dfJSON=dfJSON, columns = columns_hist)

if __name__ == '__main__':
    app.run(debug=True)