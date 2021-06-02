#!/usr/bin/python3
"""
# ## Start this Web Service like
# python .\TrainManagementWebServer.py [ ElectronicController.DummyController ]
# ex in web browser : http://localhost:8088/TrainManagement.py?control=get_help&functionName=Switch&functionValue=Off

# ## Call this WebService in Powershell like
# curl -Headers @{ "Accept" = "application/json" } "http://otter:8088/train_control/test=34&tty=toto"
# curl -Headers @{ "Accept" = "application/json" } "http://otter:8088/demo/register_switch_value" -Body @{"name" = "tty"; "value" = 1} -ContentType "application/json; charset=utf-8"
"""

import sys
import os.path as pth
import re

sys.path.append(pth.dirname(pth.realpath(__file__)))

# -- WebService part
import web, requests, json

# ---------------- Add Path  --------------------------------------------------

local_directory = pth.dirname(pth.abspath(__file__))
import_list = (
    local_directory
    , pth.realpath(pth.join(local_directory, "TrainLibraries.zip"))
    , pth.realpath(pth.join(local_directory, "Model"))
    , pth.realpath(pth.join(local_directory, "Controller"))
    , pth.realpath(pth.join(local_directory, "ElectronicComponents"))
    , pth.realpath(pth.join(local_directory, "ElectronicModel"))
)

for to_import in import_list:
  if not pth.exists(to_import): continue
  if not to_import in sys.path: sys.path.append(to_import)
# -----------------------------------------------------------------------------

from Controller.FactoryController import ControllerFactory

class WebHttpThread(object):
    """ Main class (starting point) use into a thread to response on http requests """

    _allow_origin = '*'
    _allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
    _allow_headers = 'Authorization, Origin, Accept, Content-Type, Content-Length, X-Requested-With, X-CSRF-Token'
    
    render_xml = lambda message: '<message>%s</message>'%message
    render_json = lambda obj: json.dumps(obj, default='"')
    render_html = lambda message: '<html><body>%s</body></html>'%message
    render_txt = lambda message: message

    # define routes for application
    _urls = (
        '/', 'home_controller',
        '/home/(.*)', 'HomeController',
        '/train_control/(.*)', 'TrainController',
        '/demo/(.*)', 'DemoController'
    )

    @classmethod
    def get_post_json_params(cls):
        """Return the json object from post params"""
        post_params = web.data().decode('utf-8')    
        return json.loads(post_params)

    @classmethod
    def json_app_rqt(cls):
        """Define the request format for web user"""
        web.request.accept = 'application/json, text/plain; charset=utf-8'

    @classmethod
    def json_app_resp(cls):
        """Define the response format for web user"""
        web.header('Access-Control-Allow-Origin', WebHttpThread._allow_origin)
        web.header('Access-Control-Allow-Methods', WebHttpThread._allow_methods)
        web.header('Content-Type', 'application/json; charset=utf-8')

    @classmethod
    def run_webhttp(cls, port=8080, *middleware):
        """Start the web server"""
        try:
            print("Starting the web server part")
            app = web.application(cls._urls, globals())
            func = app.wsgifunc(*middleware)
            print("Web server for TrainManagement, listening on:", end=' ')
            return web.httpserver.runsimple(func, ('0.0.0.0', port))
        except KeyboardInterrupt:
            print("Server stopped")
            pass

#End Class WebHttpThread
    
#-- Class Controllers (linked to the routes)
class HomeController(object):
    """ This controller is used for the human interaction """
    def GET(self, name = ""):
        """The get method is called for software control"""
        WebHttpThread.json_app_resp()
        if not name == "":
            name = 'world'
        return WebHttpThread.render_json( {'message': 'Hello, %s!' % name} )

    def POST(self, name = ""):
        """This post method is use for the business communication"""
        json_app_resp()
        params = WebHttpThread.get_post_json_params()

        if not name == "":
            name = 'world'
        return WebHttpThread.render_json( {'message': 'Hello, %s!' % name} )

class DemoController(object):
    """ This is the Demo Controller """

    def GET(self, name):
        WebHttpThread.json_app_resp()

        return WebHttpThread.render_json( {'message': 'OK', 'action': name} )

    def POST(self, action_str):
        WebHttpThread.json_app_resp()
        params = WebHttpThread.get_post_json_params()
        ctrl = ControllerFactory.get_controller()
        obj_response = ctrl.start_demo() if action_str == "start" else ctrl.stop_demo()
        obj_response = {"result": "ok"}

        return WebHttpThread.render_json( obj_response )

class TrainController(object):
    """ This Controller is used for the web services communication (REST) with automate """

    def GET(self, str_params):
        WebHttpThread.json_app_resp()

        dict_params = { k:v for k, v in [param.split("=") for param in str_params.split("&")] }
        return WebHttpThread.render_json( dict_params )

    def POST(self, action):

        WebHttpThread.json_app_resp()
        json_params = WebHttpThread.get_post_json_params()
        print("POST requested : %s" % (action), end = ' ')
        print(json_params)

        obj_response = ControllerFactory.get_controller().do( action, json_params )
        return WebHttpThread.render_json( obj_response )
    
    # End Class Controller


if __name__ == "__main__":
    ControllerFactory.get_controller()
    WebHttpThread.run_webhttp(port=8088)
    print("Bye")

