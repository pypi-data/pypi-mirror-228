# Python Tools for Modelling, Uncertainty, and Data Analysis for Engineers

This package contains a set of tools that are used to support the MUDE course given at Civil Engineering, TU Delft, for first-year MSc students.
It contains a set of tools and dependencies that are used in the course contents themselves.
In addition, this package has several debugging tools that can be used by students and staff to check that their installation is compatible with the requirements for the course.

## Common functionality

The top-level mude module, obtained by `import mude` contains common functionality you can use across assignments. An example of this is [environment checking](#environment-checking).

### Environment checking

The mude package allows you to check its execution environment to determine that students have the appropriate dependencies and software installed. The desired environment can be configured through a `requirements.toml` file (example found under the `week1` submodule). Example TOML file:

```
[environment]
min_python="3.11"
min_conda="23.5.0"

[requirement.numpy]
min_version="1.24.3"

[requirement.matplotlib]
min_version="3.7.1"

[requirement.mude]
min_version="0.1.0"
```

The `environment` heading contains info about the minimum required python version (`min_python`) and minimum required conda version (`min_conda`). The checker will also warn students if the code is not executed inside a conda environment, even if conda is installed. Finally, all `[requirement.package]` headings correspond to the `package`s you want students to have installed, as well as a minimum version for them (`min_version`). If any requirement is failed, the student will receive a warning and help message.

To check the environment, invoke the `check_environment` function, with the name of the submodule which contains your desired `requirements.toml`. For example, to check the requirements for `week1`, the function is called with the string `"mude.week1"`, since the TOML is stored in the folder for the `week1` submodule.

Example feedback from environment checker:

```
Your Python version (3.11.4) is up-to-date

Your Conda version (23.5.2) is up-to-date
You're executing this in the base environment, all is good!

Checking package versions...
numpy: ✓ (up-to-date, found: 1.25.2)
matplotlib: ✓ (up-to-date, found: 3.7.2)
mude: ✓ (up-to-date, found: 0.1.0)
Well done, your packages meet the default MUDE requirements.
```

## Weekly assignments

Functions related to weekly assignments are stored in their own submodules. For example, `week1` contains the `fit_a_line_to_data` and `help_task_2` functions which are called in the notebook. After updating the submodule for a week, bump the patch version number (the third one), after adding a new submodule bump the the minor version (the second number). If at any point you change a module in a way that will break existing notebooks, change the major version (the first number).

## Authors

This package was developed by the MUDE teaching team at the TU Delft Faculty of Civil Engineering and Geosciences.

## License

Per the default suggested in the roadmap “Copyright and open licenses in online education” of the TU Delft Open Education Consortium, this work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
