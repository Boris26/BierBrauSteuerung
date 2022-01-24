from flask import Flask, request, Response, jsonify
from flask_restful import Resource,Api
import json

from main import main

app = Flask(__name__)
api = Api(app)

class Available(Resource):
    def get(self):
        status_code = Response(status=200, mimetype='application/json')
        return status_code

class Recipe(Resource):
    def put(self):
        main.addProcedure(request.json)
        status_code =  Response(status=201, mimetype='application/json')
        return status_code
class Extended(Resource):
    def put(self,time):
        main.extendedLastRast(time)
        status_code = Response(status=201, mimetype='application/json')
        return status_code


class Status(Resource):
    def get(self):
        status = main.getStatus()
        return status
class Temperature(Resource):
    def put(self,alter):
        main.addProcedure(request.json)
        status_code =  Response(status=201, mimetype='application/json')
        return status_code
    def get(self,alter):
        return main.getTemp()


class Type(Resource):
    def get(self):
        return main.getType()

class Confirm(Resource):
    def get(self,confirm):
        if confirm == "Iodine":
            main.confirmIodineTest()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if confirm == "Mashup":
            main.confirmMashup()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code


class Start(Resource):
    def get(self,command,speed):
        if command == "start":
            result = main.go()
            if result != "OK":
                status_code = Response(status=500, mimetype='application/json')
            else:
                status_code = Response(status=200, mimetype='application/json')
            return status_code

        if command == "Speed":
            main.setSpeed(speed)
            status_code = Response({"OK"},status=200, mimetype='application/json')
            return status_code
        if command == "Frq":
            main.setFrq(speed)
            status_code = Response({"OK"},status=200, mimetype='application/json')
            return status_code
        if command == "Stop":
            main.Stop()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "Start":
            main.Start(speed)
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "StartBrewing":
            main.go()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "TurnOn":
            main.turnON()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "TurnOff":
            main.turnOFF()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "StartCooking":
            main.StartCooking()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code

class Ferment(Resource):
    def put(self):
        return main.startFermentMeasur()
    def get(self):
        d = main.getPressure()
        js =json.dumps(d)
        resp = Response(js, status=200, mimetype='application/json')
        return resp



class speicher():
    def speichern(self,alter):
        self.s = alter
    def get(self):
        return self.s


api.add_resource(Temperature, '/temperatur/<string:alter>')
api.add_resource(Confirm, '/Confirm/<string:confirm>')

api.add_resource(Type, '/type/')
api.add_resource(Start, '/Command/<string:command>:<string:speed>')
api.add_resource(Recipe, '/Recipe/')
api.add_resource(Status, '/Status/')
api.add_resource(Available, '/')
api.add_resource(Extended, '/Extended/<string:time>')
api.add_resource(Ferment, '/Ferment/')




if __name__ == '__main__':
    main = main()
    app.run(host='192.168.178.59',debug=False)

