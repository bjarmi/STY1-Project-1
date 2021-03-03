import sys
from Manager import Manager


def read_file_commands(file_name, first_in):
    try:
        with open(file_name) as file:
            for line in file:
                command = line.split()
                if command:
                    calls(command, first_in)
                first_in = False

    except FileNotFoundError:
        print(f"File {file_name} not found.")


def read_shell_commands():
    call: str = ""
    while not call == "q":
        call = input("> ")
        calls(call, True)


def calls(command, first_in):
    try:
        if command[0] == "cr":
            out.write(f"{manager.create(int(command[1]))} ")
        elif command[0] == "de":
            out.write(f"{manager.destroy(int(command[1]))} ")
        elif command[0] == "rq":
            out.write(f"{manager.request(int(command[1]))} ")
        elif command[0] == "rl":
            out.write(f"{manager.release(int(command[1]))} ")
        elif command[0] == "to":
            out.write(f"{manager.timeout()} ")
        elif command[0] == "in":
            if not first_in:
                out.write("\n")
            out.write(f"{manager.init()} ")
        else:
            raise IndexError("Command not available.")
    except IndexError as error:
        print(f"Invalid command.\n {error}")
        out.write(f"{-1} ")


if __name__ == '__main__':
    manager = Manager()
    out = open("output.txt", "w")
    try:
        read_file_commands(sys.argv[1], True)
    except IndexError:
        read_shell_commands()
    out.close()
