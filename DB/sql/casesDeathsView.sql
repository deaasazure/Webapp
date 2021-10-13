SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[casesDeathsView]
AS select  country , continent,year,month, SUM(cases) AS totalCases,SUM(deaths) AS totalDeaths
from [dbo].[ecdc.cases_deaths_tbl] 
group by country, continent,year,month
UNION ALL
select  country , null as continent, null as year, null as month, SUM(cases) AS totalCases,SUM(deaths) AS totalDeaths
from [dbo].[ecdc.cases_deaths_tbl]  
group by country
UNION ALL
select  null as country , continent, null as year, null as month, SUM(cases) AS totalCases,SUM(deaths) AS totalDeaths
from [dbo].[ecdc.cases_deaths_tbl]  
group by continent
UNION ALL
select  null as country , null as continent, year, null as month, SUM(cases) AS totalCases,SUM(deaths) AS totalDeaths
from [dbo].[ecdc.cases_deaths_tbl]  
group by year
UNION ALL
select  null as country , null as continent, null as year, month, SUM(cases) AS totalCases,SUM(deaths) AS totalDeaths
from [dbo].[ecdc.cases_deaths_tbl]  
group by month;
GO
