USE master;
GO

BACKUP LOG HotelDB
TO DISK = 'C:\Backups\HotelDB_Log.trn'
WITH STATS = 10;
GO

--