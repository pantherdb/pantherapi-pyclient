import argparse
import requests
from urllib.parse import quote
from xml.etree import ElementTree

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--seq_id_file', help="File path to list of sequence identifiers")


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
        base_url = "http://panthertest3.med.usc.edu:8083/services/oai/pantherdb/enrich/overrep?"
        Request.__init__(self, base_url, EnrichResponse)


class EnrichResponse(Response):
    def print_results(self):
        results = self.response['results']['result']
        print(len(results), "terms in reference list")  # Our result count

        display_headers = ["GO Term", "Expected", "Fold enrichment", "raw P value", "FDR", "Term label"]
        print("\t".join(display_headers))

        results.sort(key=lambda x: x['fold_enrichment'], reverse=True)  # Sort in same order as pantherdb.org
        for r in results:
            fold_enrichment = r['fold_enrichment']
            if fold_enrichment > 0:
                # Print result line
                print("\t".join([
                    r['term'].get("id"),
                    str(r['expected']),  # Convert float to string for printing
                    str(fold_enrichment),
                    str(r['pValue']),
                    str(r['fdr']),
                    r['term']["label"]
                    ])
                )


class GeneInfoRequest(Request):
    def __init__(self):
        base_url = "http://panthertest3.med.usc.edu:8083/services/oai/pantherdb/geneinfo?"
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

        display_headers = ["PTHR longID", "Annotation Dataset", "GO Terms"]
        print("\t".join(display_headers))

        results = self.response['search']['mapped_genes']['gene']
        for r in results:
            pthr_long_id = r['accession']
            for dt in self.handle_annotation_data_type(r['annotation_type_list']['annotation_data_type']):
                annotations = dt['annotation_list']['annotation']
                # Print result line
                go_terms = ",".join([a['id'] for a in self.handle_annotation(annotations)])
                print("\t".join([pthr_long_id, dt['content'], go_terms]))


# Script entry point
if __name__ == "__main__":
    args = parser.parse_args()

    # Hard-coded request parameters - MUST CHANGE FOR DIFFERENT SERVICES
    request_parameters = {
        "organism": "9606",
        "annotDataSet": "GO:0008150",
        "enrichmentTestType": "FISHER",
        "correction": "FDR"
    }

    # Parse sequence ID file (from -f argument) and format list to comma-delimited string
    if args.seq_id_file:
        seq_ids = []
        with open(args.seq_id_file) as seq_f:
            for l in seq_f.readlines():
                seq_ids.append(l.rstrip())
        gene_list = ",".join(seq_ids)
        request_parameters["geneInputList"] = gene_list  # Add these IDs to parameters

    # Create request object - TOGGLE COMMENTING OF Request() OBJECTS TO CONTROL WHICH SERVICE IS CALLED
    request = EnrichRequest()
    # request = GeneInfoRequest()
    # Set parameters
    request.parameters = request_parameters
    # Make the call
    response = request.call_service()
    # Display formatted results
    response.print_results()
