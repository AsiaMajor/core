import csv
import os
import statistics
from tqdm import tqdm
import time



def get_wh_data(sheet):
    l = []
    std = []
    i = 0
    end = 0

    cwd = os.getcwd()
    path = 'dbfiles/' + sheet

    with open(os.path.join(cwd, path)) as df:
        r = csv.reader(df)
        for row in r:
            if i > 5 and row != ['Avg Vel', 'stdev Vel.', 'avg UPT', 'stdev UPT']:
                l.append(row)
            if end == 1:
                std.append(row)
                break
            if row == ['Avg Vel', 'stdev Vel.', 'avg UPT', 'stdev UPT']:
                end = 1
            i += 1
        
    #print(len(l))
    #print(l[-5:])
    return l, std


#returns certain column from dataset
def get_n_column(l, n):
    col = []

    for row in l:
        if len(row) == 7:
            col.append(row[n])
    return col


avg_3percent_thresh = 400
def process_new_sheet(data):
  '''take in new sheet, calculate the 3% 50% 97% thresh'''
  data =sorted(data)
  thresh_3 = max(data[0:int(len(data)*0.03)])
  thresh_50 = statistics.median(data)
  thresh_97 = min(data[int(len(data)*0.97):len(data)])
  return thresh_3,thresh_50,thresh_97


if __name__ == '__main__':
    starttime = time.time()
    averages_vel = {'bot3':0, 'mid':0, 'top3':0, 'intq': 0, 'std': 0}
    averages_upt = {'bot3':0, 'mid':0, 'top3':0, 'intq': 0, 'std': 0}
    num_files = 0


    for file in tqdm(os.listdir('dbfiles')):
        new_col_v = []
        new_col_u = []

        wh_info,std = get_wh_data(file)


        col_info_v = get_n_column(wh_info, 1) #1 is effvel
        col_info_u = get_n_column(wh_info, 2) #2 is fro effupt
        num_files += 1

        #print(type(col_infor))
        for i in col_info_v:
            try:
                t = float(i)
                new_col_v.append(t)
            except ValueError:
                t = i

        for i in col_info_u:
            try:
                t = float(i)
                new_col_u.append(t)
            except ValueError:
                t = i
            

        bot3v, av, top3v = process_new_sheet(new_col_v)
        bot3u, au, top3u = process_new_sheet(new_col_u)

        averages_vel["bot3"] += bot3v
        averages_vel["mid"] += av
        averages_vel["top3"] += top3v
        averages_vel["std"] += float(std[0][1])

        averages_upt["bot3"] += bot3u
        averages_upt["mid"] += au
        averages_upt["top3"] += top3u
        averages_upt["std"] += float(std[0][3])


        #print(bot3, a, top3)
        #c = input()
    for key,value in averages_vel.items():
        if key != 'intq':
            averages_vel[key] /= num_files

    for key,value in averages_upt.items():
        if key != 'intq':
            averages_upt[key] /= num_files

    averages_vel['intq'] = averages_vel['top3'] - averages_vel['bot3']
    averages_upt['intq'] = averages_upt['top3'] - averages_upt['bot3']

    print(averages_vel)
    print(averages_upt)
    
    endtime = time.time()
    print(endtime - starttime)
