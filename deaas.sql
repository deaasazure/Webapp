/*
File name: D:/Webapp/citus.sql
Creation date: 02/09/2022
Created by PostgreSQL to MSSQL 3.1 [Demo]
--------------------------------------------------
More conversion tools at http://www.convert-in.com
*/
SET QUOTED_IDENTIFIER ON;
GO
IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'mlaas' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [mlaas]' END
GO

/*
Table structure for table '[mlaas].[activity_detail_tbl]'
*/

IF OBJECT_ID ('[mlaas].[activity_detail_tbl]', 'U') IS NOT NULL
DROP TABLE [mlaas].[activity_detail_tbl];
GO
CREATE TABLE [mlaas].[activity_detail_tbl] (
	[detail_id] BIGINT IDENTITY NOT NULL,
	[activity_id] NVARCHAR(MAX),
	[user_name] NVARCHAR(MAX),
	[project_id] BIGINT,
	[dataset_id] BIGINT,
	[activity_description] NVARCHAR(MAX),
	[start_time] DATETIME2 NOT NULL DEFAULT CURRENT_TIMESTAMP,
	[end_time] DATETIME2,
	[column_id] NVARCHAR(MAX),
	[parameters] NVARCHAR(MAX)
)
GO

/*
Dumping data for table '[mlaas].[activity_detail_tbl]'
*/

SET IDENTITY_INSERT [mlaas].[activity_detail_tbl] ON;
GO
INSERT INTO [mlaas].[activity_detail_tbl] ([detail_id], [activity_id], [user_name], [project_id], [dataset_id], [activity_description], [start_time], [end_time], [column_id], [parameters]) VALUES (109, N'dp_71', N'mehul', 5, 8, N'Mode imputation', '2021-12-13 06:00:51.780183', NULL, NULL, NULL), (110, N'dp_101', N'mehul', 5, 8, N'Frequent Category Imputation', '2021-12-13 06:00:51.803853', NULL, NULL, NULL), (111, N'dp_291', N'mehul', 5, 8, N'One hot encoding', '2021-12-13 06:00:51.826219', NULL, NULL, NULL), (112, N'dp_521', N'mehul', 5, 8, N'Train-test split', '2021-12-13 06:00:51.855389', NULL, NULL, N'{"train":0.80,"test":0.20}')
GO

SET IDENTITY_INSERT [mlaas].[activity_detail_tbl] OFF;
GO
IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'mlaas' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [mlaas]' END
GO

/*
Table structure for table '[mlaas].[activity_master_tbl]'
*/

IF OBJECT_ID ('[mlaas].[activity_master_tbl]', 'U') IS NOT NULL
DROP TABLE [mlaas].[activity_master_tbl];
GO
CREATE TABLE [mlaas].[activity_master_tbl] (
	[master_id] INT IDENTITY NOT NULL,
	[activity_id] NVARCHAR(MAX),
	[activity_name] NVARCHAR(MAX),
	[activity_description] NVARCHAR(MAX),
	[lang] NVARCHAR(MAX),
	[operation] NVARCHAR(MAX),
	[code] BIGINT,
	[parent_activity_id] BIGINT,
	[user_input] BIGINT,
	[check_type] BIGINT
)
GO

/*
Dumping data for table '[mlaas].[activity_master_tbl]'
*/

SET IDENTITY_INSERT [mlaas].[activity_master_tbl] ON;
GO
INSERT INTO [mlaas].[activity_master_tbl] ([master_id], [activity_id], [activity_name], [activity_description], [lang], [operation], [code], [parent_activity_id], [user_input], [check_type]) VALUES (82, N'dp_401', N'Change column datatype', N'operation on column * in process', N'US', N'Operation', 1, 1, 1, 0), (84, N'dp_511', N'Handle missing value of target column', N'operation on column * in process', N'US', N'Operation', 1, 1, 1, 0), (17, N'dp_51', N'Mean Imputation', N'operation on column * in process', N'US', N'Operation', 1, 1, 0, 0), (20, N'dp_61', N'Median Imputation', N'operation on column * in process', N'US', N'Operation', 1, 1, 0, 0), (23, N'dp_71', N'Mode Imputation', N'operation on column * in process', N'US', N'Operation', 1, 1, 0, 0), (26, N'dp_81', N'Arbitarry Value Imputation', N'operation on column * in process', N'US', N'Operation', 1, 1, 1, 2), (32, N'dp_101', N'Frequent Category Imputation', N'operation on column * in process', N'US', N'Operation', 1, 1, 0, 0), (83, N'dp_501', N'Select target column', N'operation on column * in process', N'US', N'Operation', 1, 1, 1, 0), (85, N'dp_521', N'Train-test split', N'operation on column * in process', N'US', N'Operation', 1, 10, 1, 0), (62, N'dp_201', N'Remove outliers using Z-score Detection Method', N'operation on column * in process', N'US', N'Operation', 1, 3, 0, 0), (71, N'dp_221', N'Replace Outliers with Mean using Z-score Detection', N'operation on column * in process', N'US', N'Operation', 1, 3, 0, 0)
GO

INSERT INTO [mlaas].[activity_master_tbl] ([master_id], [activity_id], [activity_name], [activity_description], [lang], [operation], [code], [parent_activity_id], [user_input], [check_type]) VALUES (73, N'dp_231', N'drop column', N'operation on column * in process', N'US', N'Operation', 1, 8, 1, 0), (74, N'dp_241', N'Add new column with same value', N'operation on column * in process', N'US', N'Operation', 1, 8, 1, 0), (75, N'dp_251', N'Remove outliers using IQR Detection Method', N'operation on column * in process', N'US', N'Operation', 1, 8, 1, 0), (76, N'dp_261', N'Replae outliers by mean using IQR Detection Method', N'operation on column * in process', N'US', N'Operation', 1, 8, 1, 0), (77, N'dp_271', N'Drop duplicates', N'operation on column * in process', N'US', N'Operation', 1, 8, 1, 0), (78, N'dp_281', N'Rename column', N'operation on column * in process', N'US', N'Operation', 1, 8, 1, 0), (79, N'dp_291', N'One-hot Encoding', N'operation on column * in process', N'US', N'Operation', 1, 5, 1, 0), (80, N'dp_301', N'Normalization feature scaling', N'operation on column * in process', N'US', N'Operation', 1, 4, 1, 0), (81, N'dp_1', N'Disard missing value', N'operation on column * in process', N'US', N'Operation', 1, 1, 1, 0)
GO

SET IDENTITY_INSERT [mlaas].[activity_master_tbl] OFF;
GO
IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'mlaas' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [mlaas]' END
GO

/*
Table structure for table '[mlaas].[dataset_explore_tbl]'
*/

IF OBJECT_ID ('[mlaas].[dataset_explore_tbl]', 'U') IS NOT NULL
DROP TABLE [mlaas].[dataset_explore_tbl];
GO
CREATE TABLE [mlaas].[dataset_explore_tbl] (
	[dataset_id] BIGINT,
	[project_id] BIGINT,
	[column_name] NVARCHAR(MAX),
	[mean_val] FLOAT,
	[std_dev] FLOAT,
	[min_val] FLOAT,
	[max_val] FLOAT,
	[percent_25] FLOAT,
	[percent_50] FLOAT,
	[percent_75] FLOAT,
	[null_val] FLOAT,
	[non_val] FLOAT,
	[data_count] FLOAT,
	[missing_val] FLOAT,
	[open_val] FLOAT,
	[close_val] FLOAT,
	[outliers_val] NVARCHAR(MAX),
	[columns_dtypes] NVARCHAR(MAX),
	[duplicates_val] BIGINT,
	[duplicate_entries_val] NVARCHAR(MAX),
	[correlation_val] NVARCHAR(MAX),
	[value_counts_val] NVARCHAR(MAX),
	[created_by] BIGINT,
	[created_on] DATETIMEOFFSET NOT NULL DEFAULT getdate()
)
GO

/*
Dumping data for table '[mlaas].[dataset_explore_tbl]'
*/

IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'mlaas' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [mlaas]' END
GO

/*
Table structure for table '[mlaas].[dataset_tbl]'
*/

IF OBJECT_ID ('[mlaas].[dataset_tbl]', 'U') IS NOT NULL
DROP TABLE [mlaas].[dataset_tbl];
GO
CREATE TABLE [mlaas].[dataset_tbl] (
	[dataset_id] BIGINT IDENTITY NOT NULL,
	[dataset_name] NVARCHAR(MAX),
	[project_id] BIGINT,
	[file_name] NVARCHAR(MAX),
	[dataset_file_path] NVARCHAR(MAX),
	[created_by] BIGINT,
	[created_on] DATETIMEOFFSET NOT NULL DEFAULT getdate(),
	[targetcolumn] NVARCHAR(MAX),
	[targetcolumn_behaviour] NVARCHAR(MAX)
)
GO

/*
Dumping data for table '[mlaas].[dataset_tbl]'
*/

SET IDENTITY_INSERT [mlaas].[dataset_tbl] ON;
GO
INSERT INTO [mlaas].[dataset_tbl] ([dataset_id], [dataset_name], [project_id], [file_name], [dataset_file_path], [created_by], [created_on], [targetcolumn], [targetcolumn_behaviour]) VALUES (6, N'hospitals_icus', 1, N'https://opendata.ecdc.europa.eu/covid19/hospitalicuadmissionrates/csv/data.csv', N'/mnt/deaas/stage/projects/ecdc/datasets/hospitals_icus/raw', 1, '2021-11-23 16:28:01.562581', NULL, NULL), (7, N'cases_deaths', 1, N'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv', N'/mnt/deaas/stage/projects/ecdc/datasets/cases_deaths/raw', 1, '2021-11-23 16:28:38.362798', NULL, NULL), (8, N'covid19', 5, N'https://covid.ourworldindata.org/data/owid-covid-data.csv', N'/mnt/deaas/stage/projects/owid_covid19/datasets/covid19/raw', 1, '2021-11-25 10:42:33.535673', N'total_cases', N'regression'), (9, N'fraudCalls', 7, NULL, N'/mnt/deaas/stage/projects/calls/datasets/fraudCalls/raw', 0, '2021-12-13 07:08:37.020515', NULL, NULL), (21, N'cases_deaths', 8, N'covid19', N'stage/projects/ecdc/datasets/cases_deaths/new', 1, '2022-02-08 14:01:21.875738', NULL, NULL), (22, N'hospital_icu', 9, N'hospital_icu', N'stage/projects/ecdc/datasets/cases_deaths/new', 1, '2022-02-08 16:37:16.782778', NULL, NULL), (23, N'testing', 9, N'covid_Testing', N'stage/projects/ecdc/datasets/cases_deaths/new', 1, '2022-02-09 06:39:57.368532', NULL, NULL)
GO

SET IDENTITY_INSERT [mlaas].[dataset_tbl] OFF;
GO
IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'mlaas' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [mlaas]' END
GO

/*
Table structure for table '[mlaas].[dataset_transform_rules_tbl]'
*/

IF OBJECT_ID ('[mlaas].[dataset_transform_rules_tbl]', 'U') IS NOT NULL
DROP TABLE [mlaas].[dataset_transform_rules_tbl];
GO
CREATE TABLE [mlaas].[dataset_transform_rules_tbl] (
	[transform_id] BIGINT IDENTITY NOT NULL,
	[project_id] BIGINT,
	[dataset_id] BIGINT,
	[operation] NVARCHAR(MAX),
	[select_cols] NVARCHAR(MAX),
	[source_tbl] NVARCHAR(MAX),
	[where_clause] NVARCHAR(MAX),
	[group_by] NVARCHAR(MAX),
	[having_clause] NVARCHAR(MAX),
	[dest_tbl] NVARCHAR(MAX),
	[order_seq] NVARCHAR(MAX),
	[created_by] BIGINT,
	[created_on] DATETIMEOFFSET NOT NULL DEFAULT getdate()
)
GO

/*
Dumping data for table '[mlaas].[dataset_transform_rules_tbl]'
*/

SET IDENTITY_INSERT [mlaas].[dataset_transform_rules_tbl] ON;
GO
INSERT INTO [mlaas].[dataset_transform_rules_tbl] ([transform_id], [project_id], [dataset_id], [operation], [select_cols], [source_tbl], [where_clause], [group_by], [having_clause], [dest_tbl], [order_seq], [created_by], [created_on]) VALUES (1, 1, 6, N'read', N'*', N'N', N'N', N'N', N'N', N'hospitalIcu_All', N'1', 1, '2021-11-24 10:32:24.347813'), (2, 1, 6, N'select', N'country,year_week,sum(case when indicator=''Daily ICU occupancy'' then value else 0 end) icu,sum(case when indicator=''Daily hospital occupancy'' then value else 0 end) hospital,url,source', N'hospitalIcu_All', N'(indicator=''Daily ICU occupancy'' or indicator==''Daily hospital occupancy'')', N'country,year_week,url,source', N'N', N'hospitalIcu_v', N'2', 1, '2021-11-24 10:41:41.137011'), (3, 1, 6, N'select', N'cdv.*,substring(cdv.year_week,1,4) as years,extract(month from date_add(to_date(concat(substring(cdv.year_week,1,4),''-01-01''),''yyyy-MM-dd''),cast(substring(cdv.year_week,7,8) as integer)*6)) as months,concat(substring(cdv.year_week,1,4),''-'',extract(month from date_add(to_date(concat(substring(cdv.year_week,1,4),''-01-01''),''yyyy-MM-dd''),cast(substring(cdv.year_week,7,8) as integer)*6))) yearMonth', N'hospitalIcu_v cdv', N'N', N'N', N'N', N'hospitalIcu_final', N'3', 1, '2021-11-24 10:45:33.721995'), (4, 1, 6, N'write', N'*', N'hospitalIcu_final', N'N', N'N', N'N', N'N', N'4', 1, '2021-11-24 10:51:34.765367'), (5, 1, 7, N'read', N'*', N'N', N'N', N'N', N'N', N'cases_all', N'1', 1, '2021-11-24 18:17:21.633264'), (7, 1, 7, N'write', N'N', N'cases_v', N'N', N'N', N'N', N'cases_final', N'3', 1, '2021-11-24 18:24:20.102674'), (10, 7, 9, N'read', N'N', N'N', N'N', N'N', N'N', N'calls_v1', N'1', 1, '2021-12-13 07:18:18.127471'), (11, 7, 9, N'read', N'N', N'N', N'N', N'N', N'N', N'calls_v2', N'2', 1, '2021-12-13 07:18:18.199263'), (12, 7, 9, N'select', N'CS1.year,CS1.month,CS1.day,CS1.hour, COUNT(*) AS FraudulentCalls', N'calls_v1 CS1, calls_v2 CS2', N'CS1.CallingIMSI = CS2.CallingIMSI AND abs(CS1.day- CS2.day) BETWEEN 1 AND 5 and CS1.SwitchNum != CS2.SwitchNum and  CS1.year= CS2.year and  CS1.month=CS2.month', N'CS1.year,CS1.month,CS1.day,CS1.hour', N'N', N'fraudCalls_v', N'3', 1, '2021-12-13 07:28:45.456470'), (13, 7, 9, N'write', N'N', N'fraudCalls_v', N'N', N'N', N'N', N'N', N'4', 1, '2021-12-13 07:41:29.484618'), (6, 1, 7, N'select', N'year years,month months,countriesAndTerritories country,countryterritoryCode country_code,continentExp continent,sum(cases) cases,sum(deaths) deaths,concat(year,''-'',month) yearMonth', N'cases_all', N'N', N'countryterritoryCode,countriesAndTerritories,continentExp,year,month', N'N', N'cases_v', N'2', 1, '2021-11-24 18:20:32.083621')
GO

SET IDENTITY_INSERT [mlaas].[dataset_transform_rules_tbl] OFF;
GO
IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'mlaas' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [mlaas]' END
GO

/*
Table structure for table '[mlaas].[parent_activity_tbl]'
*/

IF OBJECT_ID ('[mlaas].[parent_activity_tbl]', 'U') IS NOT NULL
DROP TABLE [mlaas].[parent_activity_tbl];
GO
CREATE TABLE [mlaas].[parent_activity_tbl] (
	[parent_activity_id] BIGINT,
	[parent_activity_name] NVARCHAR(MAX),
	[order_seq] BIGINT
)
GO

/*
Dumping data for table '[mlaas].[parent_activity_tbl]'
*/

SET IDENTITY_INSERT [mlaas].[parent_activity_tbl] ON;
GO
INSERT INTO [mlaas].[parent_activity_tbl] ([parent_activity_id], [parent_activity_name], [order_seq]) VALUES (1, N'Missing Value Handling', 1), (2, N'Noise Handling', 2), (3, N'Outlier Handling', 3), (4, N'Scaling', 4), (5, N'Encoding', 5), (6, N'Math Operations', 6), (7, N'Transformations', 7), (8, N'Feature Engineering', 8), (9, N'Duplicate Data Handling', 9), (10, N'Spliting', 10)
GO

SET IDENTITY_INSERT [mlaas].[parent_activity_tbl] OFF;
GO
IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'mlaas' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [mlaas]' END
GO

/*
Table structure for table '[mlaas].[project_tbl]'
*/

IF OBJECT_ID ('[mlaas].[project_tbl]', 'U') IS NOT NULL
DROP TABLE [mlaas].[project_tbl];
GO
CREATE TABLE [mlaas].[project_tbl] (
	[project_id] BIGINT IDENTITY NOT NULL,
	[project_name] NVARCHAR(MAX),
	[project_desc] NVARCHAR(MAX),
	[created_by] BIGINT,
	[created_on] DATETIMEOFFSET NOT NULL DEFAULT getdate()
)
GO

/*
Dumping data for table '[mlaas].[project_tbl]'
*/

SET IDENTITY_INSERT [mlaas].[project_tbl] ON;
GO
INSERT INTO [mlaas].[project_tbl] ([project_id], [project_name], [project_desc], [created_by], [created_on]) VALUES (1, N'ecdc', N'ecdc covid19', 1, '2021-11-23 16:11:04.429711'), (2, N'ecdc', N'ecdc covid19', 1, '2021-11-24 06:32:33.147489'), (3, N'ecdc', N'ecdc covid19', 1, '2021-11-24 11:11:03.841953'), (4, N'ecdc', N'ecdc covid19', 1, '2021-11-24 12:27:04.027080'), (5, N'owid_covid19', N'owid_covid19', 1, '2021-11-25 10:42:25.289984'), (6, N'owid', N'owid', 1, '2021-11-25 10:43:37.655953'), (7, N'calls', N'find fraud calls', 1, '2021-12-13 06:28:10.338912'), (8, N'ecdc_covid', N'covid19 of ecdc', 1, '2022-02-08 10:40:13.743030'), (9, N'ecdc_hospital', N'Hospital of ecdc', 1, '2022-02-08 16:35:21.706088')
GO

SET IDENTITY_INSERT [mlaas].[project_tbl] OFF;
GO
IF NOT EXISTS (SELECT  SCHEMA_NAME FROM    INFORMATION_SCHEMA.SCHEMATA WHERE   SCHEMA_NAME = 'mlaas' ) BEGIN EXEC sp_executesql N'CREATE SCHEMA [mlaas]' END
GO

/*
Table structure for table '[mlaas].[user_auth_tbl]'
*/

IF OBJECT_ID ('[mlaas].[user_auth_tbl]', 'U') IS NOT NULL
DROP TABLE [mlaas].[user_auth_tbl];
GO
CREATE TABLE [mlaas].[user_auth_tbl] (
	[uid] BIGINT IDENTITY NOT NULL,
	[user_name] NVARCHAR(MAX),
	[password] NVARCHAR(MAX),
	[first_name] NVARCHAR(MAX),
	[last_name] NVARCHAR(MAX),
	[email_id] NVARCHAR(MAX),
	[source] NVARCHAR(MAX),
	[created_on] DATETIMEOFFSET NOT NULL DEFAULT getdate()
)
GO

/*
Dumping data for table '[mlaas].[user_auth_tbl]'
*/

SET IDENTITY_INSERT [mlaas].[user_auth_tbl] ON;
GO
INSERT INTO [mlaas].[user_auth_tbl] ([uid], [user_name], [password], [first_name], [last_name], [email_id], [source], [created_on]) VALUES (1, N'mehul', N'mehul', N'Mehulsinh', N'Vaghela', N'mehulsinh.vaghela@vedity.com', N'internal', '2021-11-22 14:53:14.421102')
GO

SET IDENTITY_INSERT [mlaas].[user_auth_tbl] OFF;
GO
DROP SEQUENCE IF EXISTS [dbo].[activity_master_tbl_master_id_seq]
GO
CREATE SEQUENCE [dbo].[activity_master_tbl_master_id_seq] START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647
GO
DROP SEQUENCE IF EXISTS [dbo].[activity_detail_tbl_detail_id_seq]
GO
CREATE SEQUENCE [dbo].[activity_detail_tbl_detail_id_seq] START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647
GO
DROP SEQUENCE IF EXISTS [dbo].[dataset_tbl_dataset_id_seq]
GO
CREATE SEQUENCE [dbo].[dataset_tbl_dataset_id_seq] START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647
GO
DROP SEQUENCE IF EXISTS [dbo].[user_auth_tbl_uid_seq]
GO
CREATE SEQUENCE [dbo].[user_auth_tbl_uid_seq] START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647
GO
DROP SEQUENCE IF EXISTS [dbo].[dataset_transform_rules_tbl_transform_id_seq]
GO
CREATE SEQUENCE [dbo].[dataset_transform_rules_tbl_transform_id_seq] START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647
GO
DROP SEQUENCE IF EXISTS [dbo].[project_tbl_project_id_seq]
GO
CREATE SEQUENCE [dbo].[project_tbl_project_id_seq] START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647
GO


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

