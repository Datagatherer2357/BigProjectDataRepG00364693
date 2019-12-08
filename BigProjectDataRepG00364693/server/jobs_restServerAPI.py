#!flask/bin/python
# e.g. copy the localhost when server running , and paste into url: http://127.0.0.1:5000/jobs
# car = job, cars = jobs

from flask import Flask, jsonify,  request, abort, make_response
from flask_cors import CORS

app = Flask(__name__,
            static_url_path='', 
            static_folder='../')

@app.route('/') # appserver route
def index():
    return "Hello there, the jobs app server is running..."

CORS(app) # Initiate CORS for delete functionality

# missing variable to be added: "company":"Microsoft",
jobs = [
    {   "jobID":"001",
        "location":"Dublin",
        "jobTitle":"Data Analyst",
        "company":"Microsoft",
        "salary":38000
    },
    {
        "jobID":"002",
        "location":"Cork",
        "jobTitle":"Software Developer",
        "company":"Oracle",
        "salary":60000
    },
    {
        "jobID":"003",
        "location":"Dublin",
        "jobTitle":"Compliance Analyst",
        "company":"Paddy Power",
        "salary":55000
    },
    {
        "jobID":"004",
        "location":"Galway",
        "jobTitle":"Data Scientist",
        "company":"Salesforce",
        "salary":65000
    },
    {
        "jobID":"005",
        "location":"Cork",
        "jobTitle":"Cloud Architect",
        "company":"Adobe",
        "salary":49000
    },
    {
        "jobID":"006",
        "location":"Dublin",
        "jobTitle":"Java Developer",
        "company":"AirBnB",
        "salary":58000
    },
]

@app.route('/jobs', methods=['GET'])
def get_jobs():
    return jsonify( {'jobs':jobs})
# curl -i http://localhost:5000/jobs # SAMPLE CURL SCRIPTS

@app.route('/jobs/<string:jobID>', methods =['GET'])
def get_job(jobID):
    foundJobs = list(filter(lambda t : t['jobID'] == jobID , jobs))
    if len(foundJobs) == 0:
        return jsonify( { 'job' : '' }),204
    return jsonify( { 'job' : foundJobs[0] })

# curl -i http://localhost:5000/jobs/test

@app.route('/jobs', methods=['POST'])
def create_job():
    if not request.json:
        abort(400)
    if not 'jobID' in request.json:
        abort(400)
    job={
        "jobID":  request.json['jobID'],
        "location":request.json['location'],
        "jobTitle":  request.json['jobTitle'],
        "company": request.json['company'],
        "salary":request.json['salary']
    }
    jobs.append(job) # add created job to jobs table
    return jsonify( {'job':job }),201

# sample test TEST CREATE:
# curl -i -H "Content-Type:application/json" -X POST -d '{"JobID":"004","JobTitle": "Data Engineer", "Company":"Infosys","Location":"Galway","Salary":65000}' http://localhost:5000/jobs
# for windows use this one
# curl -i -H "Content-Type:application/json" -X POST -d "{\"jobID\":\"004\",\"jobTitle\":\"Data Engineer\", \"company\":\"Infosys\",\"location\":\"Galway\",\"salary\":65000}" http://localhost:5000/jobs
@app.route('/jobs/<string:jobID>', methods =['PUT'])
def update_job(jobID):
    foundJobs=list(filter(lambda t : t['jobID'] ==jobID, jobs))
    if len(foundJobs) == 0:
        abort(404)
    if not request.json:
        abort(400)

    if 'location' in request.json and type(request.json['location']) is not str:
        abort(400)
    if 'jobTitle' in request.json and type(request.json['jobTitle']) != str:
        abort(400)
    if 'company' in request.json and type(request.json['company']) != str:
        abort(400)
   
    if 'salary' in request.json and type(request.json['salary']) is not int:
        abort(400)
    foundJobs[0]['location'] =request.json.get('location', foundJobs[0]['location'])
    foundJobs[0]['jobTitle']  = request.json.get('jobTitle', foundJobs[0]['jobTitle'])
    foundJobs[0]['company']  = request.json.get('company', foundJobs[0]['company'])
   
    foundJobs[0]['salary'] =request.json.get('salary', foundJobs[0]['salary'])
    return jsonify( {'job':foundJobs[0]})
#curl -i -H "Content-Type:application/json" -X PUT -d '{"company":"Google"}' http://localhost:5000/jobs/181%20G%201234
# for windows use this one
#curl -i -H "Content-Type:application/json" -X PUT -d "{\"company\":\"Google\"}" http://localhost:5000/jobs/181%20G%201234


# Delete needs to be tried and tested and probably CORS:
# curl -X DELETE "http://127.0.0.1:5000/jobs/001"

@app.route('/jobs/<string:jobID>', methods =['DELETE'])
def delete_job(jobID):
    foundJobs = list(filter (lambda t : t['jobID'] == jobID, jobs))
    if len(foundJobs) == 0:
        abort(404)
    jobs.remove(foundJobs[0])
    return  jsonify( { 'result':True })

@app.errorhandler(404)
def not_found404(error):
    return make_response( jsonify( {'error':'Not found' }), 404)

@app.errorhandler(400)
def not_found400(error):
    return make_response( jsonify( {'error':'Bad Request' }), 400)


if __name__ == '__main__' :
    app.run(debug= True)