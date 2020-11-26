#!/bin/sh

echo "SELECT last_name,first_name from drivers where country='USA aNd first_name=john;\nSELECT *, id from drivers where id=3;\nSELECT * from shipments;\n\q" | ./qomma.py csv_samples/