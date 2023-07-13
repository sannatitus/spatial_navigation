# Automatic weekly rsync of daily husbandry videos to the ceph | last updated by Sanna, 13/7/23 s.titus@ucl.ac.uk

## The robocopy-code.bat is a batch script that will upload the data within E:\CrabStreams\Videos to the ceph, at \CrabLab\CrabitatCam_daily\. For this to occur automatically, the .bat is powered by Windows Task Scheduler (the event 'Automatic weekly rsync of daily husbandry videos to the ceph') must be enabled and the ceph must be mounted to drive letter S: (if this changes, simply edit the robocopy-script.bat). 
