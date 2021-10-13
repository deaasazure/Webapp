SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ecdc.hospitals_icus_tbl]
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
WITH
(
	DISTRIBUTION = ROUND_ROBIN,
	CLUSTERED COLUMNSTORE INDEX
)
GO
