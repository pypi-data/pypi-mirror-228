from os import sep
import pandas as pd
import numpy as np
from collections import Counter
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan

def get_wifi_matrix_day(df_hour):
    ymd_list = []

    WIFI_ON_list = []
    MISSING_list = []

    ymd = list(df_hour.YEAR_MONTH_DAY.unique())[0]

    ymd_list.append(ymd)
    WIFI_ON = df_hour.WIFI_ON.sum()
    MISSING_num = df_hour.MISSING.sum()

    WIFI_ON_list.append(WIFI_ON)
    MISSING_list.append(MISSING_num)

    df_day = pd.DataFrame(
        {"YEAR_MONTH_DAY": ymd_list, "WIFI_ON": WIFI_ON_list, "MISSING": MISSING_list})

    return df_day


if __name__ == "__main__":
    df_minute = pd.read_csv(
        r"C:\Users\Jixin\Downloads\activity_minute.csv")
    df_hour = get_wifi_matrix_day(df_minute)
    print(df_hour)
    # df_hour.to_csv(r"C:\Users\Jixin\Downloads\watch_accelerometer_decompose_hour_2021-02-04.csv")
