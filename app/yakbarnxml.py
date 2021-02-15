import os
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

xml_file_name = 'yakbarndata.xml' 

def create_xml_database(xml_file_name = xml_file_name):
    create_file = open(xml_file_name, 'w')

    root = Element('yakbarndata')
    tree = ElementTree(root)

    day = Element('day')
    day.set('id','0')
    root.append(day)

    hd = Element('herd')
    day.append(hd)

    stock = Element('stock')
    day.append(stock)

    tree.write(open(xml_file_name, 'wb'))

def add_day_to_xml(xml_file_name = xml_file_name, day_number = 0, wool_stock=0, milk_stock=0, herd=[]): #change this to the number of the day!
    #grab the file
    tree = ElementTree()
    tree.parse('yakbarndata.xml')
    root = tree.getroot()

    #add a new day with the herd and the stock #this is not DRY.
    day = Element('day')
    day.set('id',str(day_number))

    hd = Element('herd')
    day.append(hd)

    stock = Element('stock')
    day.append(stock)

    #add the labyaks to the herd
    for i in range(len(herd)):
        labyak = Element('labyak')
        labyak.set('name', str(herd[i].name))
        labyak.set('age', str(herd[i].age_in_years))
        hd.append(labyak)

    #add the stocks to the stock element
    ws = Element('wool_stock')
    ws.set('quantity',str(wool_stock))
    stock.append(ws)

    ms = Element('milk_stock')
    ms.set('quantity',str(milk_stock))
    stock.append(ms)

    #add it to the root
    root.append(day)

    #write it to the file
    tree.write(open(xml_file_name, 'wb'))

def change_wool_quantity_xml(xml_file_name = xml_file_name, current_day_number = 0, new_stock=0):
    tree = ElementTree()
    tree.parse('yakbarndata.xml')
    root = tree.getroot()
    root[int(current_day_number)][1][0].set('quantity', str(new_stock))
    tree.write(open('yakbarndata.xml', 'wb'))

def change_milk_quantity_xml(xml_file_name = xml_file_name, current_day_number = 0, new_stock=0):
    tree = ElementTree()
    tree.parse('yakbarndata.xml')
    root = tree.getroot()
    root[int(current_day_number)][1][1].set('quantity', str(new_stock))
    tree.write(open('yakbarndata.xml', 'wb'))

def get_daily_info():
    tree = ElementTree()
    tree.parse('yakbarndata.xml')
    root = tree.getroot()

change_wool_quantity_xml, change_milk_quantity_xml
"""
    root[day][0] -> herd
    root[1][0][0] -> labyak1
    root[1][0][0].attrib['name']
    root[1][0][0].attrib['age']
    root[day][1] -> stock 
    root[day][1][0] -> wool_stock
    root[day][1][1] -> milk_stock
    root[day][1][0].attrib['quantity'] -> wool_stock_of_the_day #as a string
    root[day][1][1].attrib['quantity'] -> milk_stock_of_the_day #as a string
"""