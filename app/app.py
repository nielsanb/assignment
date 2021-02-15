########################################################################################
# imports
import os
import sys
import json
from flask import Flask, render_template, request
from flask_restful import Api, Resource
from yakapplication import Yakbarn, Yak, Yakwebshop
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import yakbarnxml
from yakbarnxml import create_xml_database, add_day_to_xml, change_wool_quantity_xml, change_milk_quantity_xml

########################################################################################
#Initialize a yakbarn instance.
instance_of_barn = Yakbarn("nielsbarn")

#add first yaks as for userstory: later add a addyak button
instance_of_barn.add_yak("Betty-1", 4)
instance_of_barn.add_yak("Betty-2", 8)
instance_of_barn.add_yak("Betty-3", 9)

########################################################################################
#XMLhandler
xml_file_name = 'yakbarndata.xml' 
create_xml_database()

########################################################################################
#Initialize flask application instance.
app = Flask(__name__)

########################################################################################
#Initialize API
rest_server = Api(app)

########################################################################################
#REST SERVICES
class Getinformation(Resource): #Task inheritc from resource class
    def get(self, info_type, day_request, current_day_number=instance_of_barn.current_time):
        tree = ElementTree()
        tree.parse('yakbarndata.xml')
        root = tree.getroot()

        if info_type == 'stock':
            try:
                wst = root[int(day_request)][1][0].attrib['quantity'] # wool_stock
                mst = root[int(day_request)][1][1].attrib['quantity'] # milk_stock
                return {"milk": mst, "skins": wst}, 200
            except:
                return 404

        elif info_type == 'herd':
            try:
                z = {"herd": [{"name": root[int(day_request)][0][i].attrib['name'], "age": root[int(day_request)][0][i].attrib['age']} for i in range(len(root[int(day_request)][0]))]}
                return z, 200
            except:
                return 404

        else:
            return 404


#example: POST@ http://127.0.0.1:5000/yakshop/order?customer=niels&milkorder=1000&woolorder=2
class Postorder(Resource): #Task inheritc from resource class
    def post(self, current_day_number=instance_of_barn.current_time):
        #Get all information I need
        tree = ElementTree() #THIS IS NOT DRY
        tree.parse('yakbarndata.xml')
        root = tree.getroot()
        wst = root[int(current_day_number)-1][1][0].attrib['quantity']
        mst = root[int(current_day_number)-1][1][1].attrib['quantity']
        cust = request.args.get('customer')
        milkorder = request.args.get('milkorder')
        if milkorder is None:
            milkorder = request.form['milkorder']
        woolorder = request.args.get('woolorder')
        if woolorder is None:
            woolorder = request.form['woolorder']

        #logic
        if int(milkorder) <= float(mst) and int(woolorder) <= float(wst):
            #substract from xml stock 2x
            new_stock_milk = float(mst) - int(milkorder)
            new_stock_wool = float(wst) - int(woolorder)
            change_milk_quantity_xml(xml_file_name = xml_file_name, current_day_number = instance_of_barn.current_time, new_stock=new_stock_milk)
            change_wool_quantity_xml(xml_file_name = xml_file_name, current_day_number = instance_of_barn.current_time, new_stock=new_stock_wool)
            #substract from instance_of_barn stock 2x
            instance_of_barn.sell_wool(int(woolorder))
            instance_of_barn.sell_milk(int(milkorder))
            #return order with status 201
            return {"milk": int(milkorder), "skins": int(woolorder)}, 201

        elif int(milkorder) > float(mst) and int(woolorder) <= float(wst): #wool only
            #substract wool from xml stock
            new_stock_wool = float(wst) - int(woolorder)
            change_wool_quantity_xml(xml_file_name = xml_file_name, current_day_number = instance_of_barn.current_time, new_stock=new_stock_wool)
            #substract from instance_of_barn stock
            instance_of_barn.sell_wool(int(woolorder))

            #return order with status 206
            return {"skins": int(woolorder)}, 206

        elif int(milkorder) <= float(mst) and int(woolorder) > float(wst): #wool only
            #substract milk from xml stock
            new_stock_milk = float(mst) - int(milkorder)
            change_milk_quantity_xml(xml_file_name = xml_file_name, current_day_number = instance_of_barn.current_time, new_stock=new_stock_milk)
            #substract from instance_of_barn stock
            instance_of_barn.sell_milk(int(milkorder))
            #return order with status 206
            return {"milk": int(milkorder)}, 206

        else:
            return 404 

#adding services to routes
rest_server.add_resource(Getinformation, "/yakshop/<string:info_type>/<string:day_request>")
rest_server.add_resource(Postorder, "/yakshop/order")

########################################################################################
#WEBPAGES
@app.context_processor
def inject_variables():
    def current_time():
        return instance_of_barn.current_time

    def wool_stock():
        return instance_of_barn.wool_stock

    def milk_stock():
        return instance_of_barn.milk_stock

    def herd():
        instance_of_barn.herd

    return dict(current_time=current_time(), wool_stock=wool_stock(), milk_stock=milk_stock(), herd=herd())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#all available urls
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic')
def basic():
    return render_template('basic.html')

@app.route('/next_day')
def next_day():
    instance_of_barn.next_day()
    add_day_to_xml(day_number=instance_of_barn.current_time, wool_stock=instance_of_barn.wool_stock, milk_stock=instance_of_barn.milk_stock, herd=instance_of_barn.herd)
    return render_template('next_day.html')


""" 
#needs to be resplaced with API call
@app.route('/order_status')
def order_status():
    worder = request.args.get('woolorder')
    morder = request.args.get('milkorder')
    return render_template('order_status.html', worder=worder, morder=morder)
"""

########################################################################################
#running the flask instance.
if __name__ == "__main__":
    app.run(port=5000, debug=True)

