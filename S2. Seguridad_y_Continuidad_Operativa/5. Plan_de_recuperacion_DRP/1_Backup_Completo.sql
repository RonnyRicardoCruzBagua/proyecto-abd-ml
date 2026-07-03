USE master;
GO

BACKUP DATABASE HotelDB
TO DISK = 'C:\Backups\HotelDB_Full.bak'
WITH
FORMAT,
INIT,
NAME='Full Backup HotelDB',
STATS = 10;
GO

--