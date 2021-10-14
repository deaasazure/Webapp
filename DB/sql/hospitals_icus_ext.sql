SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO
CREATE EXTERNAL TABLE [dbo].[ecdc.hospitals_icus_ext]
(
	[country] [varchar](8000) NULL,
	[year_week] [varchar](10) NULL,
	[source] [varchar](8000) NULL,
	[url] [varchar](8000) NULL,
	[year] [smallint] NULL,
	[months] [smallint] NULL,
	[date] [date] NULL,
	[icu_count] [float] NULL,
	[hospital_count] [float] NULL
)
WITH (DATA_SOURCE = [ecdc_curated_ds],LOCATION = N'ecdc/hospitals/*.parquet',FILE_FORMAT = [ecdc_parquet_format],REJECT_TYPE = VALUE,REJECT_VALUE = 0)
GO
