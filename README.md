# Cura Launcher for the MakerSpace Heidelberg
A custom Launcher Script that performs a modifications on the Cura [slicing](http://reprap.org/wiki/Slicer) GUI
and launches it.

# Challenge
[Ultimaker](https://ultimaker.com/en/products/cura-software) Cura is a very powerful Open Source slicing tool. But
there were two minor details, the [Makerspace Heidelberg](https://wiki.heidelberg-makerspace.de/wiki/Main_Page)
wanted to be improved/customized:
  * the GUI displays the printing cost as a number without currency, making it hard to recognize it for what it is
  * for custom 3d printers, no printing bed is displayed in the 3d view. It is not obvious which one of the many
    printers is currently selected.

In order to make the code fixes sustainable and maintainable, the following constraints were given:
  * the patch needs to be easily applicable
  * turning it off and on has to be possible
  * the code should be well modifiable
  * ideally, the patch works with future versions of Cura.

# Approach

## Finding the Relevant Code
First, the right pieces of code in the Cura GUI needed to be identified. The Cura GUI is an extensive software project
written in Python. It depends on an even bigger C/C++ code base as slicing engine. Understanding the projects' structure
in its entirety takes time. Luckily, it suffices to find the pieces of code that need improvement. Linux offers the
right tool for the job in form of grep. [**grep**](https://en.wikipedia.org/wiki/Grep) allows to search the contents
of text files. To save the reader's time, it will only be shown what *should* have been searched for. To find the method
returning the cost (string), it's a good idea to search for a method definition ending with "cost":
```shell
grep -ri "cost(" .
```

"-ri" enables recursive search and ignores upper and lower cases on characters. As it turns out, both `Cura.util.gcodeInterpreter` and the `Cura.util.sliceEngine` module contain a member method
which returns a cost string. It appears only latter is printed to screen.

To find where the printer bed models are loaded, just search for the `*.stl` file ending:
```shell
grep -ri "\.stl" .
```
`Cura.gui.sceneView` is the only module loading printer bed models.

## Modifying the Code

# Results
