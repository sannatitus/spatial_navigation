robocopy "E:\Data\CrabStreams\Videos" "S:\raw\CrabLab\CrabitatCam_daily" /E /XD /log+:E:\Data\CrabStreams\Robocopy_weekly-upload\Robocopylog _%date:~-10,2%"-"%date:~7,2%"-"%date:~-4,4%.txt /v /tee 
