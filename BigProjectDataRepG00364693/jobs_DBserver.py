from flask import Flask, jsonify, request, abort
from jobDAO import jobDAO # take the job DAO/ read in
from flask_cors import CORS
app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

@app.route('/')
def index():
    return "Hello there, the jobs database server is running..."
CORS(app)

# Get all works:
# curl "http://127.0.0.1:5000/jobs"
@app.route('/jobs')
def getAll():
    #print("in getall")
    results = jobDAO.getAll()
    return jsonify(results)

# curl "http://127.0.0.1:5000/jobs/2"
@app.route('/jobs/<int:id>')
def findById(id):
    foundJob = jobDAO.findByID(id)

    return jsonify(foundJob)


# Create works:
# curl -i -H "Content-Type:application/json" -X POST -d "{\"id\":\"7\",\"location\":\"Galway\",\"jobTitle\":\"Data Engineer\", \"company\":\"Infosys\",\"salary\":65000}" http://localhost:5000/jobs

# curl -i -H "Content-Type:application/json" -X POST -d "{\"id\":\"4\",\"location\":\"Dublin\",\"jobTitle\":\"Database Admin\", \"company\":\"LinkedIn\",\"salary\":55000}" http://localhost:5000/jobs

# curl -i -H "Content-Type:application/json" -X POST -d "{\"id\":\"10\",\"location\":\"Dublin\",\"jobTitle\":\"Azure Cloud Architect\", \"company\":\"Car Trawler\",\"salary\":64000}" http://localhost:5000/jobs

# NOTE: You dont need to input a jobID for adding
@app.route('/jobs', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    job = {
        "location": request.json['location'],
        "jobTitle": request.json['jobTitle'],
        "company": request.json['company'],
        "salary": request.json['salary']
    }
    values =(job['location'],job['jobTitle'],job['company'],job['salary'])
    newId = jobDAO.create(values)
    job['id'] = newId
    return jsonify(job)

# Update works:
# curl -i -H "Content-Type:application/json" -X PUT -d "{\"id\":\"1\",\"company\":\"Google\"}" "http://127.0.0.1:5000/jobs/1"
# curl  -i -H "Content-Type:application/json" -X PUT -d "{\"location\":\"Cork\",\"jobTitle\":\"C++ Developer\",\"salary\":100000}" http://127.0.0.1:5000/jobs/1
@app.route('/jobs/<int:id>', methods=['PUT'])
def update(id):
    foundJob = jobDAO.findByID(id)
    if not foundJob:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json

    if 'salary' in reqJson and type(reqJson['salary']) is not int:
        abort(400)
		
    if 'location' in reqJson:
	    foundJob['location'] = reqJson['location']
	
    if 'jobTitle' in reqJson:
        foundJob['jobTitle'] = reqJson['jobTitle']
	
    if 'company' in reqJson:
        foundJob['company'] = reqJson['company']
		
    if 'salary' in reqJson:
        foundJob['salary'] = reqJson['salary']
		
	
    values = (foundJob['location'],foundJob['jobTitle'],foundJob['company'],foundJob['salary'],foundJob['id'],)
    jobDAO.update(values)
    return jsonify(foundJob)
        

# Delete works
# curl -X DELETE "http://127.0.0.1:5000/jobs/11"
@app.route('/jobs/<int:id>' , methods=['DELETE'])
def delete(id):
    jobDAO.delete(id)
    return jsonify({"done":True})
	


if __name__ == '__main__' :
    app.run(debug= True)