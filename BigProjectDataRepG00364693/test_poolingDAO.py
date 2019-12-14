from connectionPooling_jobDAO import jobDAO as jobDAO


jobs = jobDAO.getAll()
for job in jobs:
    print(job)