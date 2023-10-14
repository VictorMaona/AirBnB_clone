#!/usr/bin/python3
"""Establishes AirBnB clone project. """
import cmd
import re

from models.amenity import Amenity
from models.base_model import BaseModel
from models.state import State
from models.user import User
from models.city import City
from models import storage
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """The class `HBNBCommand` defines the command interpreter. """

    prompt = "(hbnb) "
    classes = [BaseModel, User, State, City, Amenity, Place, Review]
    class_dict = dict()
    for c in classes:
        class_dict[c.__name__] = c

    def default(self, line):
        """ Check (<args>)<class>.<command> syntax.

        <args> can be empty, <id> only, <id> <name> <value>, or <id> <dict>.

        """
        alt_syntax_cmds = {'all', 'count', 'show', 'destroy', 'update'}
        if re.fullmatch('^\w{4,9}\.\w{3,7}\(.*\)$', line) is None:
            return
        for cmd in alt_syntax_cmds:
            if cmd in line:
                # params tuple with ('<class>', '<cmd>', '(<args>)')
                params = list(line.partition(cmd))
                params[0] = params[0].strip('.')
                # '(<args>)' becomes list of strings
                params[2] = params[2].strip('()')
                if '{' in params[2] and '}' in params[2]:
                    params[2] = params[2].split(', ', 1)
                else:
                    params[2] = params[2].split(', ')
                for i, arg in enumerate(params[2]):
                    params[2][i] = arg.strip('"')
                if params[1] == 'all':
                    self.do_all(params[0])
                elif params[1] == 'count':
                    if params[0] not in HBNBCommand().class_dict.keys():
                        print("** class doesn't exist **")
                    else:
                        print(len([v for v in storage.all().values()
                                   if v.__class__.__name__ == params[0]]))
                elif params[1] == 'show':
                    self.do_show(params[0] + ' ' + ' '.join(params[2]))
                elif params[1] == 'destroy':
                    self.do_destroy(params[0] + ' ' + ' '.join(params[2]))
                elif params[1] == 'update':
                    if '{' in params[2] and '}' in params[2]:
                        dict_arg = eval(params[2][1])
                        if type(dict_arg) == dict:
                            for key, value in dict_arg.items():
                                # <class> <id> <attr name> <attr value>
                                update_line = ' '.join((params[0],
                                                        params[2][0],
                                                        key, str(value)))
                                self.do_update(update_line)
                    else:
                        update_line = (params[0] + ' ' +
                                       ' '.join(params[2]))
                        self.do_update(update_line)

    def do_quit(self, line):
        """To exit the program use the Quit command."""
        return True

    def do_EOF(self, line):
        """To exit the application use EOF"""
        print()
        return True

    def emptyline(self):
        """Lines that are blank are disregarded."""
        pass

    def do_create(self, line):
        """Creates new BaseModel instance saves it and outputs id."""
        args = line.split()

        if len(args) == 0:
            print("** class name missing **")

        elif args[0] not in HBNBCommand().class_dict.keys():
            print("** class doesn't exist **")

        else:
            new = self.class_dict[args[0]]()
            storage.save()
            print(new.id)

    def do_show(self, line):
        """String representation of instance is printed."""
        args = line.split()

        if len(args) == 0:
            print("** class name missing **")

        elif args[0] not in HBNBCommand().class_dict.keys():
            print("** class doesn't exist **")

        elif len(args) == 1:
            print("** instance id missing **")

        else:
            all_keys = storage.all()
            key = args[0] + "." + args[1]

            if key not in all_keys.keys():
                print("** no instance found **")

            else:
                print(all_keys[key])

    def do_destroy(self, line):
        """Removes instance"""
        args = line.split()

        if len(args) == 0:
            print("** class name missing **")

        elif args[0] not in HBNBCommand().class_dict.keys():
            print("** class doesn't exist **")

        elif len(args) == 1:
            print("** instance id missing **")

        else:
            all_keys = storage.all()
            key = args[0] + "." + args[1]

            if key not in all_keys.keys():
                print("** no instance found **")

            else:
                del all_keys[key]
                storage.save()

    def do_all(self, line):
        """Prints all string representations based on class name or not."""
        args = line.split()

        if len(args) == 0:
            print([str(v) for v in storage.all().values()])

        elif args[0] not in HBNBCommand().class_dict.keys():
            print("** class doesn't exist **")

        else:
            print([str(v) for v in storage.all().values()
                  if v.__class__.__name__ == args[0]])

    def do_update(self, line):
        """Adds or changes characteristics to an instance."""
        args = line.split()
        int_attrs = ("number_rooms", "number_bathrooms",
                     "max_guest", "price_by_night")
        flt_attrs = ("latitude", "longitude")

        if (len(args) == 0):
            print("** class name missing **")

        elif args[0] not in HBNBCommand().class_dict.keys():
            print("** class doesn't exist **")

        elif len(args) == 1:
            print("** instance id missing **")

        else:
            all_keys = storage.all()
            key = args[0] + "." + args[1]

            if key not in all_keys.keys():
                print("** no instance found **")

            else:
                if len(args) == 2:
                    print("** attribute name missing **")

                elif len(args) == 3:
                    print("** value missing **")

                else:
                    args[3] = args[3].strip('"')
                    if args[2] in int_attrs:
                        value = int(args[3])
                    elif args[2] in flt_attrs:
                        value = float(args[3])
                    # currently no check or error message for wrong format --
                    # deafults to string; int() or float() fail crashes
                    else:
                        value = args[3]
                    all_keys[key].__dict__[args[2]] = value
                    storage.save()

if __name__ == "__main__":
        HBNBCommand().cmdloop()
