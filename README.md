# pantherapi-pyclient
Example client code for calling [Panther API services](http://panthertest3.med.usc.edu:8083/services/tryItOut.jsp?url=%2Fservices%2Fapi%2Fpanther)

## Installation
```
$ git clone https://github.com/pantherdb/pantherapi-pyclient.git
$ cd pantherapi-pyclient
$ python3 -m venv env
$ . env/bin/activate (bash) or source env/bin/activate.csh (C-shell or tcsh)
$ pip3 install -r requirements.txt
```

## Running
```
$ python3 pthr_go_annots.py --service enrich --params_file params/enrich.json --seq_id_file resources/test_ids.txt
```
- Currently, there are three options for --service.
  - _enrich_ -- This is the statistical overrepresentation test on a list of genes.
  - _geneinfo_ -- This call provides GO and pathway annnotations to the uploaded genes.
  - _ortholog_ -- This call returns the orthologs of the uploaded list. Maximum of 10 genes can be loaded.

- The json file in the params folder can be edited according to uploaded data and the type of call.<br><br>
_enrich.json_  <br>
There are four items to be specified in this file.<br>
"organism": "**9606**",    _--specify an organism with a taxon ID_ <br>
"annotDataSet": "**GO:0008150**", _--specify an annotation data set. See below for the supported data type_ <br>
"enrichmentTestType": "**FISHER**", _--enter either FISHER (for Fisher's Exact test) or BINOMIAL (for binomial distribution test)_ <br>
"correction": "**FDR**" _--specify the multi test correction method (FDR, BONFERRONI, or NONE)_ <br><br>
_geneinfo.json_<br>
The organism taxon ID needs to be specified to match the uploaded data.<br><br>
_ortholog.json_<br>
There are two items to be specified <br>
"organism": "**9606**", _-- specify the organism of the uploaded genes_ <br>
"orthologType": "**LDO**" _-- specify the type of ortholog, e.g., LDO (for least divergent ortholog), or all.__ <br><br>



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
