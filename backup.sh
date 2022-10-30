#!/bin/bash
# d - specify detination path -> (required)
# c - specify container id -> (optional)
# t - specify cron schedule in quotes -> (optional)
# ./backup.sh -d <detination_path> -c <container_id> -t <cron schedule [minute hour day_of_month month day_of_week]>

date=$(date '+%d-%m-%Y')

while getopts ":d:c:t:" opt; do
    case $opt in
        d) path="$OPTARG";;
        c) container_id="$OPTARG";;
        t) crontab="$OPTARG";;
    esac
done

if [ -z "$path" ]
then
    echo 'specifying storage path with -d is required'
else
    [ ! -d "$path" ] && echo "Directory $path DOES NOT exists." && exit 1
    full_path="${path:+$path/}$date"

    [ -z "$crontab" ] && \
    (
        [ -d $full_path ] || mkdir $full_path && \ 
        [ ! -z "$container_id" ] && docker exec -it $container_id python3 manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > $full_path/dump.json || \
        python3 manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > $full_path/dump.json && \
        [ ! -z "$container_id" ] && docker cp $container_id:/home/app/media  $full_path || cp -R ./media  $full_path
    ) || (
        crontab -l > tmp
        grep -v "$(pwd)/backup.sh" tmp > tmpfile && mv tmpfile tmp
        echo "$crontab $(pwd)/backup.sh -d $path -c $container_id" >> tmp
        crontab tmp && rm tmp
    )

fi && exit 1