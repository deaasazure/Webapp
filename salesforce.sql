
IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'salesforce' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [salesforce]' END
GO

/*
Table structure for table '[salesforce].[account]'
*/

IF OBJECT_ID ('[salesforce].[account]', 'U') IS NOT NULL
DROP TABLE [salesforce].[account];
GO
CREATE TABLE [salesforce].[account] (
	[accountnumber] NVARCHAR(MAX),
	[name] NVARCHAR(MAX)
)
GO

/*
Dumping data for table '[salesforce].[account]'
*/


INSERT INTO [salesforce].[account] ([accountnumber], [name]) VALUES (N'infosys', N'infosys'), (N'Logistics', N'Express'), (N'Express', N'Express'), (N'Logistics & Transport1', N'Express Logistics and Transport1')
GO

