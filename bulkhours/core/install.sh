

if [ -d /content ];
then
    rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git 2> /dev/null
    echo "RUN git clone https://github.com/guydegnol/bulkhours.git USER $1"
    JSON_FMT='{"login":"%s","pass_code":"%s","env":"%s"}\n'
    BULK_DIR="/content"
    printf "$JSON_FMT" "$1" "$2" "$3" > "$BULK_DIR/bulkhours/.safe"
else
    echo "RUN use local bulkhours USER $1"
    BULK_DIR="/home/guydegnol/projects"
    JSON_FMT='{"login":"%s","pass_code":"%s","env":"%s"}\n'
    printf "$JSON_FMT" "$1" "$2" "$3" > "$BULK_DIR/bulkhours/.safe"
fi


