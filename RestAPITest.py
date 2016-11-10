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
    
    
  def CategoryRequestInsert(self, name, description):
    payload = {'category':{'name': name, 'description': description}}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return requests.post(URL + '/categories', data=json.dumps(payload), headers = headers), payload
    
  def CategoryInsertSimple(self, name, description): 
	response, payload = self.CategoryRequestInsert(name, description)
	self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
	self.assertEqual(201, response.status_code)
    
  def CategoryInsertSimpleExpectedError(self, name, description): 
    response, payload = self.CategoryRequestInsert(name, description)
    self.assertEqual(500, response.status_code)
    
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
	
  def updateCategory(self, oldName, newName, newDescription):
	payload = {'category':{'name': newName, 'description': newDescription}}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	response = requests.post(URL + '/categories/' + oldName, data=json.dumps(payload), headers = headers)
	self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
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
	
  def testInsertTwiceGetError(self):
	self.checkEmptyBD()
	  
	#Agregar categoria 1
	self.CategoryInsertSimple('software', 'software activities')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'software', "description": 'software activities' }],"metadata": {"count": 1}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Agregar categoria 1
	self.CategoryInsertSimpleExpectedError('software', 'software activities')
	
  def testUpdateCategory(self):
	self.checkEmptyBD()
	  
	#Agregar categoria 1
	self.CategoryInsertSimple('sport', 'sport activities')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'sport', "description": 'sport activities' }],"metadata": {"count": 1}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Actualizar categoria 1
	self.updateCategory('sport', 'outdoor activies', 'all kind of outdoor activities')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'outdoor activies', "description": 'all kind of outdoor activities' }],"metadata": {"count": 1}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Eliminar categoria 1
	self.CategoryDeleteSimple('outdoor activies')
	
	self.checkEmptyBD()
	
  def testInsertDeleteUpdateMixed(self):
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
	
	#Agregar categoria 3
	self.CategoryInsertSimple('music', 'all kind of music')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'software', "description": 'software activities' },
	{ "name": 'administration', "description": 'administration activities' },
	{ "name": 'music', "description": 'all kind of music' }],"metadata": {"count": 3}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Eliminamos categoria 2
	self.CategoryDeleteSimple('administration')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'software', "description": 'software activities' },
	{ "name": 'music', "description": 'all kind of music' }],"metadata": {"count": 2}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Actualizar categoria 3
	self.updateCategory('music', 'classic music', 'only classic music')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'software', "description": 'software activities' },
	{ "name": 'classic music', "description": 'only classic music' }],"metadata": {"count": 2}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Eliminamos categoria 1
	self.CategoryDeleteSimple('software')
	
	#Chequeo de categorias
	response = self.getCategories()
	espected = {"categories": [{ "name": 'classic music', "description": 'only classic music' }],"metadata": {"count": 1}}
	self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
	
	#Eliminamos categoria 3
	self.CategoryDeleteSimple('classic music')
	
	self.checkEmptyBD()
	
    
if __name__ == '__main__':
    unittest.main()
