SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROC [dbo].[ecdc.covid19_external_hospitals_to_db_prc] AS

BEGIN
/**********************************************************************************************
   NAME     :  [ecdc.covid19_external_hospitals_to_db_prc]
   PURPOSE  :  This sp is used to populate ecdc_covid_cases tables from external tables.
   REVISIONS:
   Ver        Date			Author                    Description
   ---------  ----------		---------------		------------------------------------
   1.0        02-Sep-2021		Mehul                Initial Version.

--EXEC [ecdc.covid19_external_hospitals_to_db_prc] 

**********************************************************************************************/  
DECLARE
@ldate date,
@lcount bigint,
@lerror varchar(max);

BEGIN TRY

select   @lcount = count(*)  from  [dbo].[ecdc.hospitals_icus_tbl];
        
IF @lcount>0 
BEGIN
delete from  [dbo].[ecdc.hospitals_icus_tbl];
END;

insert into [dbo].[ecdc.hospitals_icus_tbl]
select * from  ecdc.hospitals_icus_ext;

END TRY
BEGIN CATCH
SELECT @lerror = Error_Message()
select @lerror as errorMessage
END CATCH

END;
GO
