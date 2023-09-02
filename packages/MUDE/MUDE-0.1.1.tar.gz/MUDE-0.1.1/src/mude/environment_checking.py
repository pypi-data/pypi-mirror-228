import os
from pathlib import Path

import tomllib
import pkgutil
import pkg_resources
import platform
import subprocess
import sys

def check_environment(package):
    """
    Prints the Conda prefix (full path to Conda installation) of the Conda environment that is
    currently in use. Additionally, prints a list of the versions of a hard-coded set of packages
    that we use within MUDE.
    """
    
#    if "CONDA_PREFIX" in os.environ:
#    	print("You are running this notebook in a conda environment, perfect!")
#    else:
#    	print("You are not using a conda environment, it is highly recommended you do so for this course. Check the course website and textbooks for #further guidance.")
#    print()
    	 
    toml = tomllib.loads(pkgutil.get_data(package, "requirements.toml").decode("utf-8"))
    min_python_version = pkg_resources.parse_version(toml["environment"]["min_python"])
    installed_version = pkg_resources.parse_version(platform.python_version()) 
    if  installed_version >= min_python_version:
    	print(f"Your Python version ({installed_version}) is up-to-date")
    else:
    	print(f"Your Python version ({installed_version}) is outdated, the recommened minimum is {min_python_version}. Check the course website and textbooks for further guidance.")
    	print("Your packages will only be checked after you've updated your Python")
    	return
    print()
    
    try:
        conda_version_command = subprocess.run(["conda", "--version"], capture_output = True, check = True)
        installed_conda_version = pkg_resources.parse_version(
                                      conda_version_command.stdout.decode("utf-8").split(' ')[1]
                                  )
        min_conda_version = pkg_resources.parse_version(toml["environment"]["min_conda"])
        if (installed_conda_version >= min_conda_version):
            print(f"Your Conda version ({installed_conda_version}) is up-to-date")
        else:
            print(f"Your Conda version ({installed_conda_version}) is outdated, the recommended minimum is {min_conda_version} to avoid issues")         
       	
       	try:
       	    conda_envs_command = subprocess.run(["conda", "env", "list"], capture_output = True, check = True)
       	    conda_prefix = Path(next(filter(lambda line: line.startswith("base"), 
       	                               conda_envs_command.stdout.decode("utf-8").split("\n")))[4:].strip())
       	    executable_path = Path(sys.executable)
       	    
       	    if executable_path.is_relative_to(conda_prefix):
       	        environment_name = "base"
       	        if executable_path.parent.parent.parent.name == "envs":
       	            environment_name = executable_path.parent.parent.name
       	        print(f"You're executing this in the {environment_name} environment, all is good!")
       	    else:
       	    	print(f"You're not running this under a conda environment, maybe you forgot to activate it or select the right kernel?")
       	    
        except Exception as err:
            print("An unexpected error occured whilst trying to figure out your conda environment :(")  
            print(err) 	
       	
    except subprocess.CalledProcessError:
    	print("You don't have conda installed, it's highly recommended you use it for this course to reduce the chance of encountering issues down the line!")
    print()
    
    error = False
    print("Checking package versions...")
    for package, info in toml["requirement"].items():
        try:
                distribution = pkg_resources.get_distribution(package)
                parsed_min_version = pkg_resources.parse_version(info["min_version"])
        	
                if (distribution.parsed_version >= parsed_min_version):
        	        print(f"{package}: ✓ (up-to-date, found: {distribution.version})")
                else:
                        print(f"{package}: ⨯ (outdated, need >={info['min_version']}, but found {distribution.version})")
                        error = True
        
        except pkg_resources.DistributionNotFound:
                print(f"{package}: ⨯ (not installed)")
                error = True
    
    if error:
        print("Your packages do not meet the default MUDE requirements. Please review the course website, textbook and errors above for further guidance.")
        print("You can upgrade packages using `pip install --upgrade <package>`, or if you install them using conda `conda update <package>`")
    else:
        print("Well done, your packages meet the default MUDE requirements.")
    	
    """
    try:
    	print("Conda prefix: {}".format(os.environ["CONDA_PREFIX"]))
    except:
    	print(
    print("Numpy version: {}".format(np.__version__))
    print("Matplotlib version: {}".format(mpl.__version__))
    print("Scipy version: {}".format(sp.__version__))
    """

def _print_directory_tree(path):
    """
    Internal helper function that prints out a tree view of a given directory and all subdirectories.
    """
    for root, _, files in os.walk(path):
        indentation = root.replace(path, "").count(os.sep)
        folder_indentation = "    " * indentation
        folder_string = os.path.basename(root)
        print("{}{}/".format(folder_indentation, folder_string))
        file_indentation = "    " * (indentation + 1)
        for file in files:
            print("{}{}".format(file_indentation, file))


def check_directory(level=0):
    """
    Prints a tree view of the currently-active directory, plus the indicated amount of levels upwards.
    """
    current_directory = Path(os.getcwd())
    if level == 0:
        _print_directory_tree(str(current_directory))
    elif level < 0:
        print(
            "Error: cannot print directory to a level {}, which is below 0. Printing level 0 only.".format(
                level
            )
        )
        _print_directory_tree(str(current_directory))
    elif level > len(current_directory.parents):
        print(
            "Error: trying to print out to a level ({}) above the number of parent directories ({}). Printing level 0 only.".format(
                level, len(current_directory.parents)
            )
        )
        _print_directory_tree(str(current_directory))
    else:
        _print_directory_tree(str(current_directory.parents[level - 1]))

"""
def example_plot():
    \"\"\"
    Creates an example plot of a sine and cosine, primarily as tool to verify that all necessary
    packages and functionality are present to do so.
    \"\"\"
    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.arange(0, 2 * np.pi, step=0.01)
    sine = np.sin(x)
    cosine = np.cos(x)
    ax.plot(x, sine, label="Sine", color="#00A6D6", linewidth=2)
    ax.plot(x, cosine, label="Cosine", color="#000000", linestyle="--", linewidth=2)
    ax.set_xlabel("Argument [-]")
    ax.set_ylabel("Function value [-]")
    fig.suptitle("Example plot")
    ax.legend()
    plt.show()
"""
