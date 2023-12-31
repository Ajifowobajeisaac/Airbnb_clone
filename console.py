#!/usr/bin/python3
"""
This module contains the entry point of the command interpreter.

The command interpreter handles all the user input and interacts with the
storage and model classes.
"""

import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import ast


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class for the command interpreter"""
    prompt = '(hbnb) '
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review,
        }

    def default(self, line):
        """
        Method called on an input line when the command prefix is not
        recognized
        """

        match = re.search(r"^(\w+)\.(\w+)\((.*)\)$", line)
        if match:
            class_name = match.group(1)
            method_name = match.group(2)
            args = match.group(3)
            if class_name in self.__classes:
                if method_name == "all":
                    self.do_all(class_name)
                elif method_name == "count":
                    self.do_count(class_name)
                elif method_name == "show":
                    self.do_show(class_name + " " + args)
                elif method_name == "destroy":
                    self.do_destroy(class_name + " " + args)
                elif method_name == "update":
                    dict_arg_match = re.search(r"{.*}", args)
                    if dict_arg_match:
                        # Process dictionary argument
                        dict_arg = dict_arg_match.group(0)
                        # Extract the rest of the arguments
                        remaining_args = args.replace(dict_arg, '').split(',')
                        remaining_args = [arg.strip() for arg in remaining_args
                                          if arg.strip()]
                        id_arg = remaining_args[0].strip('"')
                        self.do_update(f"{class_name} {id_arg} {dict_arg}")
                    else:
                        # Use regex to match either a sequence of non-space
                        # characters or a sequence of characters
                        # within double quotes
                        args = re.findall(r'[^,\s]+|"[^"]*"', args)
                        # Remove quotes from arguments
                        args = [arg.replace('"', '') for arg in args]
                        # Call do_update with the correctly parsed arguments
                        if len(args) == 3:
                            self.do_update(
                                f"{class_name} {args[0]} {args[1]} {args[2]}")
                        elif len(args) == 2:
                            if isinstance(args[1], dict):
                                for key, value in args[1].items():
                                    self.do_update(
                                        f"""
                                        {class_name}
                                        {args[0]}
                                        {key}
                                        {value}
                                        """)
                            else:
                                self.do_update(
                                    f"{class_name} {args[0]} {args[1]}")
                        else:
                            print("** wrong number of arguments **")
        else:
            print("*** Unknown syntax: {}".format(line))

    def do_count(self, args):
        """Retrieves the number of instances of a class"""
        try:
            args = args.split()
            if len(args) == 0:
                print("** class name missing **")
            elif args[0] not in self.__classes:
                print("** class doesn't exist **")
            else:
                print(len([v for k, v in storage.all().items() if
                           k.split('.')[0] == args[0]]))
        except Exception as e:
            pass

    def do_all(self, args):
        """Prints all string representation of all instances based or not on
        the class name"""

        try:
            args = args.split()
            if len(args) > 0 and args[0] not in self.__classes:
                print("** class doesn't exist **")
            else:
                print(
                    [str(v) for k, v in storage.all().items() if not
                        args or k.split('.')[0] == args[0]]
                    )
        except Exception as e:
            pass

    def do_create(self, args):
        """Creates a new instance of BaseModel, saves it (to the JSON file) and
         prints the id"""
        try:
            args = args.split()
            if len(args) == 0:
                print("** class name missing **")
            elif args[0] not in self.__classes:
                print("** class doesn't exist **")
            else:
                new_instance = self.__classes[args[0]]()
                new_instance.save()
                print(new_instance.id)
        except Exception as e:
            pass

    def do_show(self, args):
        """Prints the string representation of an instance based on the class
         name and id"""
        try:
            args = args.split()
            if len(args) == 0:
                print("** class name missing **")
            elif args[0] not in self.__classes:
                print("** class doesn't exist **")
            elif len(args) == 1:
                print("** instance id missing **")
            else:
                key = args[0] + "." + args[1]
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])
        except Exception as e:
            pass

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id (save the change
          into the JSON file)"""
        try:
            args = args.split()
            if len(args) == 0:
                print("** class name missing **")
            elif args[0] not in self.__classes:
                print("** class doesn't exist **")
            elif len(args) == 1:
                print("** instance id missing **")
            else:
                key = args[0] + "." + args[1]
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()
        except Exception as e:
            pass

    def do_update(self, args):
        """Updates an instance based on the class name and id by
          adding or updating attribute (save the change into the JSON file)"""
        try:
            args = re.split(r'\s(?![^{}]*\})', args)
            if len(args) == 0:
                print("** class name missing **")
            elif args[0] not in self.__classes:
                print("** class doesn't exist **")
            elif len(args) == 1:
                print("** instance id missing **")
            else:
                key = args[0] + "." + args[1]
                if key not in storage.all():
                    print("** no instance found **")
                elif len(args) == 2:
                    print("** attribute name missing **")
                else:
                    if args[2].startswith('{') and args[2].endswith('}'):
                        # Handle dictionary argument
                        update_dict = ast.literal_eval(args[2])
                    for attr_name, value in update_dict.items():
                        if attr_name in ['id', 'created_at', 'updated_at']:
                            print("** attribute can't be updated **")
                        else:
                            attr_type = type(
                                getattr(storage.all()[key], attr_name, ""))
                            if attr_type in [int, float, str]:
                                setattr(
                                    storage.all()[key],
                                    attr_name,
                                    attr_type(value))
                                storage.all()[key].save()
                            else:
                                print("** attribute type not allowed **")
                    if args[2] in ['id', 'created_at', 'updated_at']:
                        print("** attribute can't be updated **")
                    else:
                        attr_type = type(
                            getattr(storage.all()[key], args[2], ""))
                        if attr_type in [int, float, str]:
                            setattr(
                                storage.all()[key], args[2], attr_type(args[3])
                                )
                            storage.all()[key].save()
                        else:
                            print("** attribute type not allowed **")
        except Exception as e:
            pass

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
