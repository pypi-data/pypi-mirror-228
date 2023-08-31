from os import sep
import pandas as pd
import numpy as np
from collections import Counter
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan


def get_location_cluster_day(df_hour):
    ymd = list(df_hour.YEAR_MONTH_DAY.unique())[0]

    colname_list = list(df_hour.columns)
    colname_list.remove("HOUR")
    clusterID_list = [x for x in colname_list if x not in ["YEAR_MONTH_DAY"]]
    df_hour = df_hour[clusterID_list]
    df_day = pd.DataFrame(df_hour.sum(axis=0)).T
    df_day["YEAR_MONTH_DAY"] = ymd

    df_day = df_day[colname_list]

    return df_day


if __name__ == "__main__":
    df_minute = pd.read_csv(
        r"C:\Users\jixin\Downloads\2020-08-07\phone_location_cluster_minute.csv")
    df_hour = get_location_cluster_day(df_minute)
    print(df_hour)
    # df_hour.to_csv(r"C:\Users\Jixin\Downloads\watch_accelerometer_decompose_hour_2021-02-04.csv")
