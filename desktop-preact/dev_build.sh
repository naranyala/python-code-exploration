#!/usr/bin/bash 

cd frontend 

echo "building frontend ..."
bun run build 

cd ..
echo "run aplication .."
uv run main.py 

echo "exit .."


