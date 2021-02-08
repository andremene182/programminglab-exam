from statistics import mean 

# Class ExamException
# Useful to raise Exceptions for exam
class ExamException(Exception):
  pass


# Class CSVTimeSeriesFile
class CSVTimeSeriesFile:

  # Constructor of CSVTimeSeriesFile
  # @param name -> the name of the csv to analyze
  def __init__(self,name):
    self.name = name
    
  # function getData
  # @returns csvValues -> a list of list in format [epoch, temperature]
  def getData(self):


    # Open the file, if it's possible
    try:
      csvFile = open(self.name, "r")
    except Exception as e:
      raise ExamException("It is not possible to open the file '{}'. Exception:{}".format(self.name,e)) from None

    csvValues = []

    # Extract data in format [epoch, temperature] from the file
    for line in csvFile:
      elements = line.split(',')

      if elements[0] != 'epoch':
        try:
          epoch = elements[0]
          temperature = elements[1]
        except Exception as e:
          continue
        try:
          epoch=int(epoch)
          temperature = float(temperature)
        except Exception as e:
          continue
        csvValues.append([epoch,temperature])
    csvFile.close()

    # Verify if the data are not empty
    if not csvValues:
      raise ExamException("The file '{}' doesn't contain values or it contains only one incomplete record. Please check the file again.".format(self.name))

    return csvValues


# Function calculate_stats
# @param day_temps -> list of day temperatures
# @returns single_day_stats -> list containing the min, the max and the avg temp of the single day
def calculate_single_day_stats(day_temps):
  min_temp = min(day_temps)
  max_temp = max(day_temps)
  avg_temp = mean(day_temps)

  single_day_stats = [min_temp, max_temp, avg_temp]

  return single_day_stats



# Function daily_stats
# @param time_series -> list of [epoch,temperature] data
# @returns stats -> list of list min, max and avg temperature per day
def daily_stats(time_series):



  # Verify if there are duplicates epochs
  time_series_epochs = [item[0] for item in time_series]
  time_series_epochs_set = set(time_series_epochs)
  contains_duplicates = len(time_series_epochs) != len(time_series_epochs_set)
  if(contains_duplicates):
    raise ExamException("The data contains duplicates epochs. Epochs have to be single values.")

  stats = []
  day_temps = []
  days = []
  daysCount = 0
  new_day = None

  

  for i,item in enumerate(time_series):

    epoch = item[0]
    temp = item[1]
    

    # Verify if epochs are in ascending order
    if(item != time_series[0] and epoch < time_series[i-1][0]):
      raise ExamException("The epoch '{}' is not in ascending order.".format(epoch))
      
    # Is there a new day?
    if (epoch % 86400) == 0:
      new_day = epoch
      days.append(new_day)
      
      
      if (day_temps and i!=0):
        stats.append(calculate_single_day_stats(day_temps))

      daysCount += 1

    # New Day Init
      day_temps = []
      day_temps.append(temp)
      
    # Verify if new_day exists
    elif new_day:
       # If the epoch is not a new day, verify if it belongs to new_day
      if (epoch - (epoch % 86400) == new_day):
        day_temps.append(temp)
    else:
      continue
    
    # Verify if the epoch is the last of the series, then append the new stats
    if(epoch == time_series[-1][0]):
      if (day_temps):
        stats.append(calculate_single_day_stats(day_temps))
        
  return stats