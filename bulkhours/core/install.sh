

if [ -d /content ];
then
    rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git 2> /dev/null
    echo "RUN git clone https://github.com/guydegnol/bulkhours.git"
    JSON_FMT='{"pass_code":"%s","package_dir":"%s"}\n'
    printf "$JSON_FMT" "$1" "/content/bulkhours/" > /content/bulkhours/.safe
else
    JSON_FMT='{"pass_code":"%s","package_dir":"%s"}\n'
    printf "$JSON_FMT" "$1" "/home/guydegnol/projects/bulkhours/" > /home/guydegnol/projects/bulkhours/.safe
fi


