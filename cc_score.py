import readability
import query_data
import pandas as pd
import time
import datetime

def cc_func(data):
    score = 0
    return score


if __name__ == "__main__":
    user_list = ["100001997853167", "100003714391961", "567112096", "100004095850481", "100003798186002", "100001961447372", "100003597533936",
                 "100005839453026", "100009887565225", "100010333095645", "100006280091794", "697906484", "1347383858", "100000201925350",
                 "100001131635765", "1122706035", "1165047523", "100000258961669", "595494437", "554757389", "719335150", "100001261711300",
                 "1362923905", "100002708846347", "100000718348778"]

    start = time.time()
    start_date = datetime.datetime(2018, 2, 12)
    end_date = datetime.datetime(2020, 2, 18)
    print('start date: ',start_date)
    print('end date: ',end_date)
    data = query_data.get_post(user_list,start_date,end_date)
    data.to_csv("./Backup/data.csv",index=False)
    print("time: ", time.time()-start)
