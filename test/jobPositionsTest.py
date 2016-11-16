import unittest

import requests
import json
import __init__ as constant
from categoriaTest import CategoriaHandler


class JobHandler():

    # @responses.activate
    def setUpJobHandler(self):
        response = requests.get(constant.URL + '/job_positions/test')
        self.assertEqual(json.dumps([]), response.text)
        self.assertEqual(201, response.status_code)
        self.checkEmptyBDJob()
        self.setUpHandler();

    def JobRequestInsert(self, name, description, category):
        payload = {'job_position': {'name': name, 'description': description}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + '/job_positions/categories/' + category, data=json.dumps(payload),
                             headers=headers)

    def JobInsertSimple(self, name, description, category):
        response = self.JobRequestInsert(name, description, category)
        payload = {'job_position': {'name': name, 'description': description, 'category': category}}
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)


    def JobRequestInsertWithOutParameters(self, category):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + '/job_positions/categories/' + category, data=json.dumps({}), headers=headers)

    def JobInsertSimpleExpectedError(self, name, description, category):
        response = self.JobRequestInsert(name, description, category)
        payload = {'code': 0, 'message': 'Categoria Inexistente'}
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)

    def JobInsertNoParametersExpectedError(self, category):
        payload = {'code': 0, 'message': 'Faltan parametros'}
        response = self.JobRequestInsertWithOutParameters(category)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(400, response.status_code)

    def JobRequestUpdateWithOutParameters(self, oldCategory, name):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.put(constant.URL + '/job_positions/categories/' + oldCategory + '/' + name, headers=headers)

    def JobUpdateNoParametersExpectedError(self, oldCategory, name):
        payload = {'code': 0, 'message': 'Faltan parametros'}
        response = self.JobRequestUpdateWithOutParameters(oldCategory, name)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(400, response.status_code)

    def JobRequestDelete(self, name, category):
        return requests.delete(constant.URL + '/job_positions/categories/' + category + '/' + name)

    def JobDeleteSimple(self, name, category):
        response = self.JobRequestDelete(name, category)
        self.assertEqual(204, response.status_code)

    def getJobs(self):
        return requests.get(constant.URL + '/job_positions')

    def getJobsByCategory(self, category):
        return requests.get(constant.URL + '/job_positions/categories/' + category)

    def checkEmptyBDJob(self):
        # Chequear que este vacio
        response = self.getJobs()
        espected = {"job_positions": [], "metadata": {"version": "0.1", "count": 0}}

        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def JobRequestUpdate(self, name, description, oldCategory, newCategory):
        payload = {'job_position': {'name': name, 'category': newCategory, 'description': description}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.put(constant.URL + '/job_positions/categories/' + oldCategory + '/' + name, data=json.dumps(payload),
                             headers=headers), payload

    def updateJob(self, name,description, oldCategory, newCategory):
        response, payload = self.JobRequestUpdate(name, description, oldCategory, newCategory)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def updateJobExpectedError(self, name, description, oldCategory, newCategory):
        response, payload = self.JobRequestUpdate(name, description, oldCategory, newCategory)
        self.assertEqual(json.dumps({'code': 0, 'message': 'Categoria Inexistente'}),
                         json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)

    def JobDeleteExpectedError(self, name, category):
        response = self.JobRequestDelete(name, category)
        self.assertEqual(json.dumps({'code': 0, 'message': 'Categoria Inexistente'}),
                         json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)



class TestJobs(unittest.TestCase, CategoriaHandler, JobHandler):

    # @responses.activate
    def setUp(self):
        self.setUpJobHandler()


    def testJobInsertAndDelete(self):
        self.checkEmptyBDCategory()
        self.checkEmptyBDJob()

        # Agregar categoria 1
        self.CategoryInsertSimple('sport', 'sport activities')

        response = self.getCategories()
        espected = {"categories": [{"name": 'sport', "description": 'sport activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agrego Job
        self.JobInsertSimple('Futbol', 'Saber jugar al futbol', 'sport')

        response = self.getJobs()
        espected = {"job_positions": [{"name": 'Futbol', "description": 'Saber jugar al futbol', "category": 'sport'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        response = self.getJobsByCategory('sport')
        espected = {"job_positions": [{"name": 'Futbol', "description": 'Saber jugar al futbol', "category": 'sport'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Elimino Job
        self.JobDeleteSimple('Futbol','sport')

        self.checkEmptyBDJob()

        # Eliminamos categoria 1
        self.CategoryDeleteSimple('sport')

        self.checkEmptyBDCategory()

    def testJobIntertTwoDeleteTwo(self):
        self.checkEmptyBDCategory()
        self.checkEmptyBDJob()

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

        #Agregar Job 1
        self.JobInsertSimple('c', 'Programador en c', 'software')

        #Chequeo Jobs
        response = self.getJobs()
        espected = {"job_positions": [{"name": 'c', "description": 'Programador en c', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agregar Job 2
        self.JobInsertSimple('Aministrador', 'Administrador de empresas', 'administration')

        # Chequeo Jobs
        response = self.getJobsByCategory('administration')
        espected = {"job_positions": [{"name": 'Aministrador', "description": 'Administrador de empresas', "category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Chequeo ambos Jobs
        response = self.getJobs()
        espected = {"job_positions": [{"name": 'c', "description": 'Programador en c', "category": 'software'},
                               {"name": 'Aministrador', "description": 'Administrador de empresas',"category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Elimino Job 1
        self.JobDeleteSimple('c','software')

        #Chequeo Jobs
        response = self.getJobsByCategory('administration')
        espected = {"job_positions": [{"name": 'Aministrador', "description": 'Administrador de empresas', "category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        response = self.getJobsByCategory('software')
        espected = {"job_positions": [], "metadata": {"version": "0.1", "count": 0}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        response = self.getJobs()
        espected = {"job_positions": [{"name": 'Aministrador', "description": 'Administrador de empresas', "category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Elimino Job 2
        self.JobDeleteSimple('Aministrador','administration')

        #Chequeo Jobs
        response = self.getJobsByCategory('administration')
        espected = {"job_positions": [], "metadata": {"version": "0.1", "count": 0}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        self.checkEmptyBDJob()

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


    def testNoExistCategoryError(self):
        self.checkEmptyBDCategory()
        self.checkEmptyBDJob()

        # Agregar Job 1
        self.JobInsertSimpleExpectedError('c', 'Programador en c', 'software')

        self.checkEmptyBDJob()


    def testUpdateJob(self):
        self.checkEmptyBDCategory()
        self.checkEmptyBDJob()

        # Agregar categoria 1
        self.CategoryInsertSimple('sport', 'sport activities')

        # Agregar categoria 2
        self.CategoryInsertSimple('software', 'software activities')

        #Agrego Job
        self.JobInsertSimple('Futbol', 'Saber jugar al futbol', 'software')

        # Chequeo de Jobs
        response = self.getJobs()
        espected = {"job_positions": [{"name": 'Futbol', "description": 'Saber jugar al futbol', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Update Job
        self.updateJob('Futbol','Saber jugar al futbol', 'software', 'sport')

        #Chequeo de Jobs
        response = self.getJobs()
        espected = {"job_positions": [{"name": 'Futbol', "description": 'Saber jugar al futbol', "category": 'sport'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Eliminar Job
        self.JobDeleteSimple('Futbol', 'sport')

        self.checkEmptyBDJob()

        # Eliminar categoria 1
        self.CategoryDeleteSimple('sport')

        # Eliminar categoria 2
        self.CategoryDeleteSimple('software')

        self.checkEmptyBDCategory()


    def testInsertDeleteUpdateMixed(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')


        # Agregar categoria 2
        self.CategoryInsertSimple('administration', 'administration activities')


        # Agregar categoria 3
        self.CategoryInsertSimple('music', 'all kind of music')

        #Agregar Job 1
        self.JobInsertSimple('c', 'Programador en c', 'software')

        #Chequeo Jobs
        response = self.getJobs()
        espected = {"job_positions": [{"name": 'c', "description": 'Programador en c', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agregar Job 2
        self.JobInsertSimple('Aministrador', 'Administrador de empresas', 'administration')

        # Chequeo Jobs
        response = self.getJobsByCategory('administration')
        espected = {"job_positions": [{"name": 'Aministrador', "description": 'Administrador de empresas', "category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agregar Job 3
        self.JobInsertSimple('java', 'Programador en java', 'software')

        #Chequeo Jobs
        response = self.getJobsByCategory('software')
        espected = {"job_positions": [{"name": 'c', "description": 'Programador en c', "category": 'software'},
                               {"name": 'java', "description": 'Programador en java', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Actualizar Job
        self.updateJob('Aministrador', 'Administrador de juegos de soft', 'administration', 'software')

        #Chequeo Jobs
        response = self.getJobsByCategory('software')
        espected = {"job_positions": [{"name": 'c', "description": 'Programador en c', "category": 'software'},
                               {"name": 'java', "description": 'Programador en java', "category": 'software'},
                               {"name": 'Aministrador', "description": 'Administrador de juegos de soft', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 3}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        response = self.getJobs()
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Delete Job 3
        self.JobDeleteSimple('Aministrador','software')

        #Chequeo Jobs
        response = self.getJobsByCategory('software')
        espected = {"job_positions": [{"name": 'c', "description": 'Programador en c', "category": 'software'},
                               {"name": 'java', "description": 'Programador en java', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        response = self.getJobs()
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Delete Job 1
        self.JobDeleteSimple('c', 'software')

        #Chequeo Jobs
        response = self.getJobsByCategory('software')
        espected = {"job_positions": [{"name": 'java', "description": 'Programador en java', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        response = self.getJobs()
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Delete Job 2
        self.JobDeleteSimple('java', 'software')

        # Chequeo Jobs
        response = self.getJobsByCategory('software')
        espected = {"job_positions": [],
                    "metadata": {"version": "0.1", "count": 0}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        response = self.getJobs()
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Elimino Categorias
        self.setUpHandler()

        self.checkEmptyBDJob()
        self.checkEmptyBDCategory()

    def testInsertWithOutParametersExpectedError(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Agrego Job sin parametros
        self.JobInsertNoParametersExpectedError('software')

        #Agrego Job
        self.JobInsertSimple('c', 'Programador en c', 'software')

        #Update de Job sin parametros
        self.JobUpdateNoParametersExpectedError('software', 'c')

        #Clean
        self.setUp()
        self.setUpHandler()

        self.checkEmptyBDCategory()

    def testDeleteJobError(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Agrego Job
        self.JobInsertSimple('c', 'Programador en c', 'software')

        # Agrego Job
        self.JobInsertSimple('Java', 'Programador en Java', 'software')

        #Delete Job con categoria inexistente
        self.JobDeleteExpectedError('c', 'administration')

        # Clean
        self.setUp()
        self.setUpHandler()

        self.checkEmptyBDCategory()


    def testUpdateJobError(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Agrego Job
        self.JobInsertSimple('c', 'Programador en c', 'software')

        # Delete Job con categoria inexistente
        self.updateJobExpectedError('c', 'Programador en c', 'software', 'administration')

        # Clean
        self.setUp()
        self.setUpHandler()

        self.checkEmptyBDCategory()






if __name__ == '__main__':
    unittest.main()
