from datetime import datetime
import mysql.connector


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def get_polypeptides():
    # TODO: move connection to read
    conn = mysql.connector.connect(user='looker', password='mickey',
                                   host='35.232.96.67', database='chado_genes')
    curs = conn.cursor()

    # Query database for all gene products
    query = (
        "SELECT f.uniquename, product.value "  # TODO: add values to this
        "FROM feature f "
        "JOIN cvterm polypeptide ON f.type_id=polypeptide.cvterm_id "
        "JOIN featureprop product USING(feature_id) "
        "JOIN cvterm productprop ON product.type_id=productprop.cvterm_id "
        "WHERE polypeptide.name='polypeptide' AND productprop.name = "
        "'gene_product_name';")
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
POLYPEPTIDES = get_polypeptides()


# Create a handler for our read (GET) polypeptides
def read():
    """
    This function responds to a request for /api/polypeptides
    with the complete lists of people

    :return:        sorted list of polypeptides
    """
    # Create the list of polypeptides from our data
    return [POLYPEPTIDES[key] for key in sorted(POLYPEPTIDES.keys())]
