select nt.collection_id,
       ae.name,
       ae.set_name,
       nt.Location,
       iif(nt.Foil, ae.usd_foil, ae.usd) as value
from all_entries ae
inner join
(select c1.collection_id,
        c1.Location,
        c1.Foil,
        oe.rarity,
        c1.scryfall_uri
from collection_1 c1
inner join oracle_entries oe on c1.oracle_id = oe.oracle_id
) nt on nt.scryfall_uri = ae.scryfall_uri