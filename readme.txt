LogicSim - Paolo Mura - 2020


     --Background & Setup--

LogicSim is a logic gate simulator developed in Python using Pygame. The project includes a data folder that contains the sprite images for logic gates, inputs, outputs and the screen. It also includes several Python files that contain the classes for object behaviour.

Before running LogicSim, make sure you have the following:

Python version 3.6
PyGame
NumPy

To install Python 3.6, go to www.Python.org and then navigate to Downloads->Releases. Download the latest version of 3.6 with the "Add python 3.6 to PATH" option selected if given the chance. Once downloaded, find the folder on your computer and make sure it contains IDLE.

To install Pygame, go to www.Pygame.org and then navigate to Getting Started. Follow the instructions for your operating system (mac/windows). You will have to type a pip command into the Terminal (mac) or Command Line (windows) application and then press enter.

To install NumPy, go to www.NumPy.org and then navigate to Install. Follow the instructions there or simply type in the following command into the Command Line and press enter:

pip install numpy

To run LogicSim, open the logicsim.py file in Python's IDLE application. Go to the menu and then select Run->Run Module or press F5 (fn+F5 on mac) on the keyboard.



     --How to Play--

There are six logic gates in the menu at the top of the screen. You can click and drag a logic gate from the menu into the 'drop zone' and click again to 'drop' it.

Click on a logic gate to select it. If you then click on an input/output/another logic gate, a wire will be connected between them. You can make as many outbound connections as you want but there can only be one inbound connection per terminal. To move a selected logic gate, press the space bar and then click when you want to drop it. To delete a selected logic gate, press delete/backspace.

To change the value of an input, select it and then press the space bar to change it between True (green) and False (red).

When an output is connected to the circuit it should automatically change its value depending on the logic flow. Wires should also change colour automatically depending on the logic flow in the circuit.

To display the boolean expression for the logic circuit you have created, select an output and then press the space bar.

Extra Note: Unlike logic gates, inputs and outputs don't show when they're selected. Sometimes it's best to double click them when you want to select them just to be sure.
