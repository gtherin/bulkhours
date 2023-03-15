import argparse
import sys


def get_arg_parser(argv):
    parser = argparse.ArgumentParser(
        description="Installation script evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-e", "--evaluation-id", help=f"Select which correction to apply")
    parser.add_argument("-s", "--show-solution", help="Show the solution", action="store_true")
    parser.add_argument("-d", "--delete-solution", help="Delete the solution", action="store_true")
    parser.add_argument("-c", "--pass-code", help="Pass code")
    # parser.add_argument("-p", "--promo", help="Promo", default=promotion.current_promo)

    parser = argparse.ArgumentParser(description="Evaluation params")
    parser.add_argument("-i", "--id", default=None)
    parser.add_argument("-u", "--user", default=os.environ["STUDENT"])
    parser.add_argument("-o", "--options", default=None)

    return parser.parse_args(argv)


def main(argv=sys.argv[1:]):
    print("FFFFFFFFFFFFFFFF")


if __name__ == "__main__":
    main()


"""
login="$1"
passwd="$2"
envi="$3"
passse="$4"
notebook="$5"
packages="$6"

# Check the install procedure
if [ "$passse" != "ARANCINI" ]; then
    echo "Library bulkhours is no more available.";
    exit 0;
fi

# Set up the package directory
if [ -d /content ];
then
    BULK_DIR="/content"
else
    BULK_DIR="/home/guydegnol/projects"
fi


if [ -d /content ];
then
    TS=`date '+%H:%M:%S' -d "+1 hour"`
    echo "RUN git clone https://github.com/guydegnol/bulkhours.git [$TS]" 
    rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git --depth 1 > /dev/null 2>&1
    echo "RUN pip install --upgrade pip [$TS]"
    pip install --upgrade pip > /dev/null 2>&1
    if [ "$3" = "econometrics" ]; then
        export IFS=","
        #packages="yfinance,geopandas,descartes"
        for package in $packages; do
            TS=`date '+%H:%M:%S' -d "+1 hour"`
            echo "RUN pip install $package [$TS]"
            pip install $package > /dev/null 2>&1
        done
    fi

else
    TS=`date '+%H:%M:%S' -d "+1 hour"`
    echo "RUN ln bulkhours [$TS]"
    export IFS=","
    for package in $packages; do
        TS=`date '+%H:%M:%S' -d "+1 hour"`
        echo "RUN pip install $package [$TS]"
    done

fi


VERSION=`cat "$BULK_DIR/bulkhours/bulkhours/__version__.py" | awk -F  '"' '{print $2}'`
TS=`date '+%H:%M:%S' -d "+1 hour"`
echo "ENV login $login, env $envi [$TS $VERSION]"

JSON_FMT='{"login":"%s","pass_code":"%s","env":"%s","course_version":"%s"}\n'
printf "$JSON_FMT" "$login" "$passwd" "$envi" "$passse" > "$BULK_DIR/bulkhours/.safe"
"""
