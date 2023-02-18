


if [ -d /content ];
then
    TS=`date '+%H:%M:%S' -d "+1 hour"`
    echo "RUN git clone https://github.com/guydegnol/bulkhours.git [$TS]" 
    rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git > /dev/null 2>&1
    if [ "$3" = "econometrics" ]; then
        TS=`date '+%H:%M:%S' -d "+1 hour"`
        echo "RUN pip install yfinance [$TS]"
        pip install yfinance > /dev/null 2>&1
        TS=`date '+%H:%M:%S' -d "+1 hour"`
        echo "RUN pip install geopandas [$TS]"
        pip install geopandas > /dev/null 2>&1
    fi

    BULK_DIR="/content"
else
    TS=`date '+%H:%M:%S' -d "+1 hour"`
    echo "RUN ln bulkhours [$TS]"
    BULK_DIR="/home/guydegnol/projects"
fi


VERSION=`cat "$BULK_DIR/bulkhours/bulkhours/__version__.py" | awk -F  '"' '{print $2}'`
TS=`date '+%H:%M:%S' -d "+1 hour"`
echo "ENV login $1, env $3 [$TS $VERSION]"

JSON_FMT='{"login":"%s","pass_code":"%s","env":"%s"}\n'
printf "$JSON_FMT" "$1" "$2" "$3" > "$BULK_DIR/bulkhours/.safe"
