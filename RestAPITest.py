import unittest

import requests
#~ import responses


#~ @httpretty.activate
#~ def test_one():
    #~ # define your patch:
    #~ httpretty.register_uri(httpretty.GET, "http://localhost:8080/test",
                        #~ body="Find the best daily deals")
    #~ # use!
    #~ response = requests.get('http://localhost:8080')
    #~ print response.text
    #~ assert response.text == "Find the best daily deals"
    #~ 



class TestCase(unittest.TestCase):

  #@responses.activate  
  def testExample(self):
    #~ responses.add(**{
      #~ 'method'         : responses.GET,
      #~ 'url'            : 'http://example.com/api/123',
      #~ 'body'           : '{"error": "reason"}',
      #~ 'status'         : 404,
      #~ 'content_type'   : 'application/json',
      #~ 'adding_headers' : {'X-Foo': 'Bar'}
    #~ })

    response = requests.get('http://localhost:8080/test')
    print response.text
    self.assertEqual('Prueba GET', response.text)
    #self.assertEqual(404, response.status_code)
    
    
if __name__ == '__main__':
    unittest.main()
