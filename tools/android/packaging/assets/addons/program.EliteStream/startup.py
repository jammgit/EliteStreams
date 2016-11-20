import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
import threading
import datetime
from datetime import date
from resources.libs import extract, downloader, notify, traktit, skinSwitch, uploadLog, wizard as wiz
from resources.libs import check as ck

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = wiz.addonId(ADDON_ID)
VERSION        = wiz.addonInfo(ADDON_ID,'version')
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,     'addons')
USERDATA       = os.path.join(HOME,     'userdata')
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
PACKAGES       = os.path.join(ADDONS,   'packages')
ADDONDATA      = os.path.join(USERDATA, 'addon_data', ADDON_ID)
FANART         = os.path.join(PLUGIN,   'fanart.jpg')
ICON           = os.path.join(PLUGIN,   'icon.png')
ART            = os.path.join(PLUGIN,   'resources', 'art')
SKIN           = xbmc.getSkinDir()
BUILDNAME      = wiz.getS('buildname')
BUILDVERSION   = wiz.getS('buildversion')
BUILDLATEST    = wiz.getS('latestversion')
BUILDCHECK     = wiz.getS('lastbuildcheck')
KEEPTRAKT      = wiz.getS('keeptrakt')
TRAKTSAVE      = wiz.getS('lastsave')
INSTALLED      = wiz.getS('installed')
EXTRACT        = wiz.getS('extract')
EXTERROR       = wiz.getS('errors')
NOTIFY         = wiz.getS('notify')
NOTEID         = wiz.getS('noteid') 
NOTEID         = 0 if NOTEID == "" else int(NOTEID)
NOTEDISMISS    = wiz.getS('notedismiss')
TODAY          = datetime.date.today()
TOMORROW       = TODAY + datetime.timedelta(days=1)
THREEDAYS      = TODAY + datetime.timedelta(days=3)
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
EXCLUDES       = uservar.EXCLUDES
BUILDFILE      = uservar.BUILDFILE
UPDATECHECK    = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK      = TODAY + datetime.timedelta(days=UPDATECHECK)
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
AUTOUPDATE     = uservar.AUTOUPDATE
WIZARDFILE     = uservar.WIZARDFILE
WORKING        = wiz.workingURL(BUILDFILE)

###########################
#### Check Updates   ######
###########################

ck.Access()
ck.END()

def checkUpdate():
    BUILDNAME      = wiz.getS('buildname')
    BUILDVERSION   = wiz.getS('buildversion')
    version        = wiz.checkBuild(BUILDNAME, 'version')
    wiz.setS('latestversion', version)
    t = threading.Timer(30.0, checkUpdate)
    if version > BUILDVERSION:	
		t.start()
		yes_pressed = DIALOG.yesno(ADDONTITLE,"New version of your current build avaliable: %s v%s" % (BUILDNAME, version), "Choose a build to Download.", "[COLOR=red]DON'T EXIT THE INSTALLATION![/COLOR]", yeslabel="[COLOR=red]Adult[/COLOR]", nolabel="Normal")
		if yes_pressed:
			xbmc.executebuiltin('PlayMedia(plugin://program.EliteStream/?mode=install&name=EliteStream&url=adult)')
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			t.cancel()
		else: 
			xbmc.executebuiltin('PlayMedia(plugin://program.EliteStream/?mode=install&name=EliteStream&url=normal)')
			wiz.setS('lastbuildcheck', str(NEXTCHECK))  
			t.cancel() 

while xbmc.Player().isPlayingVideo():
	time.sleep(1)
			
if AUTOUPDATE == 'Yes':
	if wiz.workingURL(WIZARDFILE):
		ver = wiz.checkWizard('version')
		zip = wiz.checkWizard('zip')
		if ver > VERSION:
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE, 'There is a new version of the %s!' % ADDONTITLE, 'Please download v%s' % ver)
			DP.create(ADDONTITLE,'Downloading Update...','', 'Please Wait')
			lib=os.path.join(PACKAGES, '%s-%s.zip' % (ADDON_ID, ver))
			try: os.remove(lib)
			except: pass
			downloader.download(zip, lib, DP)
			time.sleep(2)
			DP.update(0,"", "Installing %s update" % ADDONTITLE)
			ext = extract.all(lib, ADDONS, DP)
			DP.close()
			wiz.forceUpdate()
			wiz.LogNotify(ADDONTITLE,'Add-on updated')
	else: wiz.log("URL FOR WIZARDFILE INVALID: %s" % WIZARDFILE)
		
if ENABLE == 'Yes' and NOTIFY == 'false':
	url = wiz.workingURL(NOTIFICATION)
	if url == True:
		link  = wiz.openURL(NOTIFICATION).replace('\r','').replace('\t','')
		id, msg = link.split('|||')
		if int(id) == NOTEID:
			if NOTEDISMISS == 'false':
				notify.Notification(msg=msg, title=ADDONTITLE, BorderWidth=10)
			else: xbmc.log("Notifications id[%s] Dismissed" % int(id))
		elif int(id) > NOTEID:
			xbmc.log("Notifications id: %s" % str(int(id)))
			wiz.setS('noteid', str(int(id)))
			wiz.setS('notedismiss', 'false')
			openit=notify.Notification(msg=msg, title=ADDONTITLE, BorderWidth=10)			
			wiz.log("Notifications: Complete")
	else: wiz.log("Notifications URL(%s): %s" % (NOTIFICATION, url))
elif not ENABLE == 'Yes': wiz.log("Notifications: Not Enabled")
elif NOTIFY == 'true': wiz.log("Notifications: Turned Off")
			
if INSTALLED == 'true':
	if not EXTRACT == '100':
		yes=DIALOG.yesno(ADDONTITLE, '%s was not installed correctly!' % BUILDNAME, 'Installed: %s / Error Count:%s' % (EXTRACT, EXTERROR), 'Would you like to try again?', nolabel='No Thanks!', yeslabel='Yes Please!')
		if yes: xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=fresh)" % (ADDON_ID, urllib.quote_plus(BUILDNAME)))
	elif SKIN in ['skin.confluence', 'skin.estuary']:
		yes=DIALOG.yesno(ADDONTITLE, '%s was not installed correctly!' % BUILDNAME, 'It looks like the skin settings was not applied to the build.', 'Would you like to apply the guiFix?', nolabel='No Thanks!', yeslabel='Yes Please!')
		if yes: xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=gui)" % (ADDON_ID, urllib.quote_plus(BUILDNAME)))
	if KEEPTRAKT == 'true': traktit.traktIt('restore', 'all')
	wiz.clearS('install')

if not WORKING:
	wiz.log("Not a valid URL for Build File: %s" % BUILDFILE)
elif BUILDCHECK == '' and BUILDNAME == '':
    yes_pressed = DIALOG.yesno(ADDONTITLE,"Currently no build installed from %s." % ADDONTITLE, "Select a build to install.", "[COLOR=red]DON'T EXIT THE INSTALLATION![/COLOR]", yeslabel="[COLOR=red]Adult[/COLOR]", nolabel="Normal")
    if yes_pressed:	
		xbmc.executebuiltin('PlayMedia(plugin://program.EliteStream/?mode=install&name=EliteStream&url=adult)')
		wiz.setS('lastbuildcheck', str(NEXTCHECK)) 
    else:
		xbmc.executebuiltin('PlayMedia(plugin://program.EliteStream/?mode=install&name=EliteStream&url=normal)')
		wiz.setS('lastbuildcheck', str(NEXTCHECK)) 
elif not BUILDCHECK > str(TODAY) and not BUILDNAME == '':
		wiz.setS('lastbuildcheck', str(NEXTCHECK)); checkUpdate()
	
if KEEPTRAKT == 'true':
	if TRAKTSAVE == '' or not TRAKTSAVE > str(TODAY):
		traktit.traktIt('update' , 'all')
		wiz.setS('lastsave', str(THREEDAYS))