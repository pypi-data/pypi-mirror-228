from os import sep
import pandas as pd
import numpy as np
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan
colnames = ["YEAR_MONTH_DAY", "HOUR", "MINUTE", "PHONE_DETECTED_ACTIVITY"]
activity_types = ["IN_VEHICLE", "ON_BIKE","ON_FOOT", "RUNNING", "STILL", "TILTING","WALKING", "UNKNOWN"]


def get_stepcount_matrix_day(df_stepcount):
    if df_stepcount.shape[0] == 0:
        return None

    # transform df_mims_day
    ymd_list = []
    tz_list = []
    for time_str in df_stepcount["LOG_TIME"]:
        ymd_list.append(time_str.split(" ")[0])
        tz_list.append(time_str.split(" ")[2])

    ymd_list = [x for x in ymd_list if len(x) > 0]
    YMD = list(set(ymd_list))[0]
    tz = list(set(tz_list))[0]
    ttsteps = df_stepcount.STEPS_LAST_HOUR.sum()

    df_day = pd.DataFrame(
        {"YEAR_MONTH_DAY": [YMD], "TIMEZONE": [tz], "TOTAL_STEPS": [ttsteps]})

    return df_day

if __name__ == "__main__":
    pass
