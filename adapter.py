from thread import start_new_thread
import socket
import sys, time, linuxcnc, datetime
HOST = ''
PORT = 7878

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

#Socket bind complete

#Start listening on socket
s.listen(5)

#Socket now listening

#now keep talking with the client
def new_client(conn):

    at2='initialize'
    ct2='initialize'
    ylt2='initialize'
    ylt1=datetime.datetime.now() #initialized
    at1=datetime.datetime.now() #initialized
    ct1=datetime.datetime.now() #initialized
    ylt=float(0) #initialized
    at=float(0) #initialized
    ct=float(0) #initialized
    Xabs='UNAVAILABLE'
    Yabs='UNAVAILABLE'
    Zabs='UNAVAILABLE'
    Aabs='UNAVAILABLE'
    Babs='UNAVAILABLE'
    Srpm='UNAVAILABLE'
    estop='UNAVAILABLE'
    power='UNAVAILABLE'
    auto_time='UNAVAILABLE'
    cut_time='UNAVAILABLE'

    total_time='UNAVAILABLE'
    _exec='UNAVAILABLE'
    line='UNAVAILABLE'
    program='UNAVAILABLE'
    Fovr='UNAVAILABLE'
    Sovr='UNAVAILABLE'
    Tool_number='UNAVAILABLE'
    mode='UNAVAILABLE'

    out='initialize'
    output='initialize'

    while True:
        try:
            data=linuxcnc.stat()
            data.poll()
            output=''


            #time initialization: accumulated time: cut - auto - total
            if power=='|power|ON':
                ylt2=datetime.datetime.now()
                if ex=='|exec|ACTIVE' and Srpm!='UNAVAILABLE' and float(Srpm.split('|')[-1])>0 and estop=='|estop|ARMED':
                    ct2=datetime.datetime.now()
                else:
                    ct1=datetime.datetime.now()
                if (ex=='|exec|ACTIVE' or ex=='|exec|STOPPED' or ex=='|exec|INTERRUPTED' or float(Srpm.split('|')[-1])>0) and estop=='|estop|ARMED':
                    at2=datetime.datetime.now()
                else:
                    at1=datetime.datetime.now()
            else:
                ylt1=datetime.datetime.now()



            if data.state==1:
                ex='|exec|READY'
            elif data.state==2:
                ex='|exec|ACTIVE'
            else:
                ex=''

            if ex and ex!=_exec:
                _exec=ex
                output+=_exec

            if data.estop!=1:
                estp='|estop|ARMED'
            else:
                estp='|estop|TRIGGERED'

            if estp!=estop:
                estop=estp
                output+=estop

            pwr='|power|ON'
            if pwr!=power:
                power=pwr
                output+=power

            xps='|Xabs|'+str(format(data.actual_position[0], '.4f'))
            if Xabs!='UNAVAILABLE' and float(xps.split('|')[-1])!=float(Xabs.split('|')[-1]):
                Xabs=xps
                output+=Xabs
            elif Xabs=='UNAVAILABLE':
                Xabs=xps
                output+=Xabs

            yps='|Yabs|'+str(format(data.actual_position[1], '.4f'))
            if Yabs!='UNAVAILABLE' and float(yps.split('|')[-1])!=float(Yabs.split('|')[-1]):
                Yabs=yps
                output+=Yabs
            elif Yabs=='UNAVAILABLE':
                Yabs=yps
                output+=Yabs


            zps='|Zabs|'+str(format(data.actual_position[2], '.4f'))
            if Zabs!='UNAVAILABLE' and float(zps.split('|')[-1])!=float(Zabs.split('|')[-1]):
                Zabs=zps
                output+=Zabs
            elif Zabs=='UNAVAILABLE':
                Zabs=zps
                output+=Zabs

            abs='|Aabs|'+str(format(data.actual_position[3], '.4f'))
            if Aabs!='UNAVAILABLE' and float(abs.split('|')[-1])!=float(Aabs.split('|')[-1]):
                Aabs=abs
                output+=Aabs
            elif Aabs=='UNAVAILABLE':
                Aabs=abs
                output+=Aabs

            bbs='|Babs|'+str(format(data.actual_position[4], '.4f'))
            if Babs!='UNAVAILABLE' and float(bbs.split('|')[-1])!=float(Babs.split('|')[-1]):
                Babs=bbs
                output+=Babs
            elif Babs=='UNAVAILABLE':
                Babs=bbs
                output+=Babs

            ssp='|Srpm|'+str(data.spindle_speed)
            if Srpm!=ssp:
                Srpm=ssp
                output+=Srpm

            ln='|line|'+str(data.current_line)
            if line!=ln:
                line=ln
                output+=line

            pgm='|program|'+str(data.file)
            if pgm!=program:
                program=pgm
                output+=program

            pfo='|Fovr|'+str(data.feedrate*100)
            if pfo!=Fovr:
                Fovr=pfo
                output+=Fovr

            so='|Sovr|'+str(data.spindlerate*100)
            if so!=Sovr:
                Sovr=so
                output+=Sovr

            tooln='|Tool_number|'+str(data.tool_in_spindle)
            if tooln!=Tool_number:
                Tool_number=tooln
                output+=Tool_number


            if data.task_mode==1:
                md='|mode|MDI'
            elif data.task_mode==2:
                md='|mode|AUTOMATIC'
            elif data.task_mode==3:
                md='|mode|MANUAL'
            else:
                md=''

            if md and md!=mode:
                mode=md
                output+=mode

            #time finalization: accumulated time, cut vs auto vs total
            if ylt2!='initialize' and power=='|power|ON' and ylt1!=ylt2:
                #accumulated time:total time
                if (ylt2-ylt1).total_seconds()>=0:
                    ylt+=(ylt2-ylt1).total_seconds()
                ylt1=ylt2
                if ylt>=0 and total_time!=str(int(ylt)):
                    total_time=str(int(ylt))
                    output+='|total_time|'+total_time
                if ylt<0:
                    ylt=float(0)


                #accumulated time:cut time
                if ct2!='initialize' and ex=='|exec|ACTIVE' and Srpm!='UNAVAILABLE' and float(Srpm.split('|')[-1])>0 and estop=='|estop|ARMED':
                    if (ct2-ct1).total_seconds()>=0:
                        ct+=(ct2-ct1).total_seconds()
                    ct1=ct2
                    if ct>=0 and cut_time!=str(int(ct)):
                        cut_time=str(int(ct))
                        output+='|cut_time|'+cut_time
                    if ct<0:
                        ct=float(0)

                #accumulated time:auto time
                if (at2!='initialize' and ex=='|exec|ACTIVE' or ex=='|exec|INTERRUPTED' or ex=='|exec|STOPPED' or float(Srpm.split('|')[-1])>0) and estop=='|estop|ARMED':
                    if (at2-at1).total_seconds()>=0:
                        at+=(at2-at1).total_seconds()
                    at1=at2
                    if at>=0 and auto_time!=str(int(at)):
                        auto_time=str(int(at))
                        output+='|auto_time|'+auto_time
                    if at<0:
                        at=float(0)



            if output and output!='initialize':
                out='\r\n'+datetime.datetime.now().isoformat()+'Z'+output
                conn.sendall(out)
                time.sleep(0.200)
        except:
            if output!='|power|OFF':
                out='\r\n'+datetime.datetime.now().isoformat()+'Z'+'|power|OFF'
                output='|power|OFF'
                ylt2='initialize'
                ct2='initialize'
                at2='initialize'

                try:
                    conn.sendall(out)
                except:
                    "Connection Failure"
            ylt1=datetime.datetime.now() #initialized
            at1=datetime.datetime.now() #initialized
            ct1=datetime.datetime.now() #initialized

    conn.close()

while True:
    try:
        conn, addr = s.accept()
        start_new_thread(new_client, (conn,))
    except:
        "Connection failed"


s.close()
