from flask import Flask, request, Response, jsonify
from flask_restful import Resource,Api
from flask_cors import CORS
from subprocess import check_output
from time import sleep
import logging

import json

from main import main

app = Flask(__name__)
api = Api(app)
CORS(app)

class Available(Resource):
    def get(self):
        status_code = Response(status=200, mimetype='application/json')
        return status_code

class Recipe(Resource):
    def post(self):
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
        return jsonify(status)

class WaterStatus(Resource):
    def get(self):
        status = main.getWaterStatus()
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
        if confirm == "Cooking":
            main.StartCooking()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if confirm == "Boiling":
            main.SetIsBoilingPointReached()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code


class Start(Resource):
    def post(self,command,value):
        if command == 'AgitatorInterval':
            print(request.json)
            main.StartMixer(request.json)
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
    def get(self, command, value):
        if command == "start":
            result = main.go()
            if result != "OK":
                status_code = Response(status=500, mimetype='application/json')
            else:
                status_code = Response(status=200, mimetype='application/json')
            return status_code
        if command == "Temperatur":
            d=main.getTemp()
            js=json.dumps(d)
            resp=Response(js, status = 200, mimetype = 'application/json')
            return resp
        if command == "Speed":
            main.setSpeed(value)
            status_code = Response({"OK"},status=200, mimetype='application/json')
            return status_code
        if command == "Frq":
            main.setFrq(value)
            status_code = Response({"OK"},status=200, mimetype='application/json')
            return status_code
        if command == "Stop":
            main.StopMixer()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "Start":
            main.StartMixer(value)
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "StartBrewing":
            main.go()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "TurnOn":
            main.turnON_HeatingSystem()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "TurnOff":
            main.turnOFF_HeatingSystem()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "StartCooking":
            main.StartCooking()
            status_code = Response({"OK"}, status=200, mimetype='application/json')
            return status_code
        if command == "BoilingPointReached":
            main.SetIsBoilingPointReached()
            status_code=Response({"OK"}, status = 200, mimetype = 'application/json')
            return status_code

        if command =="FillWaterAutomatic":
            main.fillWater(value)
            status_code=Response({"OK"}, status = 200, mimetype = 'application/json')
            return status_code

        if command =="FillWaterManuel":
            main.fillWaterManuel()
            status_code=Response({"OK"}, status = 200, mimetype = 'application/json')
            return status_code
        if command =="FillWaterStop":
            main.fillWaterStop()
            status_code=Response({"OK"}, status = 200, mimetype = 'application/json')
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
api.add_resource(Start, '/Command/<string:command>:<string:value>')
api.add_resource(Recipe, '/Recipe/')
api.add_resource(Status, '/Status/')
api.add_resource(WaterStatus, '/WaterStatus/')
api.add_resource(Available, '/')
api.add_resource(Extended, '/Extended/<string:time>')
api.add_resource(Ferment, '/Ferment/')


def initializing_network() :
    while True :
        try :
            result=check_output(['hostname', '-I']).decode('utf-8').strip()
            if ('192.168.178.37' in result) :
                return True
        except :
            pass
        sleep(5)


if __name__ == '__main__':
    log=logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    initializing_network()
    main=main()
    app.run(host='192.168.178.37',debug=True)


