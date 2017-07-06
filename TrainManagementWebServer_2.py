#!/usr/bin/python3

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# ex in web browser : http://localhost:8888/TrainManagement.py?control=get_help&functionName=Switch&functionValue=Off

import web
import json
import mimerender

mimerender = mimerender.WebPyMimeRender()

render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message

urls = (
    '/home/(.*)', 'home_control',
    '/trainControl/(.*)', 'train_control',
    '/demo', 'demo'
)
app = web.application(urls, globals())

class home_control:
    @mimerender(
        default = 'html',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def GET(self, name):
        if not name: 
            name = 'world'
        return {'message': 'Hello, %s!' % name}

class demo:
    @mimerender(
        default = 'html',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def GET(self, name):

        return {'message': 'OK'}

class train_control:
    @mimerender(
        default = 'html',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def GET(self, str_params):
        # dict_params = dict([(k, v) for k, v in [param.split("=") for param in str_params.split("&")]])
        dict_params = { k:v for k, v in [param.split("=") for param in str_params.split("&")] }
        # return { 'message': json.dumps(dict_params) }
        return dict_params

if __name__ == "__main__":
    try:
        app.run()
    except KeyboardInterrupt:
        pass

    print("Server stoped\nBye")


# ## Start this Web Service like
# python .\WSRestTestMimeRender2.py 127.0.0.1:8088

# ## Call this WebService in Powershell like
# $acceptHeader = new-object 'collections.generic.dictionary[string,string]'
# $acceptHeader.Add("Accept","application/json")
# $acceptHeader = @{ "Accept" = "application/json" }
# curl -Headers $acceptHeader "http://otter:8088/trainControl/test=34&tty=toto"
# curl -Headers @{ "Accept" = "application/json" } "http://otter:8088/trainControl/test=34&tty=toto"
