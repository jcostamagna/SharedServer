import unittest

import requests
import json
import __init__ as constant
from categoriaTest import CategoriaHandler


class SkillHandler():

    # @responses.activate
    def setUpSkillHandler(self):
        response = requests.get(constant.URL + '/skills/test')
        self.assertEqual(json.dumps([]), response.text)
        self.assertEqual(201, response.status_code)
        self.checkEmptyBDSkill()
        self.setUpHandler();

    def SkillRequestInsert(self, name, description, category):
        payload = {'skill': {'name': name, 'description': description}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + '/skills/categories/' + category, data=json.dumps(payload),
                             headers=headers)

    def SkillInsertSimple(self, name, description, category):
        response = self.SkillRequestInsert(name, description, category)
        payload = {'skill': {'name': name, 'description': description, 'category': category}}
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)


    def SkillRequestInsertWithOutParameters(self, category):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + '/skills/categories/' + category, data=json.dumps({}), headers=headers)

    def SkillInsertSimpleExpectedError(self, name, description, category):
        response = self.SkillRequestInsert(name, description, category)
        payload = {'code': 0, 'message': 'Categoria Inexistente'}
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)

    def SkillInsertNoParametersExpectedError(self, category):
        payload = {'code': 0, 'message': 'Faltan parametros'}
        response = self.SkillRequestInsertWithOutParameters(category)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(400, response.status_code)

    def SkillRequestUpdateWithOutParameters(self, oldCategory, name):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.put(constant.URL + '/skills/categories/' + oldCategory + '/' + name, headers=headers)

    def SkillUpdateNoParametersExpectedError(self, oldCategory, name):
        payload = {'code': 0, 'message': 'Faltan parametros'}
        response = self.SkillRequestUpdateWithOutParameters(oldCategory, name)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(400, response.status_code)

    def SkillRequestDelete(self, name, category):
        return requests.delete(constant.URL + '/skills/categories/' + category + '/' + name)

    def SkillDeleteSimple(self, name, category):
        response = self.SkillRequestDelete(name, category)
        self.assertEqual(204, response.status_code)

    def getSkills(self):
        return requests.get(constant.URL + '/skills')

    def getSkillsByCategory(self, category):
        return requests.get(constant.URL + '/skills/categories/' + category)

    def checkEmptyBDSkill(self):
        # Chequear que este vacio
        response = self.getSkills()
        espected = {"skills": [], "metadata": {"version": "0.1", "count": 0}}

        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def SkillRequestUpdate(self, name, description, oldCategory, newCategory):
        payload = {'skill': {'name': name, 'category': newCategory, 'description': description}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.put(constant.URL + '/skills/categories/' + oldCategory + '/' + name, data=json.dumps(payload),
                             headers=headers), payload

    def updateSkill(self, name,description, oldCategory, newCategory):
        response, payload = self.SkillRequestUpdate(name, description, oldCategory, newCategory)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def updateSkillExpectedError(self, name, description, oldCategory, newCategory):
        response, payload = self.SkillRequestUpdate(name, description, oldCategory, newCategory)
        self.assertEqual(json.dumps({'code': 0, 'message': 'Categoria Inexistente'}),
                         json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)

    def SkillDeleteExpectedError(self, name, category):
        response = self.SkillRequestDelete(name, category)
        self.assertEqual(json.dumps({'code': 0, 'message': 'Categoria Inexistente'}),
                         json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)



class TestSkill(unittest.TestCase, CategoriaHandler, SkillHandler):

    # @responses.activate
    def setUp(self):
        self.setUpSkillHandler()


    def testSkillInsertAndDelete(self):
        self.checkEmptyBDCategory()
        self.checkEmptyBDSkill()

        # Agregar categoria 1
        self.CategoryInsertSimple('sport', 'sport activities')

        response = self.getCategories()
        espected = {"categories": [{"name": 'sport', "description": 'sport activities'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agrego Skill
        self.SkillInsertSimple('Futbol', 'Saber jugar al futbol', 'sport')

        response = self.getSkills()
        espected = {"skills": [{"name": 'Futbol', "description": 'Saber jugar al futbol', "category": 'sport'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        response = self.getSkillsByCategory('sport')
        espected = {"skills": [{"name": 'Futbol', "description": 'Saber jugar al futbol', "category": 'sport'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Elimino Skill
        self.SkillDeleteSimple('Futbol','sport')

        self.checkEmptyBDSkill()

        # Eliminamos categoria 1
        self.CategoryDeleteSimple('sport')

        self.checkEmptyBDCategory()

    def testSkillIntertTwoDeleteTwo(self):
        self.checkEmptyBDCategory()
        self.checkEmptyBDSkill()

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

        #Agregar Skill 1
        self.SkillInsertSimple('c', 'Programador en c', 'software')

        #Chequeo Skills
        response = self.getSkills()
        espected = {"skills": [{"name": 'c', "description": 'Programador en c', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agregar Skill 2
        self.SkillInsertSimple('Aministrador', 'Administrador de empresas', 'administration')

        # Chequeo Skills
        response = self.getSkillsByCategory('administration')
        espected = {"skills": [{"name": 'Aministrador', "description": 'Administrador de empresas', "category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Chequeo ambos skills
        response = self.getSkills()
        espected = {"skills": [{"name": 'c', "description": 'Programador en c', "category": 'software'},
                               {"name": 'Aministrador', "description": 'Administrador de empresas',"category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Elimino Skill 1
        self.SkillDeleteSimple('c','software')

        #Chequeo Skills
        response = self.getSkillsByCategory('administration')
        espected = {"skills": [{"name": 'Aministrador', "description": 'Administrador de empresas', "category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        response = self.getSkillsByCategory('software')
        espected = {"skills": [], "metadata": {"version": "0.1", "count": 0}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        response = self.getSkills()
        espected = {"skills": [{"name": 'Aministrador', "description": 'Administrador de empresas', "category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Elimino Skill 2
        self.SkillDeleteSimple('Aministrador','administration')

        #Chequeo skills
        response = self.getSkillsByCategory('administration')
        espected = {"skills": [], "metadata": {"version": "0.1", "count": 0}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        self.checkEmptyBDSkill()

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
        self.checkEmptyBDSkill()

        # Agregar Skill 1
        self.SkillInsertSimpleExpectedError('c', 'Programador en c', 'software')

        self.checkEmptyBDSkill()


    def testUpdateSkill(self):
        self.checkEmptyBDCategory()
        self.checkEmptyBDSkill()

        # Agregar categoria 1
        self.CategoryInsertSimple('sport', 'sport activities')

        # Agregar categoria 2
        self.CategoryInsertSimple('software', 'software activities')

        #Agrego Skill
        self.SkillInsertSimple('Futbol', 'Saber jugar al futbol', 'software')

        # Chequeo de Skills
        response = self.getSkills()
        espected = {"skills": [{"name": 'Futbol', "description": 'Saber jugar al futbol', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Update Skill
        self.updateSkill('Futbol','Saber jugar al futbol', 'software', 'sport')

        #Chequeo de Skills
        response = self.getSkills()
        espected = {"skills": [{"name": 'Futbol', "description": 'Saber jugar al futbol', "category": 'sport'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Eliminar Skill
        self.SkillDeleteSimple('Futbol', 'sport')

        self.checkEmptyBDSkill()

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

        #Agregar Skill 1
        self.SkillInsertSimple('c', 'Programador en c', 'software')

        #Chequeo Skills
        response = self.getSkills()
        espected = {"skills": [{"name": 'c', "description": 'Programador en c', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agregar Skill 2
        self.SkillInsertSimple('Aministrador', 'Administrador de empresas', 'administration')

        # Chequeo Skills
        response = self.getSkillsByCategory('administration')
        espected = {"skills": [{"name": 'Aministrador', "description": 'Administrador de empresas', "category": 'administration'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agregar Skill 3
        self.SkillInsertSimple('java', 'Programador en java', 'software')

        #Chequeo Skills
        response = self.getSkillsByCategory('software')
        espected = {"skills": [{"name": 'c', "description": 'Programador en c', "category": 'software'},
                               {"name": 'java', "description": 'Programador en java', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Actualizar Skill
        self.updateSkill('Aministrador', 'Administrador de juegos de soft', 'administration', 'software')

        #Chequeo Skills
        response = self.getSkillsByCategory('software')
        espected = {"skills": [{"name": 'c', "description": 'Programador en c', "category": 'software'},
                               {"name": 'java', "description": 'Programador en java', "category": 'software'},
                               {"name": 'Aministrador', "description": 'Administrador de juegos de soft', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 3}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        response = self.getSkills()
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Delete Skill 3
        self.SkillDeleteSimple('Aministrador','software')

        #Chequeo Skills
        response = self.getSkillsByCategory('software')
        espected = {"skills": [{"name": 'c', "description": 'Programador en c', "category": 'software'},
                               {"name": 'java', "description": 'Programador en java', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 2}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        response = self.getSkills()
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Delete Skill 1
        self.SkillDeleteSimple('c', 'software')

        #Chequeo Skills
        response = self.getSkillsByCategory('software')
        espected = {"skills": [{"name": 'java', "description": 'Programador en java', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        response = self.getSkills()
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        # Delete Skill 2
        self.SkillDeleteSimple('java', 'software')

        # Chequeo Skills
        response = self.getSkillsByCategory('software')
        espected = {"skills": [],
                    "metadata": {"version": "0.1", "count": 0}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))
        response = self.getSkills()
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Elimino Categorias
        self.setUpHandler()

        self.checkEmptyBDSkill()
        self.checkEmptyBDCategory()

    def testInsertWithOutParametersExpectedError(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Agrego skill sin parametros
        self.SkillInsertNoParametersExpectedError('software')

        #Agrego Skill
        self.SkillInsertSimple('c', 'Programador en c', 'software')

        #Update de skill sin parametros
        self.SkillUpdateNoParametersExpectedError('software', 'c')

        #Clean
        self.setUp()
        self.setUpHandler()

        self.checkEmptyBDCategory()

    def testDeleteSkillError(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Agrego Skill
        self.SkillInsertSimple('c', 'Programador en c', 'software')

        # Agrego Skill
        self.SkillInsertSimple('Java', 'Programador en Java', 'software')

        #Delete Skill con categoria inexistente
        self.SkillDeleteExpectedError('c', 'administration')

        # Clean
        self.setUp()
        self.setUpHandler()

        self.checkEmptyBDCategory()


    def testUpdateSkillError(self):
        self.checkEmptyBDCategory()

        # Agregar categoria 1
        self.CategoryInsertSimple('software', 'software activities')

        # Agrego Skill
        self.SkillInsertSimple('c', 'Programador en c', 'software')

        # Delete Skill con categoria inexistente
        self.updateSkillExpectedError('c', 'Programador en c', 'software', 'administration')

        # Clean
        self.setUp()
        self.setUpHandler()

        self.checkEmptyBDCategory()






if __name__ == '__main__':
    unittest.main()
