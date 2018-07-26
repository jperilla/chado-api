from datetime import datetime


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def get_genes():
    # TODO: move connection to it's own file
    conn = mysql.connector.connect(user='looker', password='mickey',
                                   host='35.232.96.67', database='chado_genes')
    curs = conn.cursor()

    # Query database for all gene products
    query = (
        "SELECT f.uniquename, gene.value "  # TODO: add values to this
        "FROM feature f "
        "JOIN cvterm type ON f.type_id=type.cvterm_id "
        "JOIN featureprop gene USING(feature_id) "
        "JOIN cvterm geneprop ON gene.type_id=geneprop.cvterm_id "
        "WHERE type.name='gene' AND geneprop.name = 'gene_symbol';")
    curs.execute(query)

    # Create products by iterating through query result - replace this with ORM
    polypeptides = dict()
    for (uniquename, value) in curs:
        polypeptides[value.decode('utf-8')] = {"uniquename":
                                               uniquename.decode('utf-8'),
                                               "product":
                                               value.decode('utf-8'),
                                               "timestamp": get_timestamp()}

    conn.close()

    return polypeptides


# Data to serve with our API
GENES = get_genes()

# Create a handler for our read (GET) genes
def read():
    """
    This function responds to a request for /api/genes
    with the complete lists of people

    :return:        sorted list of genes
    """
    # Create the list of people from our data
    return [GENES[key] for key in sorted(GENES.keys())]
