from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go

import pandas as pd

import json
import requests
app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def index():
    result = ''
    input = ''
    cat = ''
    if request.method == 'POST':
        input = request.form.get('input')
        cat = request.form.get('category')
        

        data={
            "body":input
        }
        response = requests.post("https://nlptraining.herokuapp.com" + '/' + cat,json=data)
        if response.status_code == 200:
            if 'most_similar_items' in response.json():
                result = response.json()['most_similar_items']
            else:
                result = response.json()['category_predicted']
        print("----------------------",result)
    return render_template('index.html',result=result,text=input,category=cat)

# def create_plot(feature):
#     if feature == 'Bar':
#         N = 40
#         x = np.linspace(0, 1, N)
#         y = np.random.randn(N)
#         df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
#         data = [
#             go.Bar(
#                 x=df['x'], # assign x as the dataframe column 'x'
#                 y=df['y']
#             )
#         ]
#     else:
#         N = 1000
#         random_x = np.random.randn(N)
#         random_y = np.random.randn(N)

#         # Create a trace
#         data = [go.Scatter(
#             x = random_x,
#             y = random_y,
#             mode = 'markers'
#         )]


#     graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

#     return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON= create_plot(feature)




    return graphJSON

if __name__ == '__main__':
    app.run()
