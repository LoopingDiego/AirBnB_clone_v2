#!/usr/bin/env python3
'''
classes:
FileStorage: serialize/deserialize objects to JSON
'''
import json
import os
import uuid
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    ''' FileStorage engine class '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''Returns the dictionary __objects'''

        if cls is None:
            return FileStorage.__objects
        else:
            print_dict = {}
            for key, value in FileStorage.__objects.items():
                name = cls.__name__
                obj = type(value).__name__
                if name == obj:
                    print_dict[key] = value
            return print_dict

    def new(self, obj):
        '''Sets in __objects the obj with key <obj class name>.id '''
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        ''' serializes __objects to the JSON file (path: __file_path) '''
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            new_dict = {key: obj.to_dict() for key, obj in
                        FileStorage.__objects.items()}
            json.dump(new_dict, file)

    def reload(self):
        '''Deserializes the JSON file to __objects.'''
        try:
            if (os.path.isfile(FileStorage.__file_path)):
                with open(FileStorage.__file_path, 'r',
                          encoding='utf-8') as file:
                    objs = json.load(file)
                    for key, value in objs.items():
                        FileStorage.__objects[key] = eval(
                            value['__class__'])(**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''Delete obj from __objects if it’s inside.'''
        try:
            if obj is not None:
                formats = "{}.{}".format(type(obj).__name__, obj.id)
                del FileStorage.__objects[formats]
        except BaseException:
            pass

    def close(self):
        """ deserialize the JSON file to objects """

        self.reload()
