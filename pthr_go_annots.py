import argparse
import requests
import json
from urllib.parse import quote

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--service', help="Panther API service to call (e.g. 'enrich', 'geneinfo', 'ortholog')")
parser.add_argument('-p', '--params_file', help="File path to request parameters JSON file")
parser.add_argument('-f', '--seq_id_file', help="File path to list of sequence identifiers")
parser.add_argument('-r', '--ref_seq_id_file', help="File path to list of sequence identifiers for reference list")


class Request:
    def __init__(self, base_url, response_class):
        self.base_url = base_url
        self.parameters = None
        self.response_class = response_class  # Link Response class to Request class

    def call_service(self):
        url = self.base_url

        # Format and append request parameters to API URL
        parameter_strings = []
        for key, value in self.parameters.items():
            if key == "annotDataSet":
                value = quote(value)  # Format special characters for URL. Ex: "GO:0008150" -> "GO%3A0008150"
            parameter_string = "{parameter}={query}".format(parameter=key, query=value)
            parameter_strings.append(parameter_string)
        url += "&".join(parameter_strings)

        print("Request URL -", url)
        response = requests.get(url)
        return self.response_class(response.json())


class Response:
    def __init__(self, response_json):
        self.response = response_json


class EnrichRequest(Request):
    def __init__(self):
        base_url = "https://pantherdb.org/services/oai/pantherdb/enrich/overrep?"
        Request.__init__(self, base_url, EnrichResponse)


class EnrichResponse(Response):
    def print_results(self):
        try:
            results = self.response['results']['result']
        except:
            print("ERROR: Parsing response failed. Full response:\n{}".format(self.response))
            exit()
        print(len(results), "terms in reference list")  # Our result count

        display_headers = ["GO Term", "Expected", "Fold enrichment", "raw P value", "FDR", "Term label"]
        print("\t".join(display_headers))

        results.sort(key=lambda x: x['fold_enrichment'], reverse=True)  # Sort in same order as pantherdb.org
        for r in results:
            fold_enrichment = r['fold_enrichment']
            if fold_enrichment > 0:
                # Print result line
                term_id = r['term'].get("id")
                if term_id is None:  # Handling REACTOME "UNCLASSIFIED"
                    term_id = ""
                print("\t".join([
                    term_id,
                    str(r['expected']),  # Convert float to string for printing
                    str(fold_enrichment),
                    str(r['pValue']),
                    str(r['fdr']),
                    r['term']["label"]
                    ])
                )


class GeneInfoRequest(Request):
    def __init__(self):
        base_url = "https://pantherdb.org/services/oai/pantherdb/geneinfo?"
        Request.__init__(self, base_url, GeneInfoResponse)


class GeneInfoResponse(Response):
    @staticmethod
    def handle_annotation_data_type(annotation_data_type):
        # Handle single annotation data type results that are occasionally not in list structures
        if isinstance(annotation_data_type, list):
            return annotation_data_type
        else:
            return [annotation_data_type]

    @staticmethod
    def handle_annotation(annotation):
        # Handle single annotation results that are occasionally not in list structures
        if isinstance(annotation, list):
            return annotation
        else:
            return [annotation]

    def print_results(self):
        print(len(self.response['search']['mapped_genes']['gene']), "mapped genes")

        display_headers = ["PANTHER gene ID", "AnnotationDataset", "Annotation Terms"]
        print("\t".join(display_headers))

        dataset_title_mapping = {
            "GO:0008150": "GO biological process complete",
            "GO:0005575": "GO cellular component complete",
            "GO:0003674": "GO molecular function complete",
            "ANNOT_TYPE_ID_PANTHER_GO_SLIM_BP": "PANTHER GO-Slim Biological Process",
            "ANNOT_TYPE_ID_PANTHER_GO_SLIM_CC": "PANTHER GO-Slim Cellular Component",
            "ANNOT_TYPE_ID_PANTHER_GO_SLIM_MF": "PANTHER GO-Slim Molecular Function",
            "ANNOT_TYPE_ID_PANTHER_PATHWAY": "PANTHER Pathways",
            "ANNOT_TYPE_ID_REACTOME_PATHWAY": "Reactome pathways",
            "ANNOT_TYPE_ID_PANTHER_PC": "PANTHER Protein Class",
        }

        try:
            results = self.response['search']['mapped_genes']['gene']
        except:
            print("ERROR: Parsing response failed. Full response:\n{}".format(self.response))
            exit()
        if isinstance(results, dict):
            results = [results]
        for r in results:
            pthr_long_id = r['accession']
            if 'annotation_type_list' in r:
                for dt in self.handle_annotation_data_type(r['annotation_type_list']['annotation_data_type']):
                    annotations = dt['annotation_list']['annotation']
                    # Print result line
                    go_terms = ",".join([a['id'] for a in self.handle_annotation(annotations)])
                    if dt['content'] in dataset_title_mapping:
                        dataset_title = dataset_title_mapping[dt['content']]
                    else:
                        dataset_title = dt['content']
                    print("\t".join([pthr_long_id, dataset_title, go_terms]))
            else:
                print("\t".join([pthr_long_id, "", ""]))


class OrthologRequest(Request):
    def __init__(self):
        base_url = "https://pantherdb.org/services/oai/pantherdb/ortholog/matchortho?"
        Request.__init__(self, base_url, OrthologResponse)


class OrthologResponse(Response):
    def print_results(self):
        display_headers = ["InputGeneID", "MappedID", "OrthologID", "OrthologSymbol", "OrthologType"]
        print("\t".join(display_headers))

        try:
            ortholog_matches = self.response['search']['mapping']['mapped']
        except:
            print("ERROR: Parsing response failed. Full response:\n{}".format(self.response))
            exit()
        unique_matches = []
        for m in ortholog_matches:
            if m not in unique_matches:
                unique_matches.append(m)
        for m in unique_matches:
            target_gene_symbol = str(m.get('target_gene_symbol')) if 'target_gene_symbol' in m else ""
            print("\t".join([
                m['id'],
                m['gene'],
                m['target_gene'],
                target_gene_symbol,
                m['ortholog']
                ])
            )


# Handy argument-to-object mapping
SERVICE_OBJ_LOOKUP = {
    "enrich": EnrichRequest,
    "geneinfo": GeneInfoRequest,
    "ortholog": OrthologRequest,
}


def get_request_obj(service):
    return SERVICE_OBJ_LOOKUP[service]()


def check_args(args):
    if args.service is None:
        print("ERROR: Please specify a service to call with --service")
        exit()
    elif args.service not in SERVICE_OBJ_LOOKUP:
        print("ERROR: --service '{}' is not a supported service".format(args.service))
        exit()
    if args.params_file is None:
        print("ERROR: Please specify a parameters file with --params_file")
        exit()
    # TODO: Check if args.seq_id_file is req'd for certain services


# Script entry point
if __name__ == "__main__":
    args = parser.parse_args()

    check_args(args)  # Any missing arguments should stop script here

    with open(args.params_file) as pf:
        request_parameters = json.loads(pf.read())

    # Parse sequence ID file (from -f argument) and format list to comma-delimited string
    if args.seq_id_file:
        seq_ids = []
        with open(args.seq_id_file) as seq_f:
            for l in seq_f.readlines():
                seq_ids.append(l.rstrip())
        gene_list = ",".join(seq_ids)
        request_parameters["geneInputList"] = gene_list  # Add these IDs to parameters

    # Parse sequence ID file (from -f argument) and format list to comma-delimited string
    if args.ref_seq_id_file:
        ref_seq_ids = []
        with open(args.ref_seq_id_file) as ref_seq_f:
            for l in ref_seq_f.readlines():
                ref_seq_ids.append(l.rstrip())
        ref_gene_list = ",".join(ref_seq_ids)
        request_parameters["refInputList"] = ref_gene_list  # Add these IDs to parameters

    request = get_request_obj(args.service)
    # Set parameters
    request.parameters = request_parameters
    # Make the call
    response = request.call_service()
    # Display formatted results
    response.print_results()
