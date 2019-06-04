# AutoBook-Olsanka
Books first free slot in badminton on web [http://olsanka.e-rezervace.cz/](http://olsanka.e-rezervace.cz/)
which satisfies the conditions defined in `app/config.py`.

## Usage

1. modify `app/config.py` file 
2. run `docker-compose up` or `python3 main.py` if you already have 
installed dependencies from requirements.txt

## Config
* if the docker-compose is used for run, make sure that you change the environment variables: `OLSANKA_USERNAME` and 
`OLSANKA_PASSWORD` in this file
* environment variables: `OLSANKA_USERNAME` and `OLSANKA_PASSWORD` must be specified in your system otherwise