

if [ -d /content ];
then
    rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git 2> /dev/null
    echo "RUN git clone https://github.com/guydegnol/bulkhours.git USER $1"
    JSON_FMT='{"user":"%s","pass_code":"%s","env":"%s","package_dir":"%s"}\n'
    printf "$JSON_FMT" "$1" "$2" "$3" "/content/bulkhours/" > /content/bulkhours/.safe
else
    echo "RUN use local bulkhours USER $1"
    JSON_FMT='{"user":"%s","pass_code":"%s","env":"%s","package_dir":"%s"}\n'
    printf "$JSON_FMT" "$1" "$2" "$3" "/home/guydegnol/projects/bulkhours/" > /home/guydegnol/projects/bulkhours/.safe
fi


