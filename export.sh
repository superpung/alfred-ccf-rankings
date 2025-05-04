if [ -d "dist" ]; then
    rm -r dist
fi
mkdir -p dist
zip -r ./dist/ccf-rankings.alfredworkflow ./*
