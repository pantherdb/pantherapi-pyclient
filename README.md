# pantherapi-pyclient
Example client code for calling [Panther API services](http://panthertest3.med.usc.edu:8083/services/tryItOut.jsp?url=%2Fservices%2Fapi%2Fpanther)

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
$ python3 pthr_go_annots.py --service enrich --params_file params/enrich.json --seq_id_file resources/test_ids.txt
```

## Usage
```
$ python3 pthr_go_annots.py -h
usage: pthr_go_annots.py [-h] [-s SERVICE] [-p PARAMS_FILE] [-f SEQ_ID_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVICE, --service SERVICE
                        Panther API service to call (e.g. 'enrich',
                        'geneinfo', 'ortholog')
  -p PARAMS_FILE, --params_file PARAMS_FILE
                        File path to request parameters JSON file
  -f SEQ_ID_FILE, --seq_id_file SEQ_ID_FILE
                        File path to list of sequence identifiers
```

## Dependencies
```
requests==2.22.0
```
