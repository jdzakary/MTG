select ti.*,
       oe.oracle_text_1,
       oe.oracle_text_2
from oracle_entries oe
inner join
(select c1.scryfall_uri,
       c1.oracle_id,
       ae.name,
       ae.set_name,
       ae.set_type,
       c1.Location,
       iif(c1.Foil, ae.usd_foil, ae.usd) as value,
       c1.purchased,
       c1.Foil
from {0} c1
inner join all_entries ae on ae.scryfall_uri = c1.scryfall_uri
where c1.collection_id = {1}) ti on ti.oracle_id = oe.oracle_id