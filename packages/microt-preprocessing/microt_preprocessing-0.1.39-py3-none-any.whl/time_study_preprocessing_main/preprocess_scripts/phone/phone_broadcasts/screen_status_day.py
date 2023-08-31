from os import sep
import pandas as pd
import numpy as np
import warnings

# warnings.filterwarnings("ignore")
NAN = np.nan


def get_screen_status_matrix_day(df_hour):
    ymd_list = []
    screen_on_seconds_list = []
    unlock_events_num_list = []

    ymd = list(df_hour.YEAR_MONTH_DAY.unique())[0]

    screen_on_seconds_hour = df_hour.SCREEN_ON_SECONDS.sum()
    unlock_events_num = df_hour.UNLOCK_EVENTS_NUM.sum()

    ymd_list.append(ymd)

    screen_on_seconds_list.append(screen_on_seconds_hour)
    unlock_events_num_list.append(unlock_events_num)

    df_day = pd.DataFrame(
        {"YEAR_MONTH_DAY": ymd_list, "SCREEN_ON_SECONDS": screen_on_seconds_list, "UNLOCK_EVENTS_NUM": unlock_events_num_list})

    return df_day


if __name__ == "__main__":
    df_minute = pd.read_csv(
        r"C:\Users\Jixin\Downloads\screen_minute.csv")
    df_hour = get_screen_status_matrix_day(df_minute)
    print(df_hour)
    # df_hour.to_csv(r"C:\Users\Jixin\Downloads\watch_accelerometer_decompose_hour_2021-02-04.csv")
