import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from random import randint
from datetime import datetime, timedelta

# Generate random data for the last 10 days
dates = [datetime.now() - timedelta(days=i) for i in range(10)]
qtys = [randint(1, 20) for _ in range(10)]
costs = [randint(10, 100) for _ in range(10)]
values = np.array(qtys) * np.array(costs) 

# Convert time to matplotlib date
mpl_dates = mdates.date2num(dates)

# Determine the size of each point as a percentage of the y-range
y_range = max(values) - min(values)
sizes = (np.array(qtys) / max(qtys)) * y_range * 0.05  # 5% of y-range

# Create a scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(mpl_dates, values, c=range(len(values)), cmap='viridis', s=sizes)

# Formatting the date on the x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.xlabel('Time')
plt.ylabel('Value (Qty * Cost)')
plt.title('Scatter Plot')
plt.grid(True)
plt.colorbar(scatter, label='Order Index')
plt.show()

