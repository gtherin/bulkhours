

if [ -d /content ];
then
    echo "RUN git clone https://github.com/guydegnol/bulkhours.git"
    rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git 2> /dev/null
    if [ "$3" = "econometrics" ]; then
        echo "RUN pip install yfinance"
        pip install yfinance 2> /dev/null
    fi

    BULK_DIR="/content"
else
    echo "RUN ln bulkhours"
    BULK_DIR="/home/guydegnol/projects"
fi


cat "$BULK_DIR/bulkhours/bulkhours/__version__.py"
VERSION="None"
echo "ENV BULK Helper cOURSe (version=$VERSION, login=$1 env=$3)")

JSON_FMT='{"login":"%s","pass_code":"%s","env":"%s"}\n'
printf "$JSON_FMT" "$1" "$2" "$3" > "$BULK_DIR/bulkhours/.safe"

