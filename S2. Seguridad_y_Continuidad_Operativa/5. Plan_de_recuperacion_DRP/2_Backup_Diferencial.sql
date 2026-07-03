USE master;
GO

BACKUP DATABASE HotelDB
TO DISK = 'C:\Backups\HotelDB_Diff.bak'
WITH
DIFFERENTIAL,
NAME='Differential Backup HotelDB',
STATS = 10;
GO

--