from flask import Flask
from flask_restful import Resource, Api
import pickle
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
#creating an api object
api = Api(app)

#predict api call
class predict(Resource):
    def get(self, vol_moving_avg, adj_close_rolling_med):
        vol_moving_avg = float(vol_moving_avg)
        adj_close_rolling_med = float(adj_close_rolling_med)
        dict = {'vol_moving_avg':vol_moving_avg, 'adj_close_rolling_med':adj_close_rolling_med}
        df = pd.DataFrame([dict])
        model = pickle.load(open('randomforest_model_stock_volume_prediction.sav', 'rb'))
        predict = model.predict(df)
        predict= float(predict[0])
        return (predict)

api.add_resource(predict, '/predict/<float:vol_moving_avg>/<float:adj_close_rolling_med>')



if __name__=='__main__':
    app.run(debug =True)
