import unittest

import requests
import json
#~ import responses
#~ URL = 'http://localhost:8080'
URL = 'https://tallersharedserver.herokuapp.com'


class TestCase(unittest.TestCase):

  #@responses.activate  
  def setUp(self):
    response = requests.get(URL + '/test')
    self.assertEqual(json.dumps([]), response.text)
    self.assertEqual(201, response.status_code)
    self.checkEmptyBD()
    
  def CategoryInsertSimple(self, name, description): 
    payload = {'category':{'name': name, 'description': description}}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(URL + '/categories', data=json.dumps(payload), headers = headers)
    self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
    self.assertEqual(201, response.status_code)
    
  def CategoryDeleteSimple(self, name):
	response = requests.delete(URL + '/categories/' + name)
	self.assertEqual(204, response.status_code)
	
  def getCategories(self):
	   return requests.get(URL + '/categories')
    
    
  def checkEmptyBD(self):
	#Chequear que este vacio
	response = self.getCategories()
	espected = {"categories": [],"metadata": {"count": 0}}

	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	self.assertEqual(201, response.status_code)
    
    
  def testCategoryInsertAndDelete(self):
	self.checkEmptyBD()
	
	#Agregar categoria 1
	self.CategoryInsertSimple('sport', 'sport activities')
	
	response = self.getCategories()
	espected = {"categories": [{ "name": 'sport', "description": 'sport activities' }],"metadata": {"count": 1}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Eliminamos categoria 1
	self.CategoryDeleteSimple('sport')
	
	self.checkEmptyBD()
	
  def testCategoryIntertTwoDeleteTwo(self):
	self.checkEmptyBD()
	  
	#Agregar categoria 1
	self.CategoryInsertSimple('software', 'software activities')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'software', "description": 'software activities' }],"metadata": {"count": 1}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Agregar categoria 2
	self.CategoryInsertSimple('administration', 'administration activities')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'software', "description": 'software activities' },{ "name": 'administration', "description": 'administration activities' }],"metadata": {"count": 2}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Eliminamos categoria 2
	self.CategoryDeleteSimple('administration')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'software', "description": 'software activities' }],"metadata": {"count": 1}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Eliminamos categoria 1
	self.CategoryDeleteSimple('software')
	
	self.checkEmptyBD()
	
	
    
if __name__ == '__main__':
    unittest.main()
