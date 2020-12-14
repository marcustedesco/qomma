#!/bin/sh

QUERY1="SELECT last_name,first_name from drivers where country='USA aNd first_name=john;\n"
QUERY2="SELECT *, id from drivers where id=3;\n"
QUERY3="SELECT * from shipments;\n"
QUIT="\q"

echo "${QUERY1}${QUERY2}${QUERY3}${QUIT}" | qomma csv_samples