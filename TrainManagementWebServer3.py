#!/usr/bin/python3

# ---------------- Add Path  --------------------------------------------------
import sys
from sys import path as sys_pth
import os.path as pth

local_directory = pth.dirname(pth.abspath(__file__))
import_list = [local_directory
                    , pth.join(local_directory,"Model")
                    , pth.join(local_directory,"Controler")
                    , pth.join(local_directory,"ElectronicComponents")
                    , pth.join(local_directory,"ElectronicModel")
]

for to_import in import_list:
  abs_dir = pth.dirname(pth.abspath(to_import))
  if not abs_dir in sys_pth: sys_pth.append(abs_dir)
# -----------------------------------------------------------------------------

from bottle import route, get, post, request, run, response
import json
from io import TextIOWrapper

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, Content-Length, X-Requested-With, X-CSRF-Token'

dynamic_controler_name = sys.argv[1] if len(sys.argv) > 1 else "ElectronicControler.DummyControler"

dynamic_controler = __import__(dynamic_controler_name, fromlist=["*"])

# Create the real controler
controler = dynamic_controler.Controler()

print("Controler name loaded: %s" % dynamic_controler.__name__)
print("Controler class name: %s" % type(controler))

def json_app_rqt():
    # about request
    request.accept = 'application/json, text/plain; charset=utf-8'

def json_app_resp():
    # about response
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Content-Type'] = 'application/json; charset=utf-8'

def json_app():
    json_app_rqt()
    json_app_resp()

def get_json_request(rqt):
    with TextIOWrapper(rqt.body, encoding = "UTF-8") as json_wrap:
        json_text = ''.join(json_wrap.readlines())
        json_data = json.loads(json_text)
        return json_data


if __name__ == "__main__":

    json_app_rqt()

    @get("/")
    def ui():
        main_page = local_directory + "/UI/TrainManagement.html"
        response.content_type = 'text/html'
        html_page = "Page under construction ..."
        # try:
        with open(main_page, 'r') as fic:
            html_page = ''.join(fic.readlines())
        # finally:
        return html_page

    # @route("/test/:control/:value", METHOD="GET")
    @get("/test/:control/:value")
    def test(control, value):
        respObj = {'message': 'test ok with control %s and value %s' % (control, value) }
        return (respObj)

    @get("/train_control/:control/:params")
    def train_control(control, params={}):
        return controler.do( control, params )

    @post("/train_control/:control")
    def do_train_control(control):
        json_app_resp()

        data = get_json_request(request)
        print(data)

        return controler.do( control, data )

    @get("/start_demo")
    def start_demo():
        return controler.start_demo()

    @get("/stop_demo")
    def start_demo():
        return controler.stop_demo()
    run(host='0.0.0.0', port=8088)


# if not controler.contains_function(control_name):
  # print("Status: 404 Not Found")
  # print("")
  # exit()

# ## Start this Web Service like and pass the ElectronicControler
# python .\TrainManagementWebServer3.py ElectronicControler.DummyControler

# ## Call this WebService in Powershell like
# $acceptHeader = new-object 'collections.generic.dictionary[string,string]'
# $acceptHeader.Add("Accept","application/json")
# $acceptHeader = @{ "Accept" = "application/json" }
# curl -Headers $acceptHeader "http://otter:8088/trainControl/test=34&tty=toto"

# curl -Headers @{ "Accept" = "application/json" } "http://otter:8088/test/ct1/val1"
# curl -Headers @{ "Accept" = "application/json" } "http://otter:8088/train_control/get_status/val1"