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
  - _ortholog_ -- This call returns the orthologs of the uploaded list. Maximum of 10 genes can be loaded. The orthologs can be from a specified genome, or from all genomes in the PANTHER database (132 total).<br><br>


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
"orthologType": "**LDO**" _-- specify the type of ortholog, e.g., LDO (for least divergent ortholog), or all._ <br>
"targetOrganism": “**10090**,**7227**” _-- specifiy the taxon ids for the target organisms, separated by a comma._<br><br>

**How to find a Taxon ID?**

There are three ways to find the exact taxon IDs for genomes supported by PANTHER. 

1. Go to the PANTHER Open API site (http://panthertest3.med.usc.edu:8083/services/tryItOut.jsp?url=%2Fservices%2Fapi%2Fpanther), and use the /supportedgenomes service.
2. Go directly to the API link page (http://panthertest3.med.usc.edu:8083/services/oai/pantherdb/supportedgenomes). 
3. Run the following command: curl -X POST "http://panthertest3.med.usc.edu:8083/services/oai/pantherdb/supportedgenomes" -H  "accept: application/json"

Use the taxon ID that corresponds to the genomes in the ‘name’ field.

**How to find the ID for supported annotation dataset?**

There are three similar ways to find the IDs or text needed for the supported annotation dataset.
1. Go to the PANTHER Open API site (http://panthertest3.med.usc.edu:8083/services/tryItOut.jsp?url=%2Fservices%2Fapi%2Fpanther), and use the /supportedannotdatasets service.
2. Go directly to the API link page (http://panthertest3.med.usc.edu:8083/services/oai/pantherdb/supportedannotdatasets). 
3. Run the following command: curl -X POST "http://panthertest3.med.usc.edu:8083/services/oai/pantherdb/supportedannotdatasets" -H  "accept: application/json"


Use the text in the ‘id’ field for the parameter files.


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
