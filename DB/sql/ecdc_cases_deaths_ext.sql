SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO
CREATE EXTERNAL TABLE [ecdc].[cases_deaths_ext]
(
	[country] [varchar](8000) NULL,
	[continent] [varchar](8000) NULL,
	[source] [varchar](8000) NULL,
	[population] [varchar](8000) NULL,
	[year_week] [varchar](10) NULL,
	[country_code] [varchar](8000) NULL,
	[year] [smallint] NULL,
	[month] [smallint] NULL,
	[yearMonth] [varchar](10) NULL,
	[cases] [bigint] NULL,
	[deaths] [bigint] NULL
)
WITH (DATA_SOURCE = [ecdc_curated_ds],LOCATION = N'ecdc/cases/*.parquet',FILE_FORMAT = [ecdc_parquet_format],REJECT_TYPE = VALUE,REJECT_VALUE = 0)
GO
