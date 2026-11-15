# -*- coding: utf-8 -*-
import re
import subprocess
import datetime
import time
import tweepy
import myConf
from recobuta import write_log

def do_hello(cmd, api):
    write_log('---> do_hello...')
    ans= myConf.doHello_reply
    return ans

def do_balus(cmd, api):
    write_log('---> do_balus...')
    ans= myConf.doBalus_reply + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    api.update_status(ans)
    time.sleep(15)
    write_log('-----> shutdown...')
    sys.exit(0)

def do_radiru(cmd, api):
    write_log('---> do_radiru...')
    CHANNEL= ['NHK1', 'NHK2', 'FM', 'NHK1_SENDAI', 'FM_SENDAI', 'NHK1_NAGOYA', 'FM_NAGOYA', 'NHK1_OSAKA', 'FM_OSAKA']

    if len(cmd) < 1:
        cmd[0]= 'hlp'

    if str(cmd[0]).lower() == 'hlp':
        write_log('-----> help...')
        ans= 'radiru function Usage...\n'
        ans+= 'rec [CHANNEL] [RECORDING TIME] [START DATE] [START TIME] [PREFIX]\n'
        ans+= 'can [at ID]\n'
        ans+= 'hlp'
        return ans

    if str(cmd[0]).lower() == 'rec':
        write_log('-----> rec...')
        nDateTime= datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        sDateTime= cmd[3] + ' ' + cmd[4]

      #C... Check FORMAT
        if not cmd[1].upper() in CHANNEL:
            ans= cmd[1] + ' is not active channel...\n'
            ans+= str(CHANNEL)
            return ans
        if not cmd[2].isdigit():
            ans= cmd[2] + ' is not integer...\n'
            ans+= 'RECODIUNG TIME is minits'
            return ans
        try:
            sTimeDate= datetime.datetime.strptime(sDateTime, '%Y/%m/%d %H:%M').strftime('%H:%M %d.%m.%y')
        except:
            ans= cmd[3] + ' ' + cmd[4] + ' is not correct Date/Time...\n'
            ans+= 'START DATE/TIME : YYYY/mm/dd HH:MM[:SS]' 
            return ans

      #C...To do 時刻比較

      #C... Make Command
        var= myConf.doRadiru_rec_script_path + ' '
        var+= cmd[1].upper() + ' ' + cmd[2] + ' '
        var+= myConf.doRadiru_rec_folder + ' '
        var+= cmd[5]

      #C... Output File
        afile= myConf.doRadiru_tmp_folder + '/_doRadiru.tmp'
        fp= open(afile, 'w')
        fp.write(var)
        fp.close()

      #C... Update at Commnad
        var= 'at ' + sTimeDate + ' -f ' + afile
        try:
            ret= subprocess.check_output(var, shell= True)
            ans= ret
        except:
            ans= 'cannot access(at command)...'
            return ans

      #C... Get ID from standard output

        return ans

    if str(cmd[0]).lower() == 'can':
        write_log('-----> can...')
        if not cmd[1].isdigit():
            ans= cmd[1] + ' is not integer...\n'
            return ans

        var= 'at -r ' + str(cmd[1])
        try:
            ret= subprocess.check_output(var, shell= True)
            ans= ret
        except:
            ans= 'cannot delete job...'

        return ans
            
    ans= u''
    return ans