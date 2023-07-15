from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
CORS(app)
api = Api(app)

def getindex():

    option = ""
    for i in pages:
        option += "<button onclick='openpage(\""+i+"\")'>"+i+"</button><br>"
    index = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <title>test</title>
    </head>
    <body>
        <!DOCTYPE html>
        <html>
        <head>
            <title>Form Submission</title>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        </head>
        <body>
            <form id="myForm">
                <label for="code">Code:</label>
                <input type="text" id="code" name="code" required>
                <br>
                <label for="route">Route:</label>
                <input type="text" id="route" name="route" required>
                <br>
                <input type="submit" value="Submit">
            </form>
            <div>'''+option+'''
            </div>
        
            <script>
                $(document).ready(function() {
                    $('#myForm').submit(function(event) {
                        event.preventDefault();  // Prevent the default form submission
                        var form_data = $(this).serializeArray();  // Serialize the form data
                        $.ajax({
                            url: 'http://127.0.0.1:5000/',  // Flask API endpoint
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(form_data),
                            success: function(response) {
                                if (response.success == 1) {
                                    openpage(response.page)
                                }
                                // Handle the success response here
                            },
                            error: function(error) {
                                console.error(error);
                                // Handle the error response here
                            }
                        });
                    });
                });
                function openpage(route) {
                    $.ajax({
                        url: 'http://127.0.0.1:5000/' + route,  // Flask API endpoint
                        type: 'GET',
                        success: function(response) {
                            if (response.success == 1) {
                                document.body.innerHTML = response.data
                            }
                            // Handle the success response here
                        },
                        error: function(error) {
                            console.error(error);
                            // Handle the error response here
                        }
                    });
                }
            </script>
        </body>
        </html>
        
    </body>
    </html>
    '''
    return index

pages = {}

class HelloWorld(Resource):
    def get(self):
        response = {"code": getindex()}
        return jsonify(response)
    
    def post(self):
        data = request.get_json()
        if data[1]["value"] not in pages:
            pages[data[1]["value"]] = {}
        user_dict = pages[data[1]["value"]]
        if user_dict:
            user_dict[data[2]["value"]] = data[0]["value"]
        else:
            pages[data[1]["value"]] = {data[2]["value"]:data[0]["value"]}


        return jsonify({"success":True, "user":data[1]["value"], "page":data[2]["value"]})
    
class Route(Resource):
    def get(self, route, user):
        if user in pages:
            user_dict = pages[user]
            if route in user_dict:
                return jsonify({"success": True, "data": user_dict[route]})
            else:
                return jsonify({"success": False, "data": "404"})
        else:
            return jsonify({"success": False, "data": "404"})
        
class Index(Resource):
    def get(self):
        return getindex()

api.add_resource(HelloWorld, '/')
api.add_resource(Route, '/<user>/<route>')
api.add_resource(Index, '/index')


if __name__ == '__main__':
    app.run(debug=True)