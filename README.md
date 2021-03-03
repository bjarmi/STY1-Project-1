# STY1-Project-1
This project develops a simple process and resource manager. 
In the most basic form, the manager supports the creation and 
management of the data structures to represent processes and 
resources. The manager also provides the basic operations invoked 
by processes to create and destroy processes, and to request and 
release resources. A manually invoked timeout function mimics the 
behavior of preemptive scheduling.

The manager can be tested using a presentation shell developed as
part of the project. This allows the testing of the manager without
running any actual processes and without having to access the
physical CPU or other hardware components. Instead, the presentation
shell plays the role of both the currently running process and the
hardware by accepting commands typed in by the user and invoking the
corresponding functions of the manager.

##### Python version 3.9

##### Running program in terminal/CMD:

    To read in a file:
        python path_to/main.py {file_name}
        
    To use shell inputs:
        python path_to/main.py