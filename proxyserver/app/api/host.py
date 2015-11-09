from proxyserver.app.main.models import Host
from proxyserver.app.main.common import *
import logging

logger = logging.getLogger("app.debug")


# @requireLogin


def host_all(request):
    # GET the whole Host List
    if request.method == 'GET':
        data_all = {}
        hosts = Host.objects.all()
        for host in hosts:
            data_per = host.read_as_json()
            # Unique ID per host record
            host_id = host.id
            host_env = host.hostEnv
            if host_env not in data_all:
                data_all[host_env] = {}
            # Append JSON structure per host record to whole result set
            data_all[host_env]["id_"+str(host_id)] = data_per
        return Response.success(data_all, StatusCode.OK)
    # POST new host record
    elif request.method == 'POST':
            p_data = analyse_post_data(request)
            return Host.create_as_json(p_data)
    else:
        return Response.fail(ErrorMessage.method_not_allowed(), StatusCode.METHOD_NOT_ALLOWED)


def host_by_id(request, host_id):
    # get the host data by id
    if request.method == 'GET':
        with get_item_by_id(Host, host_id) as (status, target):
            if status:
                return Response.success(target.read_as_json(), StatusCode.OK)
            else:
                return Response.fail(ErrorMessage.not_found(), StatusCode.NOT_FOUND)
    # update the host data by id
    elif request.method == 'PUT':
        u_data = analyse_post_data(request)
        with get_item_by_id(Host, host_id) as (status, target):
            if status:
                """
                sample output (success):
                    {
                    status: "success"
                    data: {
                    host_id: 9
                    host_account: [0]
                    host_ip: "192.168.1.1"
                    comments: "comment"
                    host_name: "hostname"
                    }-
                    }
                sample output (fail):
                    {
                        status: "fail"
                        error: "duplicated hostname"
                    }
                """
                return target.update_as_json(u_data)
            else:
                """
                sample output (fail):
                    {
                        status: "fail"
                        error: "host not found"
                    }
                """
                return Response.fail(ErrorMessage.not_found(), StatusCode.NOT_FOUND)

    elif request.method == "DELETE":
        with get_item_by_id(Host, host_id) as (status, target):
            if status:
                target.delete()
                # better response needed
                return Response.success(ErrorMessage.deleted(), StatusCode.DELETED)
            else:
                return Response.fail(ErrorMessage.not_found(), StatusCode.NOT_FOUND)
    else:
        return Response.fail(ErrorMessage.method_not_allowed(), StatusCode.METHOD_NOT_ALLOWED)
