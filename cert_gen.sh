#!/bin/sh

CERT_DIR=/certs
KEY_FILE=$CERT_DIR/server.key
CERT_FILE=$CERT_DIR/server.cert

# Create folder certs if does not exist
mkdir -p $CERT_DIR

# Generate certificates only if they do not exist
if [ ! -f "$KEY_FILE" ] || [ ! -f "$CERT_FILE" ]; then
  echo "Generating SSL certificates..."
  openssl req -x509 -newkey rsa:4096 -nodes \
    -keyout "$KEY_FILE" -out "$CERT_FILE" \
    -days 365 \
    -subj "/C=PL/ST=Test/L=Test/O=Test/CN=localhost"
else
  echo "SSL certificates already exist."
fi

# Run main process
exec "$@"