select set_type,
       set_name,
       scryfall_uri
from all_entries ae
left join oracle_entries oe on oe.oracle_id = ae.oracle_id