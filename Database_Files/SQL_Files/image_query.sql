select ae.set_type,
       ae.set_name,
       oe.type_line,
       ae.scryfall_uri,
       ae.image_url_1,
       ae.image_url_2
from all_entries ae
left join oracle_entries oe on ae.oracle_id = oe.oracle_id
where downloaded = FALSE