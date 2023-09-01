export CPOC_LOG_LEVEL=DEBUG
export CPOC_JOBS_PATH="/Users/alvaroperis/Dropbox/cinemawritter/cassette/cassette/jobs"

#cat - | xargs -I {} cassette {}
#cd cassette
#cat - | xargs -I {} python3.9 main.py {}
#./build.sh
python3.9 -m cassette.jobs.job_test.Test.describe()

