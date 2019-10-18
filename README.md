# pantherapi-pyclient
Example code for calling Panther API services

## Installation
```
$ git clone https://github.com/pantherdb/pantherapi-pyclient.git
$ cd pantherapi-pyclient
$ python3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
```

## Running
```
$ python3 pthr_go_annots.py --service enrich --params_file enrich_params.json --seq_id_file test_ids.txt
```

## Dependencies
```
requests==2.22.0
```
