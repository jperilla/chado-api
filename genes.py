from datetime import datetime


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
GENES = {
    "tonB": {
        "name": "tonB",
        "timestamp": get_timestamp()
    },
    "dnaA": {
        "name": "dnaA",
        "timestamp": get_timestamp()
    },
    "grpP": {
        "name": "grpP",
        "timestamp": get_timestamp()
    }
}


# Create a handler for our read (GET) genes
def read():
    """
    This function responds to a request for /api/genes
    with the complete lists of people

    :return:        sorted list of genes
    """
    # Create the list of people from our data
    return [GENES[key] for key in sorted(GENES.keys())]
