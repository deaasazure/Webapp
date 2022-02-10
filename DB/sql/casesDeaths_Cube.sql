SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[casesDeaths_cube]
(
	[country] [varchar](8000) NULL,
	[continent] [varchar](8000) NULL,
	[year] [smallint] NULL,
	[month] [smallint] NULL,
	[totalCases] [bigint] NULL,
	[totalDeaths] [bigint] NULL,
	[yearMonth] [varchar](13) NOT NULL
)
WITH
(
	DISTRIBUTION = ROUND_ROBIN,
	CLUSTERED COLUMNSTORE INDEX
)
GO
