USE master;
GO

RESTORE DATABASE HotelDB
FROM DISK='C:\Backups\HotelDB_Full.bak'
WITH NORECOVERY;
GO

RESTORE DATABASE HotelDB
FROM DISK='C:\Backups\HotelDB_Diff.bak'
WITH NORECOVERY;
GO

RESTORE LOG HotelDB
FROM DISK='C:\Backups\HotelDB_Log.trn'
WITH RECOVERY;
GO                  

--