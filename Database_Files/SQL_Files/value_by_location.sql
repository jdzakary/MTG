select c1.Location,
       sum(iif(c1.Foil, ae.usd_foil, ae.usd)) as value,
       count(collection_id)
from collection_1 c1
inner join all_entries ae on ae.scryfall_uri = c1.scryfall_uri
where iif(c1.Foil, ae.usd_foil, ae.usd) > 1.5
group by Location