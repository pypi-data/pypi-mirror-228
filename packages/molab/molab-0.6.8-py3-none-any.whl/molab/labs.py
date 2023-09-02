import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time
from .tools import get_class_lab_instance_type, get_class_layout_id, get_morpheus_terraform_plan_id, get_instance_provisioning_payload, get_instance, get_morpheus_terraform_inputs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class newClass():
    def __init__(self,url,headers,instance_map,instance_name):
        self.url = url
        self.headers = headers
        self.instance_map = instance_map
        self.instanceName = instance_name
        self.custom_options = self.instance_map["customOptions"]
        self.templateParameters = get_morpheus_terraform_inputs(self.custom_options)
        self.templateParameters["lab_name"] = self.instanceName.split("-")[-1]
        self.templateParameters["master_region"] = self.instance_map["customOptions"]["trainingZone"].split(",")[0]
        self.templateParameters["labs_region"] = self.instance_map["customOptions"]["trainingZone"].split(",")[1]
        self.instance_type = get_class_lab_instance_type(self.url,self.headers,f'ilt{self.instance_map["customOptions"]["class_name"][0:3]}')
        self.instance_layout_id = get_class_layout_id(self.url,self.headers,self.custom_options,self.instance_type)
        self.terraform_plan_id = get_morpheus_terraform_plan_id(self.url,self.headers)
        self.deploy_payload = get_instance_provisioning_payload(
            class_version=self.custom_options["class_version"],
            zone_id=self.instance_map["input"]["zoneId"],
            instance_name=self.instanceName,
            site_id=self.instance_map["input"]["site"]["id"],
            instance_type=self.instance_type["code"],
            instance_type_code=self.instance_type["code"],
            layout_id=self.instance_layout_id,
            plan_id=self.terraform_plan_id,
            template_parameters=self.templateParameters,
            )
        
    def deploy(self):
        try:
            logger.info(f'Attempting to deploy the instance: {self.instanceName}')
            resp = requests.post(f'{self.url}/api/instances',headers=self.headers,json=self.deploy_payload,verify=False)
        except Exception as e:
            logger.error(e)
        if "200" in str(resp):
            logger.info(f'Instance {self.instanceName} deployment successfully triggered...')
            self.instance_id = resp.json()["instance"]["id"]
            return
        elif "504" in str(resp):
            logger.info(f'Received a gateway timeout.')
            logger.info(f'Instance {self.instanceName} deployment possibly triggered...')
            self.instance_id = "null"
            return
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp)

    def status(self):
        counter = 0
        max_counter = 20
        logger.info(f'Checking the deployment status of the instance: {self.instanceName}')
        while counter < max_counter:
            try:
                resp = requests.get(f'{self.url}/api/instances/{self.instance_id}',headers=self.headers,verify=False)
                counter += 1
            except Exception as e:
                logger.error(f'Something went wrong: {e}')
            if "200" in str(resp):
                logger.info(f'Instance {self.instanceName} instance found. Checking status...')
                logger.info(f'Status: {resp.json()["instance"]["status"]}')
                if resp.json()["instance"]["status"] == "provisioning":
                    logger.info(f'Instance {self.instanceName} is still provisioning. Waiting 60 seconds and checking again...')
                    self.status = resp.json()["instance"]["status"]
                    time.sleep(60)
                elif resp.json()["instance"]["status"] == "running":
                    logger.info(f'Instance {self.instanceName} is running. Continuing...')
                    self.status = resp.json()["instance"]["status"]
                    return
                else:
                    logger.error(f'Unexpected status: {resp.json()["instance"]["status"]}')
                    self.status = resp.json()["instance"]["status"]
                    return
            else:
                logger.error(f'Something went wrong: {resp.json()}')
                return(resp.json())

    def lock(self):
        try:
            logger.info(f'Attempting to lock the instance: {self.instanceName}')
            resp = requests.put(f'{self.url}/api/instances/{self.instance_id}/lock',headers=self.headers,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        if "200" in str(resp):
            logger.info(f'Instance {self.instanceName} locked successfully.')
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.json())
        
    def get_lab_data(self):
        self.lab_data = {}
        try:
            logger.info(f'Attempting to get the lab info for the instance: {self.instanceName}')
            resp = requests.get(f'{self.url}/api/instances/{self.instance_id}/state',headers=self.headers,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        if "200" in str(resp):
            logger.info(f'Lab info for instance {self.instanceName} found.')
            self.lab_data["lab_name"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "lab_name"][0]
            self.lab_data["region"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "labs_region"][0]
            self.lab_data["morpheus_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_external_ip"][0]
            self.lab_data["morpheus_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_internal_ip"][0]
            self.lab_data["morpheus_url"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_url"][0]
            self.lab_data["rocky_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "rocky_ami"][0]
            self.lab_data["ubuntu_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "ubuntu_ami"][0]
            self.lab_data["iam_key"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_key"][0]
            self.lab_data["iam_secret"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_secret"][0]
            return
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.json())

class existingClass():
    def __init__(self,url,headers,instance_map) :
        self.url = url
        self.headers = headers
        self.instance_id = instance_map["id"]
        self.instance_name = instance_map["name"]

    def unlock(self):
        for lab in self.instance_map["config"]["attributes"]["labs"]:
            try:
                logger.info(f'Attempting to unlock the instance: {lab["lab_name"]}')
                resp = requests.put(f'{self.url}/api/instances/{lab["instance_id"]}/unlock',headers=self.headers,verify=False)
            except Exception as e:
                logger.error(f'Something went wrong: {e}')
            if "200" in str(resp):
                logger.info(f'Instance {lab["lab_name"]} unlocked successfully.')
            else:
                logger.error(f'Something went wrong: {resp.json()}')
                return(resp.json())
            
    def delete(self):
        for lab in self.instance_map["config"]["attributes"]["labs"]:
            try:
                logger.info(f'Attempting to delete the instance: {lab["lab_name"]}')
                resp = requests.delete(f'{self.url}/api/instances/{lab["instance_id"]}',headers=self.headers,verify=False)
            except Exception as e:
                logger.error(f'Something went wrong: {e}')
            if "200" in str(resp):
                logger.info(f'Instance {lab["lab_name"]} deleted successfully.')
            else:
                logger.error(f'Something went wrong: {resp.json()}')
                return(resp.json())

class existingLab():
    def __init__(self,url,headers,instance_id) -> None:
        self.instance_map = get_instance(url,headers,instance_id)
        self.instance_name = self.instance_map["name"]
        self.instance_id = instance_id
        self.status = self.instance_map["status"]
        
    def get_lab_data(self):
        self.lab_data = {}
        try:
            logger.info(f'Attempting to get the lab info for the instance: {self.instance_name}')
            resp = requests.get(f'{self.url}/api/instances/{self.instance_id}/state',headers=self.headers,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        if "200" in str(resp):
            logger.info(f'Lab info for instance {self.instance_name} found.')
            self.lab_data["lab_name"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "lab_name"][0]
            self.lab_data["region"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "labs_region"][0]
            self.lab_data["morpheus_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_external_ip"][0]
            self.lab_data["morpheus_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_internal_ip"][0]
            self.lab_data["morpheus_url"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_url"][0]
            self.lab_data["rocky_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "rocky_ami"][0]
            self.lab_data["ubuntu_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "ubuntu_ami"][0]
            self.lab_data["iam_key"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_key"][0]
            self.lab_data["iam_secret"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_secret"][0]
            return
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.json())
        
    def unlock(self):
        try:
            logger.info(f'Attempting to unlock the instance: {self.instance_name}')
            resp = requests.put(f'{self.url}/api/instances/{self.instance_id}/unlock',headers=self.headers,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        if "200" in str(resp):
            logger.info(f'Instance {self.instance_name} unlocked successfully.')
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.json())
        
    def delete(self):
        try:
            logger.info(f'Attempting to delete the instance: {self.instance_name}')
            resp = requests.delete(f'{self.url}/api/instances/{self.instance_id}',headers=self.headers,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        if "200" in str(resp):
            logger.info(f'Instance {self.instance_name} deleted successfully.')
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.json())
        
class newLab():
    def __init__():
        pass