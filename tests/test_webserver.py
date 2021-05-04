'''
Created on 2021-01-26

@author: wf
'''
import unittest
from dblp.webserver import WebServer
import tests.test_dblp
import getpass

class TestWebServer(unittest.TestCase):

    def setUp(self):
        '''
        test the webserver
        ''' 
        if getpass.getuser()!="wf":
            return
        self.debug=False
        mock=True
        dblp=tests.test_dblp.TestDblp.getMockedDblp(mock, debug=self.debug) 
        self.web=WebServer(dblp)
        app=self.web.app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        pass
    
    def getResponse(self,query):
        response=self.app.get(query)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data is not None)
        html=response.data.decode()
        if self.debug:
            print(html)
        return html

    def tearDown(self):
        pass

    def testSamples(self):
        '''
        test the samples handling
        '''
        if getpass.getuser()!="wf":
            return
        html=self.getResponse("/sample/dblp/article/100")
        self.assertTrue("<th> publtype </th>" in html)
        pass

    def testOREvents(self):
        '''
        test OPENSRESEARCH event list
        '''
        if getpass.getuser()!="wf":
            return
        html=self.getResponse("/openresearch/Event")
        self.assertTrue("acronym" in html)
        pass

    def testORCountries(self):
        '''
        test OPENSRESEARCH event list
        '''
        if getpass.getuser()!="wf":
            return
        html=self.getResponse("/openresearch/Country")
        self.assertTrue("wikidataId" in html)
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()