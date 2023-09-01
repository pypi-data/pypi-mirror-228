import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_morpheus_terraform_inputs(morpheus_custom_options):
    """
    The get_lab_terraform_inputs function takes the provided Morpheus custom options and parses them to determine which template parameters need to be filled in. It then fills in the appropriate values for those parameters and returns a dictionary of all of the template parameters with their corresponding values.
    
    :param morpheus_custom_options: Pass in the custom options that have been provided by the user
    :return: A dictionary of the key value pairs that should be used for the lab
    :doc-author: Trelent
    """
    # Set the class version
    class_version = morpheus_custom_options["class_version"]

    # Validate the class type and import the correct file template for the template parameters to fill in
    if "administration" in morpheus_custom_options["class_name"]:
        logger.info(f'Administration class selected. Importing admin_class_config.json')
        f = pkgutil.get_data(__name__, f"../template_files/{class_version}/admin_class_config.json")
        f = json.loads(f)
    elif "installation" in morpheus_custom_options["class_name"]:
        logger.info(f'Installation class selected. Importing instal_class_config.json')
        f = pkgutil.get_data(__name__, f"../template_files/{class_version}/install_class_config.json")
        f = json.loads(f)
    elif 'automation' in morpheus_custom_options["class_name"]:
        logger.info(f'Automation class selected. Importing automation_class_config.json')
        f = pkgutil.get_data(__name__, f"../template_files/{class_version}/automation_class_config.json")
        f = json.loads(f)
    elif 'troubleshooting' in morpheus_custom_options["class_name"]:
        logger.info(f'Troubleshooting class selected. Importing troubleshooting_class_config.json')
        f = pkgutil.get_data(__name__, f"../template_files/{class_version}/troubleshooting_class_config.json")
        f = json.loads(f)
    terraform_inputs = {}
    # Parse the key value pairs of the provided Morpheus custom options
    for k, v in morpheus_custom_options.items():
        logger.info(f'Checking for a match on the option type: {k}')
        try: 
            if k in f:
                logger.info(f'Found {k}, updating with a value of {v}')
                update = {k: v}
                terraform_inputs.update(update)
            else:
                logger.info(f'{k} not found in the template. Skipping it.')
        except Exception as e:
            logger.error(f'Something went wrong {e}')
    for k, v in f.items():
        try:
            if v :
                logger.info(f'Item {k} with a value of {v} discovered. Adding it to the payload.')
                update = {k: v}
                terraform_inputs.update(update)
            else:
                logger.info(f'{k} does not have a default value in the template. Skipping it')
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
    return(terraform_inputs)

def _get_instance_ids_from_names(url,headers,names:list):
    """
    The _get_instance_ids_from_names function accepts a list of names and returns a list of instance IDs.
    It does this by making an API call to the AS API for each name in the provided list, and then returning
    the ID from that response.
    
    :param url: Specify the url of the instance
    :param headers: Pass the api key to the _get_instance_ids_from_names function
    :param names:list: Pass a list of names to the _get_instance_ids_from_names function
    :return: A list of instance ids based on a list of names
    :doc-author: Trelent
    """
    session = FuturesSession()
    endpoint = "/api/instances"
    ids = []
    futures=[session.get(f'{url}{endpoint}?name={n}',headers=headers,verify=False) for n in names]
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            i = resp.json()["instances"][0]
            ids.append(i["id"])
    return(ids)

