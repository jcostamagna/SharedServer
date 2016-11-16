import unittest

import requests
import json
import __init__ as constant


class CategoriaHandler():

    def setUpHandler(self):
        response = requests.get(constant.URL + '/categories/test')
        self.assertEqual(json.dumps([]), response.text)
        self.assertEqual(201, response.status_code)
        self.checkEmptyBDCategory()

    def CategoryRequestInsert(self, name, description):
        payload = {'category': {'name': name, 'description': description}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + '/categories', data=json.dumps(payload), headers=headers), payload

    def CategoryInsertSimple(self, name, description):
        response, payload = self.CategoryRequestInsert(name, description)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def CategoryRequestInsertWithOutParameters(self):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + '/categories', data=json.dumps({}), headers=headers)

    def CategoryInsertSimpleExpectedError(self, name, description):
        response, payload = self.CategoryRequestInsert(name, description)
        self.assertEqual(500, response.status_code)

    def CategoryInsertNoParametersExpectedError(self):
        payload = {'code': 0, 'message': 'Faltan parametros'}
        response = self.CategoryRequestInsertWithOutParameters()
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(400, response.status_code)

    def CategoryRequestDelete(self, name):
        return requests.delete(constant.URL + '/categories/' + name)

    def CategoryDeleteSimple(self, name):
        response = self.CategoryRequestDelete(name)
        self.assertEqual(204, response.status_code)

    def CategoryDeleteExpectError(self, name):
        response = self.CategoryRequestDelete(name)
        self.assertEqual(404, response.status_code)

    def getCategories(self):
        return requests.get(constant.URL + '/categories')

    def checkEmptyBDCategory(self):
        # Chequear que este vacio
        response = self.getCategories()
        espected = {"categories": [], "metadata": {"version": "0.1", "count": 0}}

        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def CategoryRequestUpdate(self, oldName, newName, newDescription):
        payload = {'category': {'name': newName, 'description': newDescription}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + '/categories/' + oldName, data=json.dumps(payload),
                             headers=headers), payload

    def updateCategory(self, oldName, newName, newDescription):
        response, payload = self.CategoryRequestUpdate(oldName, newName, newDescription)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def updateCategoryExpectedError(self, oldName, newName, newDescription):
        response, payload = self.CategoryRequestUpdate(oldName, newName, newDescription)
        self.assertEqual(json.dumps({'code': 0, 'message': 'Categoria Inexistente'}),
                         json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)



class TestCategoria(unittest.TestCase, CategoriaHandler):

    # @responses.activate
    def setUp(self):
        #self.handler = CategoriaHandler()
        self.setUpHandler()

    def testCategoryInsertAndDelete(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('sport', 'sport activities')

        response = self.getCategories()
        espected = {"categories": [{"name": 'sport', "description": 'sport activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Eliminamos categoria 1
        self.CategoryDeleteSimple('sport')

        self.checkEmptyBDCategory()

    def testCategoryIntertTwoDeleteTwo(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Agregar categoria 2
        self.CategoryInsertSimple('administration', 'administration activities')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'},
                                   {"name": 'administration', "description": 'administration activities'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Eliminamos categoria 2
        self.CategoryDeleteSimple('administration')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Eliminamos categoria 1
        self.CategoryDeleteSimple('software')

        self.checkEmptyBDCategory()

    def testInsertTwiceGetError(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Agregar categoria 1
        self.CategoryInsertSimpleExpectedError('software', 'software activities')

    def testUpdateCategory(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('sport', 'sport activities')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'sport', "description": 'sport activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Actualizar categoria 1
        self.updateCategory('sport', 'outdoor activies', 'all kind of outdoor activities')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'outdoor activies', "description": 'all kind of outdoor activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Eliminar categoria 1
        self.CategoryDeleteSimple('outdoor activies')

        self.checkEmptyBDCategory()

    def testInsertDeleteUpdateMixed(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Agregar categoria 2
        self.CategoryInsertSimple('administration', 'administration activities')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'},
                                   {"name": 'administration', "description": 'administration activities'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Agregar categoria 3
        self.CategoryInsertSimple('music', 'all kind of music')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'},
                                   {"name": 'administration', "description": 'administration activities'},
                                   {"name": 'music', "description": 'all kind of music'}],
                    "metadata": {"version": "0.1", "count": 3}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Eliminamos categoria 2
        self.CategoryDeleteSimple('administration')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'},
                                   {"name": 'music', "description": 'all kind of music'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Actualizar categoria 3
        self.updateCategory('music', 'classic music', 'only classic music')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'software', "description": 'software activities'},
                                   {"name": 'classic music', "description": 'only classic music'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Eliminamos categoria 1
        self.CategoryDeleteSimple('software')

        # Chequeo de categorias
        response = self.getCategories()
        espected = {"categories": [{"name": 'classic music', "description": 'only classic music'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Eliminamos categoria 3
        self.CategoryDeleteSimple('classic music')

        self.checkEmptyBDCategory()

    def testInsertWithOutParametersExpectedError(self):
        self.checkEmptyBDCategory()

        # Agrego categoria sin parametros
        self.CategoryInsertNoParametersExpectedError()

        self.checkEmptyBDCategory()

    def testDeleteCategoryError(self):
        self.checkEmptyBDCategory()

        # Elimino categoria inexistente
        self.CategoryDeleteExpectError('software')

        self.checkEmptyBDCategory()


    def testUpdateCategoryError(self):
        self.checkEmptyBDCategory()

        # Updateo categoria inexistente
        self.updateCategoryExpectedError('sport', 'software', 'software activities new')

        self.checkEmptyBDCategory()




if __name__ == '__main__':
    unittest.main()
