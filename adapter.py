import time, linuxcnc, datetime
from data_item import Event, SimpleCondition, Sample
from mtconnect_adapter import Adapter

class pocketNCAdapter(object):
    
    def __init__(self, host, port):
        
        self.host = host
        self.port = port
        
        self.adapter = Adapter((host,port))

        self.auto_time = Sample('auto_time')
        self.adapter.add_data_item(self.auto_time)

        self.cut_time = Sample('cut_time')
        self.adapter.add_data_item(self.cut_time)

        self.total_time = Sample('total_time')
        self.adapter.add_data_item(self.total_time)

        self.Xabs = Sample('Xabs')
        self.adapter.add_data_item(self.Xabs)

        self.Yabs = Sample('Yabs')
        self.adapter.add_data_item(self.Yabs)
        
        self.Zabs = Sample('Zabs')
        self.adapter.add_data_item(self.Zabs)

        self.Aabs = Sample('Aabs')
        self.adapter.add_data_item(self.Aabs)

        self.Babs = Sample('Babs')
        self.adapter.add_data_item(self.Babs)

        self.Srpm = Sample('Srpm')
        self.adapter.add_data_item(self.Srpm)

        self.estop = Event('estop')
        self.adapter.add_data_item(self.estop)

        self.power = Event('power')
        self.adapter.add_data_item(self.power)

        self._exec = Event('exec')
        self.adapter.add_data_item(self._exec)

        self.line = Event('line')
        self.adapter.add_data_item(self.line)

        self.program = Event('program')
        self.adapter.add_data_item(self.program)

        self.Fovr = Event('Fovr')
        self.adapter.add_data_item(self.Fovr)

        self.Sovr = Event('Sovr')
        self.adapter.add_data_item(self.Sovr)

        self.Tool_number = Event('Tool_number')
        self.adapter.add_data_item(self.Tool_number)

        self.mode = Event('mode')
        self.adapter.add_data_item(self.mode)

        self.avail = Event('avail')
        self.adapter.add_data_item(self.avail)

        self.adapter.start()

        self.adapter.begin_gather()
        self.avail.set_value("AVAILABLE")
        self.adapter.complete_gather()

        self.adapter_stream()

    def data_pull(self):
        data = linuxcnc.stat()
        data.poll()
        return data

    def adapter_stream(self):

        at2='initialize'
        ct2='initialize'
        ylt2='initialize'
        ylt1=datetime.datetime.now() #initialized
        at1=datetime.datetime.now() #initialized
        ct1=datetime.datetime.now() #initialized
        ylt=float(0) #initialized
        at=float(0) #initialized
        ct=float(0) #initialized
        
        while True:
            try:
                data = self.data_pull()
                
                #time initialization: accumulated time: cut - auto - total
                if self.power.value() == 'ON':
                    ylt2=datetime.datetime.now()
                    if ex=='ACTIVE' and self.Srpm.value()!=None and float(self.Srpm.value())>0 and estop=='ARMED':
                        ct2=datetime.datetime.now()
                    else:
                        ct1=datetime.datetime.now()
                    if (ex=='ACTIVE' or ex=='STOPPED' or ex=='INTERRUPTED' or float(self.Srpm.value())>0) and estop=='ARMED':
                        at2=datetime.datetime.now()
                    else:
                        at1=datetime.datetime.now()
                else:
                    ylt1=datetime.datetime.now()



                if data.state==1:
                    ex='READY'
                elif data.state==2:
                    ex='ACTIVE'
                else:
                    ex=''

                self.adapter.begin_gather()
                self._exec.set_value(ex)
                self.adapter.complete_gather()

                if data.estop!=1:
                    estp='ARMED'
                else:
                    estp='TRIGGERED'

                self.adapter.begin_gather()
                self.estop.set_value(estp)
                self.adapter.complete_gather()


                self.adapter.begin_gather()
                #self.power.set_value(pwr)  #Not sure why this is not defined...
                self.adapter.complete_gather()
                
                self.adapter.begin_gather()
                xps=str(format(data.actual_position[0], '.4f'))
                self.Xabs.set_value(xps)
                yps=str(format(data.actual_position[1], '.4f'))
                self.Yabs.set_value(yps)
                zps=str(format(data.actual_position[2], '.4f'))
                self.Zabs.set_value(zps)
                abs=str(format(data.actual_position[3], '.4f'))
                self.Aabs.set_value(abs)
                bbs=str(format(data.actual_position[4], '.4f'))
                self.Babs.set_value(bbs)

                self.adapter.complete_gather()

                ssp=str(data.spindle_speed)
                self.adapter.begin_gather()
                self.Srpm.set_value(ssp)

                ln=str(data.motion_line)
                self.adapter.begin_gather()
                self.line.set_value(ln)

                pgm=str(data.file)
                self.adapter.begin_gather()
                self.program.set_value(pgm)

                pfo=str(data.feedrate*100)
                self.adapter.begin_gather()
                self.Fovr.set_value(pfo)

                so=str(data.spindlerate*100)
                self.adapter.begin_gather()
                self.Sovr.set_value(so)

                tooln=str(data.tool_in_spindle)
                self.adapter.begin_gather()
                self.Tool_number.set_value(tooln)
                self.adapter.complete_gather()

                if data.task_mode==1:
                    md='MDI'
                elif data.task_mode==2:
                    md='AUTOMATIC'
                elif data.task_mode==3:
                    md='MANUAL'
                else:
                    md=''

                self.adapter.begin_gather()
                self.mode.set_value(md)
                self.adapter.complete_gather()

                #time finalization: accumulated time, cut vs auto vs total
                if ylt2!='initialize' and self.power.value()=='ON' and ylt1!=ylt2:
                    #accumulated time:total time
                    if (ylt2-ylt1).total_seconds()>=0:
                        ylt+=(ylt2-ylt1).total_seconds()
                    ylt1=ylt2
                    if ylt>=0 and self.total_time.value()!=str(int(ylt)):
                        self.adapter.begin_gather()
                        self.total_time.set_value(str(int(ylt)))
                        self.adapter.complete_gather()
                    if ylt<0:
                        ylt=float(0)


                    #accumulated time:cut time
                    if ct2!='initialize' and ex=='ACTIVE' and self.Srpm.value()!=None and float(self.Srpm.value())>0 and self.estop.value()=='ARMED':
                        if (ct2-ct1).total_seconds()>=0:
                            ct+=(ct2-ct1).total_seconds()
                        ct1=ct2
                        if ct>=0 and self.cut_time.value()!=str(int(ct)):
                            self.adapter.begin_gather()
                            self.cut_time.set_value(str(int(ct)))
                            self.adapter.complete_gather()
                        if ct<0:
                            ct=float(0)

                    #accumulated time:auto time
                    if (at2!='initialize' and ex=='ACTIVE' or ex=='INTERRUPTED' or ex=='STOPPED' or float(self.Srpm.value())>0) and self.estop.value()=='ARMED':
                        if (at2-at1).total_seconds()>=0:
                            at+=(at2-at1).total_seconds()
                        at1=at2
                        if at>=0 and self.auto_time.value()!=str(int(at)):
                            self.adapter.begin_gather()
                            self.auto_time.set_value(str(int(at)))
                            self.adapter.complete_gather()
                        if at<0:
                            at=float(0)


            except:
                if self.power.value() and self.power.value()!='OFF':
                    self.adapter.begin_gather()
                    self.power.set_value('OFF')
                    self.adapter.complete_gather()
                    ylt2='initialize'
                    ct2='initialize'
                    at2='initialize'

                ylt1=datetime.datetime.now() #initialized
                at1=datetime.datetime.now() #initialized
                ct1=datetime.datetime.now() #initialized

if __name__ == "__main__":
    print "Starting Up"
    pocketNcadapter = pocketNCAdapter('localhost',7878)
    
