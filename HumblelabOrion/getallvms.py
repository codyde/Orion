import atexit
import ssl
from pyVim import connect
from pyVmomi import vim
import json
import collections


def vconnect():
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE  # disable our certificate checking for lab
    vms = []  # create our future array
    service_instance = connect.SmartConnect(host="hlcoremgt01.humblelab.com",  # build python connection to vSphere
                                            user="administrator@vsphere.local",
                                            pwd="holypantsandshirts!",
                                            sslContext=s)

    atexit.register(connect.Disconnect, service_instance)  # build disconnect logic

    content = service_instance.RetrieveContent()

    container = content.rootFolder  # starting point to look into
    viewtype = [vim.VirtualMachine]  # object types to look for
    recursive = True  # whether we should look into it recursively
    containerview = content.viewManager.CreateContainerView(container, viewtype, recursive)  # create container view
    children = containerview.view

    objects_list = []
    for child in children:
        summary = child.summary
        d = collections.OrderedDict()
        d['name'] = summary.config.name
        d['powerStatus'] = summary.runtime.powerState
        objects_list.append(d)
    j = json.dumps(objects_list)
    return j
