import unittest

import requests
import json
#~ import responses



class TestCase(unittest.TestCase):

  #@responses.activate  
  def setUp(self):

    response = requests.get('https://tallersharedserver.herokuapp.com/test')
    self.assertEqual(json.dumps([]), response.text)
    self.assertEqual(201, response.status_code)
    
  def testCategoryInsertSimple(self):
    payload = {'category':{'name': 'sport', 'description': 'sport activities'}}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post('https://tallersharedserver.herokuapp.com/categories', data=json.dumps(payload), headers = headers)
    self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
    self.assertEqual(201, response.status_code)
    
    
  def checkEmptyBD(self):
	#Chequear que este vacio
	response = requests.get('http://localhost:8080/categories')
	espected = {"categories": [{}],"metadata": {"count": 0}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	self.assertEqual(201, response.status_code)
    
    
  def CategoryInsertAndDelete(self):
	self.checkEmptyBD()
	
	#Agregar categoria 1
	payload = {'category':{'name': 'sport2', 'description': 'sport activities2'}}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	response = requests.post('http://localhost:8080/categories', data=json.dumps(payload), headers = headers)
	self.assertEqual(json.dumps(payload), response.text)
	self.assertEqual(201, response.status_code)
	
	#Eliminamos categoria 1
	response = requests.delete('http://localhost:8080/categories/sport2')
	self.assertEqual(204, response.status_code)
	
	self.checkEmptyBD()
	
    
if __name__ == '__main__':
    unittest.main()
