# get the anime dataset... this is a pain because its on GDRIVE. The solution comes from:
# https://gist.github.com/tanaikech/f0f2d122e05bf5f971611258c22c110f

# USING CURL IS SLOW! you can also download through dgrive here
# https://drive.google.com/file/d/1HG7YnakUkjaxtNMclbl2t5sJwGLcHYsI/view

fileid="1HG7YnakUkjaxtNMclbl2t5sJwGLcHYsI"
filename="anime.tgz"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}
rm cookie

echo "got here"

# get the faces and smiley faces quickdraw dset
curl "https://storage.cloud.google.com/quickdraw_dataset/full/simplified/smiley%20face.ndjson" > smiley.ndjson
curl "https://storage.cloud.google.com/quickdraw_dataset/full/simplified/face.ndjson" > faces.ndjson

# unpack the anime data
tar zxvf anime.tgz
rm anime.tgz

# use the python script to unpack the ndjson
WORKERS=${1:-4} # default value is 4 workers

mkdir -p sketches
python data/unpack_sketches.py -i smiley.ndjson -o sketches -w $WORKERS
python data/unpack_sketches.py -i faces.ndjson -o sketches -w $WORKERS

