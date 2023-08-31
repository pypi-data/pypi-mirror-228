from os import sep
import pandas as pd
import numpy as np
from collections import Counter
from ...utils.parse_YMD import *
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan

def get_battery_matrix_day(df_hour):
    ymd_list = []

    BATTERY_LEVEL_list = []
    CHARGING_STATUS_list = []
    MISSING_list = []

    ymd = list(df_hour.YEAR_MONTH_DAY.unique())[0]

    average_battery_level = df_hour.AVERAGE_BATTERY_LEVEL.mean()
    CHARGING_MINUTES = df_hour.CHARGING_MINUTES.sum()
    MISSING_MINUTES = df_hour.MISSING_MINUTES.sum()

    ymd_list.append(ymd)

    BATTERY_LEVEL_list.append(average_battery_level)
    CHARGING_STATUS_list.append(CHARGING_MINUTES)
    MISSING_list.append(MISSING_MINUTES)

    df_day = pd.DataFrame(
        {"YEAR_MONTH_DAY": ymd_list, "AVERAGE_BATTERY_LEVEL": BATTERY_LEVEL_list, "CHARGING_MINUTES": CHARGING_STATUS_list, "CHARGING_STATES_MISSING_MINUTES": MISSING_list})
    # parse YMD
    y_list, m_list, d_list = parse_YMD(df_day.YEAR_MONTH_DAY)
    df_day["YEAR"] = y_list
    df_day["MONTH"] = m_list
    df_day["DAY"] = d_list

    return df_day


if __name__ == "__main__":
    df_minute = pd.read_csv(
        r"C:\Users\Jixin\Downloads\activity_minute.csv")
    df_hour = get_battery_matrix_day(df_minute)
    print(df_hour)
    # df_hour.to_csv(r"C:\Users\Jixin\Downloads\watch_accelerometer_decompose_hour_2021-02-04.csv")
