from .. import environment_checking
from pathlib import Path
import os
import numpy as np

def fit_a_line_to_data(x, y):
    """ Fits a line of best fit (using least squares) to data points
    Arguments:
        x (numpy array): x-coordinates of points
        y (numpy array): y-coordinates of points
    """
    
    x_mean, y_mean = np.mean(x), np.mean(y)
    slope = np.sum(np.multiply((x - x_mean), (y - y_mean))) / np.sum(np.square(x - x_mean))
    intercept = y_mean - slope * x_mean
    
    return (slope, intercept)
    
def check_environment():
	environment_checking.check_environment(__name__)
	
def help_task_2(globalz):
	csv_path = Path("auxiliary_files/data.csv")
	
	if csv_path.exists():
		print("Well done, you set up your working directory properly.")
	else:
		print("OOPS! The data file is in the wrong location. Pay attention to the working directory recommendations.")    
	print()
	
	cwd = Path(os.getcwd())
	
	if cwd.name == "Week_1_1":
		print("Well done, it looks like you set up a good working directory structure.")
	else:
		print("OOPS! It looks like you aren't using a working directory for Q1 Week 1 (Week_1_1). Why not?")
	print()
	
	if "data_x" in globalz and "data_y" in globalz:
		print("The data is in the notebook--great! You can continue with this assignment.")
	else:
		print("OOPS! The data has not been added to the notebook environment. Make sure you successfully run the data import cell (Task 2.1) before moving on.")
	
	
	
	
