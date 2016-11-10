import unittest

import requests
import json
import __init__ as constant
from categoriaTest import CategoriaHandler


class TestSkill(unittest.TestCase, CategoriaHandler):

    # @responses.activate
    def setUp(self):
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

    def CategoryRequestInsert(self, name, description):
        payload = {'category': {'name': name, 'description': description}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + '/categories', data=json.dumps(payload), headers=headers), payload

    def CategoryInsertSimple(self, name, description):
        response, payload = self.CategoryRequestInsert(name, description)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def SkillRequestInsertWithOutParameters(self, category):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(constant.URL + 'skills/categories' + category, headers=headers)

    def SkillInsertSimpleExpectedError(self, name, description, category):
        response = self.SkillRequestInsert(name, description, category)
        payload = {'code': 0, 'message': 'Categoria Inexistente'}
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)

    def SkillInsertNoParametersExpectedError(self):
        payload = {'code': 0, 'message': 'Faltan parametros'}
        response = self.SkillRequestInsertWithOutParameters()
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(400, response.status_code)

    def SkillDeleteSimple(self, name, category):
        response = requests.delete(constant.URL + '/skills/categories/' + category + '/' + name)
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

    def SkillRequestUpdate(self, name,description, oldCategory, newCategory):
        payload = {'skill': {'name': name, 'category': newCategory, 'description': description}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.put(constant.URL + '/skills/categories/' + oldCategory + '/' + name, data=json.dumps(payload),
                             headers=headers), payload

    def updateSkill(self, name,description, oldCategory, newCategory):
        response, payload = self.SkillRequestUpdate(name, description, oldCategory, newCategory)
        self.assertEqual(json.dumps(payload), json.dumps(json.loads(response.text)))
        self.assertEqual(201, response.status_code)

    def updateSkillExpectedError(self, name, oldCategory, newCategory):
        response, payload = self.SkillRequestUpdate(name, oldCategory, newCategory)
        self.assertEqual(json.dumps({'code': 0, 'message': 'No existe el recurso solicitado'}),
                         json.dumps(json.loads(response.text)))
        self.assertEqual(404, response.status_code)

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

        response = self.getSkills()
        espected = {"skills": [{"name": 'c', "description": 'Programador en c', "category": 'software'}],
                    "metadata": {"version": "0.1", "count": 1}}
        self.assertEqual(json.dumps(espected), json.dumps(json.loads(response.text)))

        #Agregar Skill 2
        self.SkillInsertSimple('Aministrador', 'Administrador de empresas', 'administration')

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

    def testUpdateSkillNotExist(self):
        self.checkEmptyBDCategory()

        # Actualizo categoria Inexistente
        # self.updateCategoryExpectedError('sport', 'outdoor activies', 'all kind of outdoor activities')

        self.checkEmptyBDCategory()





if __name__ == '__main__':
    unittest.main()
