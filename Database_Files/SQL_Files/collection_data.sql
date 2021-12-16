select nt.collection_id,
       ae.name,
       ae.set_name,
       nt.Location,
       iif(nt.Foil, ae.usd_foil, ae.usd) as value,
       nt.Foil,
       nt.rarity,
       nt.cmc,
       nt.color_identity,
       nt.colors,
       nt.mana_cost,
       nt.type_line
from all_entries ae
inner join
(select c1.collection_id,
        c1.Location,
        c1.Foil,
        c1.scryfall_uri,
        oe.rarity,
        oe.cmc,
        oe.color_identity,
        oe.colors,
        oe.mana_cost,
        oe.type_line
from collection_1 c1
inner join oracle_entries oe on c1.oracle_id = oe.oracle_id
) nt on nt.scryfall_uri = ae.scryfall_uri