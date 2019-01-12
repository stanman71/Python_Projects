
########
REST API
########

IMPORTANT:
use in pythen shell
first steps: import requests, json 
             from requests.auth import HTTPBasicAuth


<<< Retrieve a task >>>  

requests.get('http://localhost:5000/api/resource/8', 
              auth=HTTPBasicAuth('admin', 'SuperSecretPwd')).json() 


<<< Retrieve list of tasks >>>

requests.get('http://localhost:5000/api/resource', 
              auth=HTTPBasicAuth('admin', 'SuperSecretPwd')).json() 


<<< Create a new task >>>

requests.post('http://localhost:5000/api/resource',
               headers={'Content-Type': 'application/json'},
               auth=HTTPBasicAuth('admin', 'SuperSecretPwd'),
               data=json.dumps({'username': 'Muster', 
                                'email': 'max@gmx.de', 
                                'password': 'geheim',
                                'role': 'user'})).json()


<<< Update an existing task >>>

requests.put('http://localhost:5000/api/resource/8', 
              auth=HTTPBasicAuth('admin', 'SuperSecretPwd'),
              headers={'Content-Type': 'application/json'},
              data=json.dumps({'role': 'superuser'})).json()


<<< Delete a task >>>

requests.delete('http://localhost:5000/api/resource/8', 
                 auth=HTTPBasicAuth('admin', 'SuperSecretPwd')).json() 


#################
DATABASE (MySQL):
#################

Database:  python
Tablename: user
           id       (Integer, primary_key)
           username (String(15), unique)
           email    (String(50), unique)
           password (String(80))
           role     (String(80))