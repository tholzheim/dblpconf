'''
Created on 2020-12-30

@author: wf
'''
from fb4.app import AppWrap
from fb4.login_bp import LoginBluePrint
from flask_login import current_user, login_user,logout_user, login_required
from flask import send_file,abort
from fb4.widgets import Link, Icon, Image, MenuItem
from flask import render_template, url_for
from wikibot.wikiuser import WikiUser
from fb4.sqldb import db
from dblp.dblpxml import Dblp
import os

class WebServer(AppWrap):
    ''' 
    dblp conf webserver
    '''
    
    def __init__(self, host='0.0.0.0', port=8252, debug=False):
        '''
        constructor
        
        Args:
            wikiId(str): id of the wiki to use as a CMS backend
            host(str): flask host
            port(int): the port to use for http connections
            debug(bool): True if debugging should be switched on
        '''
        self.debug=debug
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        template_folder=scriptdir + '/../templates'
        super().__init__(host=host,port=port,debug=debug,template_folder=template_folder)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(self.app)
        self.db=db
        self.loginBluePrint=LoginBluePrint(self.app,'login')
        
        #
        # setup global handlers
        #
        @self.app.before_first_request
        def before_first_request_func():
            self.initDB()
            loginMenuList=self.adminMenuList("Login")
            self.loginBluePrint.setLoginArgs(menuList=loginMenuList)
            
        @self.app.route('/')
        def index():
            return self.index()
        
        @self.app.route('/sample/<entity>/<int:limit>')
        def showSample(entity,limit):
            return self.showSample(entity,limit)
        
    def initDB(self):
        '''
        initialize the database
        '''
        self.db.drop_all()
        self.db.create_all()
        self.initUsers()
        dblp=Dblp()
        self.sqlDB=dblp.getSqlDB(debug=self.debug)
        self.tableList=self.sqlDB.getTableList()
        self.tableDict={}
        for table in self.tableList:
            self.tableDict[table['name']]=table
    
    def initUsers(self):
        self.loginBluePrint.addUser(self.db,"admin","dblp")
        
    def showSample(self,entity,limit):
        
        if not entity in self.tableDict:
            abort(404)
        else:
            menuList=self.adminMenuList(entity)
            samples=self.sqlDB.query("select * from %s limit %d" % (entity,limit))
            html=render_template("sample.html",title=entity,menuList=menuList,dictList=samples)
            return html
            
    def adminMenuList(self,activeItem:str=None):
        '''
        get the list of menu items for the admin menu
        Args:
            activeItem(str): the active  menu item
        Return:
            list: the list of menu items
        '''
        menuList=[
            MenuItem(url_for('index'),'Home'),
            MenuItem('http://wiki.bitplan.com/index.php/Dblpconf','Docs'),
            MenuItem('https://github.com/WolfgangFahl/dblpconf','github'),
            ]
        if current_user.is_anonymous:
            menuList.append(MenuItem('/login','login'))
        else:
            menuList.append(MenuItem('/logout','logout'))
        for entity in self.tableDict.keys():
            url=url_for('showSample',entity=entity,limit=1000)
            title="%s" %entity
            menuList.append(MenuItem(url,title))
        
        if activeItem is not None:
            for menuItem in menuList:
                if menuItem.title==activeItem:
                    menuItem.active=True
                if menuItem.url.startswith("/"):
                    menuItem.url="%s%s" % (self.baseUrl,menuItem.url)
        return menuList
    
    def index(self):
        menuList=self.adminMenuList("Home")
        html=render_template("index.html",title="Home", menuList=menuList)
        return html

if __name__ == '__main__':
    # construct the web application    
    web=WebServer()
    parser=web.getParser(description="dblp conference webservice")
    args=parser.parse_args()
    web.optionalDebug(args)
    web.run(args)