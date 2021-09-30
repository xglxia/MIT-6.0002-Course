# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy as np

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()
        #print(self.rawdata['SEATTLE'].keys())
        #print(self.rawdata['SEATTLE'][1961][1])

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

#print(Climate('data.csv').get_daily_temp('SEATTLE', 1, 1, 1961,))
#sampl = Climate('data.csv').rawdata['NEW YORK']
#print(sampl)
#print(Climate('data.csv').rawdata['NEW YORK'][1961][1])

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    assert len(x) == len(y)
    models = []
    for d in degs:
        model_d = pylab.polyfit(x, y, d)
        models.append(model_d)
        
    return models

#print(generate_models(pylab.array([1961, 1962, 1963]), pylab.array([-4.4, -5.5, -6.6]), [1, 2]))

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    numerator = ((y - estimated)**2).sum()
    denominator = ((y - y.mean())**2).sum()
    
    return 1 - numerator/denominator

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    
    
    for model in models:
        estY = pylab.polyval(model, x)
        
        pylab.figure()
        pylab.plot(x, y, 'bo', label = 'Data Points')
        pylab.plot(x, estY, 'r-', label = 'Model')
        pylab.legend(loc='best')
        pylab.xlabel('Year')
        pylab.ylabel('Degree in Celsius')
        if len(model) == 2:
            pylab.title('r**2 = ' + str(r_squared(y, estY)) + '\n'
                        + 'degree =' + str(len(model)-1) + '\n '
                         + 'standard error =' + str(se_over_slope(x, y, estY, model)))
        else:
            pylab.title('r**2 = ' + str(r_squared(y, estY)) + 'and degree =' + str(len(model)-1))

            
            
            
def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    avg_year_temp = []
    for year in years:
        cities_year_temp = []
        for city in multi_cities:
            city_year_temp = climate.get_yearly_temp(city, year)
            cities_year_temp.append(city_year_temp)
        cities_year_temp = pylab.array(cities_year_temp)
        
        avg_year_temp.append(cities_year_temp.mean())
            
    avg_year_temp = pylab.array(avg_year_temp)
        
   
    return avg_year_temp
    
# climate = Climate('data.csv')
# multi_cities = ['TAMPA', 'DALLAS']
# years = range(2010, 2016)  
# gen_cities_avg(climate, multi_cities, years)   

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    moved_average = []
    y = pylab.array(y)
    for i in range(len(y)):
        if i < window_length:
            slice_i = y[:(i+1)]
            avg_slice_i = slice_i.sum()/slice_i.size
            moved_average.append(avg_slice_i)
        else:
            slice_i = y[(i - window_length +1):(i+1)]
            avg_slice_i = slice_i.sum()/window_length
            moved_average.append(avg_slice_i)
    moved_average = pylab.array(moved_average)
    
    return moved_average

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    Error_sum = ((y - estimated)**2).sum()
    
    return (Error_sum/len(y))**0.5
    
    

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    
    yearly_std_dev = []
    for year in years:
        cities_year_temp = []
        for city in multi_cities:
            city_year_temp = climate.get_yearly_temp(city, year)
            cities_year_temp.append(city_year_temp)
        cities_year_temp = pylab.array(cities_year_temp)  
        daily_mean = cities_year_temp.mean(axis=0)   
        std_dev = pylab.std(daily_mean)   
        yearly_std_dev.append(std_dev)
    yearly_std_dev = pylab.array(yearly_std_dev)  
    return yearly_std_dev
    
    
   

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    
    for model in models:
        estY = pylab.polyval(model, x)
        
        pylab.figure()
        pylab.plot(x, y, 'bo', label = 'Data Points')
        pylab.plot(x, estY, 'r-', label = 'Model')
        pylab.legend(loc='best')
        pylab.xlabel('Year')
        pylab.ylabel('Degree in Celsius')
        pylab.title('RMSE = ' + str(rmse(y, estY)) + '\n'
                    + 'and degree =' + str(len(model)-1))
    
    
    

if __name__ == '__main__':

    pass 

    # Part A.4
    # TODO: replace this line with your code
    
    #Part A.4.I
    # sample1 = []
    # for year in range(1961, 2010):
    #     sample1.append(Climate('data.csv').rawdata['NEW YORK'][year][1][10])
   
    # sample1 = [-2.5, -5.8, 2.75, 0.85, 1.1, 2.8, 1.1, -12.75, -3.05, -6.1, -0.25, 9.45, -1.9, -1.9, 5.8, -6.35, -0.85, -8.1, -3.9, -1.65, -7.5, -11.1, 7.8, 3.3, -5.0, 4.15, 3.35, -5.3, -0.3, 5.8, 1.95, 5.55, -3.35, -6.1, -1.35, -1.65, 2.75, 5.85, -2.5, 9.2, -2.5, 6.7, 3.9, -12.8, 6.1, 6.1, 0.25, 6.95, -2.2]
    # x_sample1 = np.array(range(1961, 2010))
    # y_sample1 = np.array(sample1)
    
    # model_1 = generate_models(x_sample1, y_sample1, degs = [1])
    # evaluate_models_on_training(x_sample1, y_sample1, model_1)
    
    #Part A.4.II
    # avg_year_temp = []
    # for year in range(1961, 2010):
    #     year_temp = Climate('data.csv').rawdata['NEW YORK'][year]
    #     avg_mon = []
    #     for key in year_temp.keys():
    #         mon_total_temp = sum(year_temp[key].values())
    #         avg_mon_tep = mon_total_temp/len(year_temp[key])
    #         avg_mon.append(avg_mon_tep)
        
    #     avg_year_temp.append(sum(avg_mon)/12)
        
    
    # avg_year_temp = [11.96191660266257, 11.016225678443421, 11.4928168202765, 11.908683568162154, 11.262811059907834, 11.716622183819766, 10.282604646697388, 11.377538623161536, 12.156330645161288, 12.108514784946237, 12.741629544290836, 12.426437554072427, 12.641246799795185, 12.332848502304147, 12.532011968766, 11.234535595105674, 11.293406938044035, 11.818886328725037, 11.915376024065543, 11.957445309603264, 12.435077124935995, 12.225005120327701, 13.143601510496671, 12.895545822518846, 12.524841269841268, 12.28655049923195, 12.172513120839731, 11.873249907304412, 11.75634056579621, 13.131177675371227, 13.450978302611366, 11.748549623037944, 12.335186891961087, 12.249856950844853, 12.684842229902713, 11.524589667531826, 12.152053571428572, 13.317868343573991, 12.871925243215566, 11.660225404770735, 12.736383128520224, 12.864998079877113, 11.49721678187404, 12.094236497342726, 12.410512992831542, 13.168001152073735, 12.37071044546851, 12.67985508589791, 12.13781266001024]
    
    # x_sample2 = np.array(range(1961, 2010))
    # y_sample2 = np.array(avg_year_temp)
    
    # model2 = generate_models(x_sample2, y_sample2, degs = [1])
    # evaluate_models_on_training(x_sample2, y_sample2, model2)
    
    
    
    # Part B
    # TODO: replace this line with your code
    # x_sample3 = pylab.array(TRAINING_INTERVAL)
    # y_sample3 = gen_cities_avg(Climate('data.csv'), CITIES, TRAINING_INTERVAL)
    # model3 = generate_models(x_sample3, y_sample3, [1])
    # evaluate_models_on_training(x_sample3, y_sample3, model3)
        

    # Part C
    # TODO: replace this line with your code
    # cities_avg = gen_cities_avg(Climate('data.csv'), CITIES, TRAINING_INTERVAL)
    # x_sample4 = pylab.array(TRAINING_INTERVAL)
    # y_sample4 = moving_average(cities_avg, 5)
    # model4 = generate_models(x_sample4, y_sample4, [1])
    # evaluate_models_on_training(x_sample4, y_sample4, model4)
    
    
   

    # Part D.2.I
    # TODO: replace this line with your code
    # cities_avg = gen_cities_avg(Climate('data.csv'), CITIES, TRAINING_INTERVAL)
    # x_sample5 = pylab.array(TRAINING_INTERVAL)
    # y_sample5 = moving_average(cities_avg, 5)
    # degs = [1, 2, 20]
    
    # model5 = generate_models(x_sample5, y_sample5, degs)
    # evaluate_models_on_training(x_sample5, y_sample5, model5)
    
    #Part D.2.II
    
    # cities_avg = gen_cities_avg(Climate('data.csv'), CITIES, TRAINING_INTERVAL)
    # x_sample5 = pylab.array(TRAINING_INTERVAL)
    # y_sample5 = moving_average(cities_avg, 5)
    # degs = [1, 2, 20]
    # model5 = generate_models(x_sample5, y_sample5, degs)
    
    # cities_avg_testing = gen_cities_avg(Climate('data.csv'), CITIES, TESTING_INTERVAL)
    # x_sample5_testing = pylab.array(TESTING_INTERVAL)
    # y_sample5_testing = moving_average(cities_avg_testing, 5)
    # evaluate_models_on_testing(x_sample5_testing, y_sample5_testing, model5)
    
        

    # Part E
    # TODO: replace this line with your code
    
    # std_dev = gen_std_devs(Climate('data.csv'), CITIES, TRAINING_INTERVAL)
    # std_dev_moved = moving_average(std_dev, 5)
    # x_data = pylab.array(TRAINING_INTERVAL)
    # std_dev_models = generate_models(x_data, std_dev_moved, [1, 2, 20])
    # evaluate_models_on_training(x_data, std_dev_moved, std_dev_models)
    
