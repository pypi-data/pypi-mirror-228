from os import sep
import pandas as pd
import numpy as np
from collections import Counter
from ...utils.parse_YMD import *
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan

def get_battery_matrix_hour(df_minute):
    ymd_list = []
    hour_list = []

    BATTERY_LEVEL_list = []
    CHARGING_STATUS_list = []
    MISSING_list = []

    ymd = list(df_minute.YEAR_MONTH_DAY.unique())[0]

    for hour in range(24):
        df_subset = df_minute[df_minute.HOUR == str(hour)]
        average_battery_level = np.nanmean(pd.to_numeric(df_subset['BATTERY_LEVEL'], errors='coerce'))

        pred_count = Counter(df_subset.CHARGING_STATUS)
        if 'true' in pred_count:
            CHARGING_STATUS = pred_count['true']
        else:
            CHARGING_STATUS = 0

        MISSING_num = 60 - pred_count['true'] - pred_count['false']

        ymd_list.append(ymd)
        hour_list.append(hour)

        BATTERY_LEVEL_list.append(average_battery_level)
        CHARGING_STATUS_list.append(CHARGING_STATUS)
        MISSING_list.append(MISSING_num)

    df_hour = pd.DataFrame(
        {"YEAR_MONTH_DAY": ymd_list, "HOUR": hour_list, "AVERAGE_BATTERY_LEVEL": BATTERY_LEVEL_list, "CHARGING_MINUTES": CHARGING_STATUS_list, "CHARGING_STATES_MISSING_MINUTES": MISSING_list})

    # parse YMD
    y_list, m_list, d_list = parse_YMD(df_hour.YEAR_MONTH_DAY)
    df_hour["YEAR"] = y_list
    df_hour["MONTH"] = m_list
    df_hour["DAY"] = d_list
    return df_hour


if __name__ == "__main__":
    df_minute = pd.read_csv(
        r"C:\Users\Jixin\Downloads\activity_minute.csv")
    df_hour = get_battery_matrix_hour(df_minute)
    print(df_hour)
    # df_hour.to_csv(r"C:\Users\Jixin\Downloads\watch_accelerometer_decompose_hour_2021-02-04.csv")
