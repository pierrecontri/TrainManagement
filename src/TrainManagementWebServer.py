#!/usr/bin/python3

# ex in web browser : http://localhost:8088/TrainManagement.py?control=get_help&functionName=Switch&functionValue=Off

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


# -- WebService part
import web, requests, json

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, Content-Length, X-Requested-With, X-CSRF-Token'

render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda obj: json.dumps(obj, default='"')
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message

# define routes for application
urls = (
    '/', 'home_control',
    '/home/(.*)', 'home_control',
    '/train_control/(.*)', 'train_control',
    '/demo/(.*)', 'demo'
)
app = web.application(urls, globals())

def get_post_json_params():
    """Return the json object from post params"""
    post_params = web.data().decode('utf-8')
    print(post_params)
    json_params = json.loads(post_params)

    return json_params

def json_app_rqt():
    """Define the request format for web user"""
    web.request.accept = 'application/json, text/plain; charset=utf-8'

def json_app_resp():
    """Define the response format fot web user"""
    web.header('Access-Control-Allow-Origin', _allow_origin)
    web.header('Access-Control-Allow-Methods', _allow_methods)
    web.header('Content-Type', 'application/json; charset=utf-8')

# -- End WebService part


# -- Using ElectronicControler

# Create the real controler
# With specifications in args
dynamic_controler_name = sys.argv[1] if len(sys.argv) > 1 else "ElectronicControler.DummyControler"
dynamic_controler = __import__(dynamic_controler_name, fromlist=["*"])
controler = dynamic_controler.Controler()
# print the controler type
print("Controler name loaded: %s" % dynamic_controler.__name__)
print("Controler class name: %s" % type(controler))
# -- End Using ElectronicControler

#-- Class Controlers (linked to the routes)
class home_control:

    def GET(self, name = ""):
        json_app_resp()
        if not name == "":
            name = 'world'
        return render_json( {'message': 'Hello, %s!' % name} )

    def POST(self, name = ""):
        json_app_resp()
        params = get_post_json_params()

        if not name == "":
            name = 'world'
        return render_json( {'message': 'Hello, %s!' % name} )

class demo:

    def GET(self, name):
        json_app_resp()

        return render_json( {'message': 'OK', 'action': name} )

    def POST(self, action_str):
        json_app_resp()
        params = get_post_json_params()
        obj_response = controler.start_demo() if action_str == "start" else controler.stop_demo()

        return render_json( obj_response )

class train_control:

    def GET(self, str_params):
        json_app_resp()

        dict_params = { k:v for k, v in [param.split("=") for param in str_params.split("&")] }
        return render_json( dict_params )

    def POST(self, action):
        json_app_resp()
        print(action)
        json_params = get_post_json_params()
        print(json_params)

        obj_response = controler.do( action, json_params )

        return render_json( obj_response )

# End Class Controler


if __name__ == "__main__":
    try:
        web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", 8088))
    except KeyboardInterrupt:
        pass

    print("Server stoped\nBye")


# ## Start this Web Service like
# python .\TrainManagementWebServer.py
# Or
# python .\TrainManagementWebServer.py ElectronicControler.DummyControler

# ## Call this WebService in Powershell like
# $acceptHeader = new-object 'collections.generic.dictionary[string,string]'
# $acceptHeader.Add("Accept","application/json")
# $acceptHeader = @{ "Accept" = "application/json" }
# curl -Headers $acceptHeader "http://otter:8088/trainControl/test=34&tty=toto"
# curl -Headers @{ "Accept" = "application/json" } "http://otter:8088/trainControl/test=34&tty=toto"
