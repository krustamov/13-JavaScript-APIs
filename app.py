

from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DOUBLE
import pandas as pd
from warnings import filterwarnings
#import pymysql
import sqlite3

#filterwarnings('ignore', category=sqlite3.Warning)
import os
import json
 
import numpy as np
from flask import (
    Flask,
    render_template,
    jsonify,
    request)


# My routine to conceal root passwords
pass_file_name = "C:\PSW\psw.json"
data = json.load(open(pass_file_name))
bbSamples_csv = os.path.join("data", "belly_button_biodiversity_samples.csv")
bbSamples_df = pd.read_csv(bbSamples_csv, dtype=object)

bbOtu_csv = os.path.join('data', 'belly_button_biodiversity_otu_id.csv')
bbOtu_df = pd.read_csv(bbOtu_csv, dtype=object)

spassword = data['password']

#using sqlalchemy engine
seng = 'sqlite:///database.sqlite'

engine=create_engine(seng)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################

#from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite"
db = SQLAlchemy(app)

#################################################
# Routes
#################################################

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/names")
#this route is a test route
def names():
    print("Server received request for 'names data' page...")
    #return the list of sample names
    return_value = []
    for value in bbSamples_df.columns:
        if value != 'otu_id':
            return_value.append(value)
    return jsonify(return_value)

@app.route("/otu")
#this route is a test route
def otu():
    print("Server received request for 'otu data' page...")
    #return the list of sample names
    #fname = 'clean_bellybuttondata'
    #new_df = pd.read_sql_query('select [lowest_taxonomic_unit_found] from '+fname, engine)
    
    #retData = pd.DataFrame.to_json(new_df)
    #retData = new_df.to_json(orient='values')
    return_value = []
    for value in bbOtu_df['lowest_taxonomic_unit_found']:
        return_value.append(value)
    return jsonify(return_value)

# David Rinck [8:16 PM]
# my_list = []
#    my_obj = {"otu_ids" : [116,34,53], "sample_values: [123,451,12]"}
#    #my_obj['otu_ids'].append(45)
#    my_list.append(my_obj)



@app.route("/metadata/<sample>", methods=['GET'])
# the above route takes the table name and delivers the entire table in json
def metadata(sample):
    print("Server received request for metadata for " + sample)
    sampleID = sample
    fname = 'clean_bbMetadata'
    new_df = pd.read_sql_query('select [AGE],[BBTYPE], [ETHNICITY], [GENDER],[LOCATION],[SAMPLEID]  from '+fname + ' where [sampleid] = ' + sampleID, engine)
    return json.dumps(new_df.iloc[0,:].to_dict())

@app.route("/wfreq/<sample>", methods=['GET'])
# the above route takes the table name and delivers the entire table in json
def wfreq(sample):
    print("Server received request for wash frequency for  " + sample)
    sampleID = sample
    fname = 'clean_bbMetadata'
    new_df = pd.read_sql_query('select [WFREQ]  from '+fname + ' where [sampleid] = ' + sampleID, engine)   
    #retData = pd.DataFrame.to_json(new_df)
    retData2 = new_df.iloc[0,:]

    return (jsonify(int(retData2['WFREQ'])))

@app.route("/samples/<sample>", methods=['GET'])
# the above route takes the table name and delivers the entire table in json
def samples(sample):
    print("Server received request for samples for  " + sample)
    sampleID = 'BB_'+ sample
    
    fname = 'clean_bbSamples'
    new_df = pd.read_sql_query('select [otu_id], [' + sampleID + '] from '+fname+  ' order by  ['+sampleID+'] DESC' , engine)
    #retData = pd.DataFrame.to_json(new_df)
    #print(new_df.columns)
    #print(new_df['otu_id'])
    retValue = { "otu_ids" : [], "sample_values" : []}

    #new_df.head()
    #new_df['otu_id'].head()

    for value in new_df['otu_id']:
        retValue['otu_ids'].append(int(value))

    for value in new_df[sampleID]:
        if not np.isnan(value):
            retValue['sample_values'].append(int(value))
            
    #for row in new_df.iterrows():
    #    print(row)


    #retValue
    return (jsonify(retValue))

if __name__ == '__main__':
    app.run(debug=True)