import datetime
import csv
import time
import msvcrt
import threading
import sys
import os

file = 'db.csv'
backup_file = 'db_tmp.csv'

initial_time = None
current_time = None
db = []
current_row = [None,None,None]

pressed_char = None

def readTotalTimeFromFile():
    with open(file, newline='') as dbfile:
        dbreader = csv.reader(dbfile, delimiter = ',')

        for row in dbreader:
            db.append(row)

        total_time_seconds = 0
                
        for row in db[1:]:
            total_time_seconds += float(row[2])
        
        total_time = datetime.timedelta(seconds = total_time_seconds)

        print('Total time so far: ' + str(total_time))
    
    with open(backup_file, 'w', newline='') as backupfile:
        writer = csv.writer(backupfile, delimiter=',')
        writer.writerows(db)
        
def countThread():
    global current_row
    global current_time
    global pressed_char
    print('Waiting for input, press \'space\' to start recording time or \'ESCape\' to exit')

    while(True):
        while(not(msvcrt.kbhit())):
            time.sleep(0.2)
        pressed_char = msvcrt.getch()
        if(pressed_char == b' '):
            break
        elif(pressed_char == chr(27).encode()):
            sys.exit(0)


    time_diff = None
    print('Start Recording, press \'space\' to stop or \'ESCape\' to stop and exit')
    initial_time = datetime.datetime.now(datetime.UTC)
    current_row[0] = initial_time
    print('Start time: ' + initial_time.strftime('%H:%M:%S:%f'))
    print('Elapsed Time: ')
    while(True):
        time.sleep(0.1)
        current_time = datetime.datetime.now(datetime.UTC)
        
        time_diff = (current_time-initial_time)
        print(time_diff, end="\r")
        
        if(msvcrt.kbhit()):
            pressed_char = msvcrt.getch()
            if(pressed_char == b' ' or pressed_char == chr(27).encode()):
                end_time = current_time
                current_row[1] = end_time
                break

    print('Total time: ', end ="")
    print(time_diff)
    
def csvThread():
    global current_time
    
    seconds_to_auto_save = 5
    auto_save_timer = seconds_to_auto_save
    
    # Make sure the variable has been initialized
    while(current_row[0] == None):
        time.sleep(0.3)
        if(pressed_char == chr(27).encode()):
            sys.exit(0)
    
    while(True):
        time.sleep(1)
        if(current_row[1] != None):
            
            current_row[2] = (current_row[1] - current_row[0]).total_seconds()
            db.append([str(current_row[0]),str(current_row[1]),str(current_row[2])])
    
            with open(file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(db)
                return
        else:
            auto_save_timer -= 1
            if(auto_save_timer == 0):
                auto_save_timer = seconds_to_auto_save
                with open(file, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    tmp_row = []
                    tmp_row.append(str(current_row[0]))
                    tmp_row.append(str(current_time))
                    tmp_row.append(str((current_time - current_row[0]).total_seconds()))
                    db.append(tmp_row)
                    writer.writerows(db)
                    db.pop()
        
def main():
    global current_row
    os.system("cls")
    print('Starting Time logger')

    readTotalTimeFromFile()
    
    while(True):
        timer_thread = threading.Thread(target=countThread)
        csv_thread = threading.Thread(target=csvThread)
        
        timer_thread.start()
        csv_thread.start()
        
        timer_thread.join()
        csv_thread.join()
        
        if(pressed_char == chr(27).encode()):
            sys.exit(0)
        else:
            os.system("cls")
            current_row = [None,None,None]

if __name__ == '__main__':
    main()