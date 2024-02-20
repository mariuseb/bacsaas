--select * from buildings order by id limit 10
--select * from buildings order by year_of_construction limit 10
--select * from buildings where year_of_construction = 2005 order by (location, floor_area)
--select year_of_construction, count(year_of_construction) from buildings group by year_of_construction order by year_of_construction

--select building_category from buildings
--select distinct building_category from buildings

--select count(id) from timeseries
--select * from timeseries limit 10

--select * from data_sources
--delete from data_sources where id = 18

--update data_sources set name = 'Firma AS' where id = 10
--update data_sources set phone = '900-55555' where name = 'Firma AS'
--delete from data_sources where name = 'Firma AS'