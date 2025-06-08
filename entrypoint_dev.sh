#!/bin/bash

/load_sqlite3.sh
/cert_gen.sh 
exec "$@"