#!/bin/bash
echo "GET $1 HTTP/1.1
Host: example.local
Accept: application/json" | ncat -C 127.0.0.1 53210

