#!/bin/bash
echo "Starting Flask app..."
echo "PORT: $PORT"
echo "Environment variables:"
env | grep PORT
python -m flask run --host=0.0.0.0 --port=$PORT
