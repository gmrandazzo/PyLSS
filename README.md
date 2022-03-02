# PyLSS

PyLSS [1] is a python package useful to calculate linear solvent strength parameters [2]
in Liquid Chromatography.

PyLSS is able to compute:
  - LSS parameters (log kw and S)
  - Build and plot chromatograms from experimental/predicted retention times
  - A graphical user interface facilitate you to make models and easly
    estimate LSS parameters

![ScreenShot](https://github.com/gmrandazzo/PyLSS/blob/master/gui/pylssgui.png)

PyLSS include a personalised algorithm to optimise and calculate the LSS parameters
in a fast manner.

References:
----------
[1] Prediction of retention time in reversed-phase liquid chromatography as a tool for steroid identification
G.M. Randazzo, D. Tonoli, S. Hambye, D. Guillarme, F. Jeanneret, A. Nurisso, L. Goracci, J. Boccard, Prof. S. Rudaz
Analytica Chimica Acta 2016
doi:10.1016/j.aca.2016.02.014

[2] High-Performance Gradient Elution:
The Practical Application of the Linear-Solvent-Strength Model
Lloyd R. Snyder, John W. Dolan
ISBN: 978-0-471-70646-5
496 pages
January 2007

License
============

PyLSS is distributed under LGPLv3 license, this means that:

- you can use this library where you want doing what you want.
- you can modify this library and commit changes.
- you can not use this library inside a commercial software.

To know more in details how the licens work please read the file "LICENSE" or
go to "http://www.gnu.org/licenses/lgpl-3.0.html"

PyLSS is currently property of Giuseppe Marco Randazzo which is also the
current package maintainer.

Voluntary contributions are welcome.


Dependencies
============

The required dependencies to use PyLSS are:

- python version 2 or 3
- numpy
- scipy
- matplotlib
- PyQt5 to use the GUI

Install
=======

To install for all users on Unix/Linux/OSX/Windows:

  python setup.py install

To use the GUI:
  - install PyQt5: pip install pyqt5
  - run python3 pylss-guy.py to visualize the GUI.

How to use the command line?
=======

See the examples directory. Inside you can find a script runtest.sh which
show a simple use of the library to calculate the LSS parameters.

If you check also at the bin directory you can find some usefull executables
to run your calculations.


Development
===========
GIT
---

You can check the latest sources with the command::

  git clone https://github.com/gmrandazzo/PyLSS.git


Contributing
------------

To contribute you can fork the project, or if you have already forked the project
update to the latest version of PyLSS, make the changes and open a Pull Request.

However some recomendation before open a Pull Request:
  * Be sure that your code it's working.
  * Use pylint to check your code. The Global Evaluation rate must be >= 9.0
  * Comment your code with Parameters, Attribute, Return, Notes and References.
  * An example is necessary.

Probabily your code will be integrated but some quality and goals have to keep in mind.
