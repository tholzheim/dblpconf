'''
Created on 31.01.2021

@author: wf
'''
from lodstorage.query import Query

class Code(object):
    '''
    a piece of code
    '''
    
    def __init__(self, name:str,text:str,lang:str='python'):
        '''
        construct me from the given text and language
        '''
        self.name=name
        self.text=text
        self.lang=lang
        
    def execute(self,context):
        '''
        https://stackoverflow.com/questions/701802/how-do-i-execute-a-string-containing-python-code-in-python
        https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3
        https://stackoverflow.com/questions/2220699/whats-the-difference-between-eval-exec-and-compile
        '''
        exec(self.text)
        pass

class LambdaAction(object):
    '''
    a lambda action
    '''

    def __init__(self, name:str,query:Query,code:Code):
        '''
        Constructor
        '''
        self.name=name
        self.query=query
        self.code=code
        
    def executeQuery(self,context):
        rows=None
        if "sqlDB" in context:
            db=context["sqlDB"]
            rows=db.query(self.query.query)
            context["rows"]=rows
        return rows
            
    def getMessage(self,context):
        message=None
        if 'result' in context:
            result=context['result']
            if 'message' in result:
                message=result["message"]
        return message
        
    def execute(self,context):
        '''
        run my query and feed the result into the given code
        
        Args:
            context(dict): a dictionary for the exchange of parameters
        '''
        self.executeQuery(context)
        self.code.execute(context)
        

