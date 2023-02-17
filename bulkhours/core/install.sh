

if [ -d /content ];
then
    echo "RUN git clone https://github.com/guydegnol/bulkhours.git"
    rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git &> /dev/null
    if [ "$3" = "econometrics" ]; then
        echo "RUN pip install yfinance"
        pip install yfinance /dev/null 2>&1
    fi

    BULK_DIR="/content"
else
    echo "RUN ln bulkhours"
    BULK_DIR="/home/guydegnol/projects"
fi


VERSION=`cat "bulkhours/bulkhours/__version__.py" | awk -F  '"' '{print $2}'`
echo "ENV BULK Helper cOURSe (version=$VERSION, login=$1 env=$3)"

JSON_FMT='{"login":"%s","pass_code":"%s","env":"%s"}\n'
printf "$JSON_FMT" "$1" "$2" "$3" > "$BULK_DIR/bulkhours/.safe"
