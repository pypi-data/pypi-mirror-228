import json
import os
import requests
import configparser
import subprocess

from cohesity_management_sdk.cohesity_client import CohesityClient

# Fetch the Cluster credentials from config file.
configparser = configparser.ConfigParser()
#configparser.read('/home/naveena.maplelabs/management-sdk-python/samples/project-anfield/config.ini')

def run_cmd(cmd):
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print(proc.communicate())

cluster_ip = input("Enter Cluster IP")
# Delete policies
'''
cohesity_client = CohesityClient(cluster_vip=\
        configparser.get('import_cluster_config', 'cluster_ip'),
                                 username=configparser.get(
                                     'import_cluster_config', 'username'),
                                 password=\
                                 configparser.get('import_cluster_config', 'password'),
                                 domain=configparser.get('import_cluster_config', 'domain'))
'''
cohesity_client = CohesityClient(cluster_ip,"admin","Cohe$1ty")
_input = input("Deleting all resources from %s!!!!!\nAre you sure to proceed, press 'y' to continue " % cluster_ip)
if _input not in ["y", "Y"]:
    exit()
import time
for job in cohesity_client.protection_jobs.get_protection_jobs(is_active=True):
    print(job.name, job.is_active, job.is_paused)
    if job.is_deleted:
        continue
    try:
        print(cohesity_client.protection_jobs.delete_protection_job(id=job.id))
    except Exception as err:
        print(err)
    except Exception as err:
        print(err)
        #time.sleep(10)
        pass


views = cohesity_client.views.get_views().views
v = views if views else []
for view in v:
    try:
        cohesity_client.views.delete_view(name=view.name)
    except Exception as e:
        print(e)
exit()
policies = cohesity_client.protection_policies.get_protection_policies()
policies = [] if not policies else policies
for policy in policies:
    if policy.name in ["Bronze", "Gold", "Silver"]:
        continue
    print(cohesity_client.protection_policies.delete_protection_policy(id=policy.id))

views = cohesity_client.views.get_views().views
v = views if views else []
for view in v:
    try:
        cohesity_client.views.delete_view(name=view.name)
    except Exception as e:
        print(e)

root_nodes = cohesity_client.protection_sources.list_protection_sources_registration_info().root_nodes
root_nodes = [] if not root_nodes else root_nodes
for node in root_nodes:
    if node.root_node.environment in ["kGCP", "kHive", "kHDFS"]:
        pass
        #continue
    try:
        id = node.root_node.id
        cohesity_client.protection_sources.delete_unregister_protection_source(id)
    except Exception as err:
        print(err)



vaults = cohesity_client.vaults.get_vaults(include_marked_for_removal=False)
for vault in vaults:
    try:
        cohesity_client.vaults.delete_vault(vault.id, body=vault)
    except Exception as e:
        print(e)
        continue


remote_clusters = cohesity_client.remote_cluster.get_remote_clusters()
for cluster in remote_clusters:
    print(dir(cluster))
    print(cohesity_client.remote_cluster.delete_remote_cluster(cluster.cluster_id))

