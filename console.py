# console.py
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User

class HBNBCommand(cmd.Cmd):
    """HBNBCommand class for the command interpreter"""
    prompt = '(hbnb) '
    classes = {"BaseModel": BaseModel, "User": User}

    def do_create(self, args):
        """Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id"""
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            new_instance = self.classes[args[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id"""
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id (save the change into the JSON file)"""
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
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

    def do_all(self, args):
        """Prints all string representation of all instances based or not on the class name"""
        args = args.split()
        if len(args) > 0 and args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in storage.all().items() if not args or k.split('.')[0] == args[0]])

    def do_update(self, args):
        """Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file)"""
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key not in storage.all():
                print("** no instance found **")
            elif len(args) == 2:
                print("** attribute name missing **")
            elif len(args) == 3:
                print("** value missing **")
            else:
                setattr(storage.all()[key], args[2], args[3])
                storage.all()[key].save()

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
