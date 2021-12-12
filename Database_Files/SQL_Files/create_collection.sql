create table {0}
(
	collection_id integer
		constraint collection_2_pk
			primary key autoincrement,
	scryfall_uri text
		constraint collection_2_all_entries_scryfall_uri_fk
			references all_entries,
	oracle_id text
		constraint collection_2_oracle_entries_oracle_id_fk
			references oracle_entries,
	Location text,
	purchased real,
	Foil boolean
);