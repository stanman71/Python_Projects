IMPORTANT:
use in pythen shell
first steps: import requests, json 
             from requests.auth import HTTPBasicAuth


<<< Retrieve a task >>>  

requests.get('http://localhost:5000/api/resource/8', 
              auth=HTTPBasicAuth('admin', 'SuperSecretPwd')).json() 


<<< Delete a task >>>

requests.delete('http://localhost:5000/api/resource/8', 
                 auth=HTTPBasicAuth('admin', 'SuperSecretPwd')).json() 


<<< Update an existing task >>>

requests.put('http://localhost:5000/api/resource/1', 
              auth=HTTPBasicAuth('admin', 'SuperSecretPwd'),
              headers={'Content-Type': 'application/json'},
              data=json.dumps({'email': 'go away'})).json()


<<< Retrieve list of tasks >>>

requests.get('http://localhost:5000/api/resource', 
              auth=HTTPBasicAuth('admin', 'SuperSecretPwd')).json() 


<<< Create a new task >>>

requests.post('http://localhost:5000/api/resource',
               headers={'Content-Type': 'application/json'},
               auth=HTTPBasicAuth('admin', 'SuperSecretPwd'),
               data=json.dumps({'username': 'Muster', 
                                'email': 'max@gmx.de', 
                                'password': 'geheim'})).json()

