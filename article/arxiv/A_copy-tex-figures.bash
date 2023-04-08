## create files path
mkdir -p files

## copy tex file
cp ../latex/main.tex files

## copy relevant *.cls files
cp ../latex/*.cls files

## cp image files to arxiv path
cp ../figures/main-results/outputs/drawing-v00.png files/main-fig-results.png
