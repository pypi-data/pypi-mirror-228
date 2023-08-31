import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

def csv_read(path):
    return pd.read_csv(path)


def plot_gender(df):
    sevc = df['Sex'].value_counts()

    sevc_index = list(sevc.keys())

    sevc_values = np.array(list(sevc)) # ใช้ Array เพื่อให้การคำนวนง่ายขึ้น
    sevc_normalized = sevc_values / sum(sevc_values) # คำนวนเป็นเปอร์เซ็น

    bars = plt.bar(sevc_index, sevc_normalized, color=['#0099cc', 'pink'])

    plt.ylim(0, 1)
    plt.yticks(plt.yticks()[0], ['{:,.0%}'.format(x) for x in plt.yticks()[0]])

    # Annotating each bar
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0-0.05, yval, sevc_values[i], va='bottom')  # va: vertical alignment

    plt.title("Gender")
    plt.show()

def easy_plot(df):
    plt.hist(df.Age.values)
    plt.show()