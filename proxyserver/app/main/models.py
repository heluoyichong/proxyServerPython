from django.db import models
from django.db import IntegrityError
from proxyserver.app.main.common import *


class Admin(models.Model):
    firstName = models.CharField(max_length=80)
    lastName = models.CharField(max_length=80)
    emailAddr = models.EmailField(max_length=254, null=True)
    loginName = models.CharField(max_length=80, unique=True)
    loginPass = models.CharField(max_length=32)

    def __unicode__(self):
        return self.firstName + ' ' + self.lastName

    class Meta:
        db_table = "tblAdmin"


class Account(models.Model):
    firstName = models.CharField(max_length=80)
    lastName = models.CharField(max_length=80)
    emailAddr = models.EmailField(max_length=254, null=True)
    loginName = models.CharField(max_length=80, unique=True)
    loginPass = models.CharField(max_length=32)

    def __unicode__(self):
        return self.firstName + ' ' + self.lastName

    class Meta:
        db_table = "tblAccount"

    def read_as_json(self):
        return dict(
            account_id=self.id,
            account_fname=self.firstName,
            account_lname=self.lastName,
            account_email=self.emailAddr,
            account_login_name=self.lastName
        )

    def update_as_json(self, json_data):
        try:
            if 'account_fname' in json_data:
                self.firstName = json_data['account_fname']
            if 'account_lname' in json_data:
                self.lastName = json_data['account_lname']
            if 'account_email' in json_data:
                self.emailAddr = json_data['account_email']
            if 'account_login_name' in json_data:
                self.loginName = json_data['account_login_name']

            if 'hosts' in json_data:
                existing_hosts = [host.id for host in self.host_set.all()]
                updated_hosts = json_data['hosts']
                added_hosts = [_id for _id in updated_hosts if _id not in existing_hosts]
                deleted_hosts = [_id for _id in existing_hosts if _id not in updated_hosts]
                if added_hosts:
                    for host_id in added_hosts:
                        self.accounts.add(Host.objects.get(id=host_id))
                elif deleted_hosts:
                    for host_id in deleted_hosts:
                        self.accounts.remove(Host.objects.get(id=host_id))
            self.save()
        except IntegrityError:
            return Response.fail(ErrorMessage.duplicated(), StatusCode.DUPLICATED)
        else:
            return Response.success(self.read_as_json(), StatusCode.OK)

    @classmethod
    def create_as_json(cls, json_data):
        try:
            cls.objects.get(loginName=json_data['account_login_name'])
        except cls.DoesNotExist:
            cls.objects.create(
                loginName=json_data['account_login_name'],
                loginPass=json_data['account_login_pass'],
                firstName=json_data['account_fname'],
                lastName=json_data['account_lname'],
                emailAddr=json_data['account_email'])
            new_account = cls.objects.get(loginName=json_data['account_login_name'])
            return Response.success(new_account.read_as_json(), StatusCode.OK)
        else:
            return Response.fail(ErrorMessage.duplicated(), StatusCode.DUPLICATED)


class Service(models.Model):
    serviceName = models.CharField(max_length=80, unique=True)
    portNumber = models.IntegerField(unique=True)
    comments = models.CharField(max_length=512)

    def __unicode__(self):
        return self.serviceName

    class Meta:
        db_table = "tblService"

    # def read_as_json(self):
    #     return dict(
    #         service_id=self.id,
    #         service_name=self.serviceName,
    #         service_port=self.portNumber,
    #         comments=self.comments
    #     )
    #
    # def update_as_json(self, json_data):
    #     try:
    #         if 'service_name' in json_data:
    #             self.serviceName = json_data['service_name']
    #         if 'service_port' in json_data:
    #             self.portNumber = json_data['service_ip']
    #         if 'comments' in json_data:
    #             self.comments = json_data['comments']
    #
    #         if 'hosts' in json_data:
    #             existing_hosts = [host.id for host in self.host_set.all()]
    #             updated_hosts = json_data['hosts']
    #             added_hosts = [_id for _id in updated_hosts if _id not in existing_hosts]
    #             deleted_hosts = [_id for _id in existing_hosts if _id not in updated_hosts]
    #             if added_hosts:
    #                 for host_id in added_hosts:
    #                     self.accounts.add(Host.objects.get(id=host_id))
    #             elif deleted_hosts:
    #                 for host_id in deleted_hosts:
    #                     self.accounts.remove(Host.objects.get(id=host_id))
    #         self.save()
    #     except IntegrityError:
    #         return Response.fail(ErrorMessage.duplicated(), StatusCode.DUPLICATED)
    #     else:
    #         return Response.success(self.read_as_json(), StatusCode.OK)


class Host(models.Model):
    # ORM attributes
    hostName = models.CharField(max_length=80, unique=True)
    hostIp = models.GenericIPAddressField(protocol='IPv4')
    # hostEnvs => ('DEV','UAT','PRD','Others')
    hostEnv = models.CharField(max_length=10)
    comments = models.CharField(max_length=512, null=True)
    accounts = models.ManyToManyField(Account)
    services = models.ManyToManyField(Service)

    class Meta:
        db_table = "tblHost"

    def __unicode__(self):
        return self.hostName

    def read_as_json(self):
        return dict(
            host_id=self.id,
            host_name=self.hostName,
            host_ip=self.hostIp,
            comments=self.comments,
            accounts=[(account.id, account.loginName) for account in self.accounts.all()]
        )

    def update_as_json(self, json_data):
        try:
            if 'host_name' in json_data:
                self.hostName = json_data['host_name']
            if 'host_ip' in json_data:
                self.hostIp = json_data['host_ip']
            if 'host_env' in json_data:
                self.hostEnv = json_data['host_env']

            if 'accounts' in json_data:
                existing_accounts = [account.id for account in self.accounts.all()]
                updated_accounts = json_data['accounts']
                added_accounts = [_id for _id in updated_accounts if _id not in existing_accounts]
                deleted_accounts = [_id for _id in existing_accounts if _id not in updated_accounts]
                if added_accounts:
                    for account_id in added_accounts:
                        self.accounts.add(Account.objects.get(id=account_id))
                elif deleted_accounts:
                    for account_id in deleted_accounts:
                        self.accounts.remove(Account.objects.get(id=account_id))
            if 'comments' in json_data:
                self.comments = json_data['comments']
            self.save()
        except IntegrityError:
            return Response.fail(ErrorMessage.duplicated(), StatusCode.DUPLICATED)
        else:
            return Response.success(self.read_as_json(), StatusCode.OK)

    @classmethod
    def create_as_json(cls, json_data):
        try:
            cls.objects.get(hostName=json_data['host_name'])
        except cls.DoesNotExist:
            cls.objects.create(
                hostName=json_data['host_name'],
                hostIp=json_data['host_ip'],
                hostEnv=json_data['host_env'],
                comments=json_data['comments'])
            new_host = cls.objects.get(hostName=json_data['host_name'])
            return Response.success(new_host.read_as_json(), StatusCode.OK)
        else:
            return Response.fail(ErrorMessage.duplicated(), StatusCode.DUPLICATED)



# class AccountHostMapping(models.Model):
#     # ORM attributes
#     account = models.ForeignKey(TblAccountInfo)
#     host = models.ForeignKey(Host)
#     # oprLevels => ('admin','developer','system','normal')
#     # operation level
#     oprLevel = models.CharField(max_length=10, default='normal')
#
#     class Meta:
#         db_table = "tblAccountHostMapping"
#
#
# class ServiceHostMapping(models.Model):
#     # ORM attributes
#     service = models.ForeignKey(TblServiceInfo)
#     host = models.ForeignKey(Host)
#     oprLevel = models.CharField(max_length=10, default='normal')
#
#     class Meta:
#         db_table = "tblServiceHostMapping"
