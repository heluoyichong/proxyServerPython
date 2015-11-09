BEGIN;
CREATE DATABASE `proxyServer`;
USE proxyServer;

CREATE TABLE `tblAdminInfo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `firstName` varchar(80) NOT NULL,
    `lastName` varchar(80) NOT NULL,
    `emailAddr` varchar(254) NOT NULL,
    `loginName` varchar(80) NOT NULL UNIQUE,
    `loginPass` varchar(32) NOT NULL
)
;
CREATE TABLE `tblAccountInfo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `firstName` varchar(80) NOT NULL,
    `lastName` varchar(80) NOT NULL,
    `emailAddr` varchar(254) NOT NULL,
    `loginName` varchar(80) NOT NULL UNIQUE,
    `loginPass` varchar(32) NOT NULL
)
;
CREATE TABLE `tblHostInfo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `hostName` varchar(80) NOT NULL UNIQUE,
    `hostIp` char(39) NOT NULL,
    `hostEnv` varchar(10) NOT NULL,
    `comments` varchar(512) NOT NULL
)
;
CREATE TABLE `tblServiceInfo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `serviceName` varchar(80) NOT NULL UNIQUE,
    `portNumber` integer NOT NULL UNIQUE,
    `comments` varchar(512) NOT NULL
)
;
CREATE TABLE `tblAccountHostMapping` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `account_id` integer NOT NULL,
    `host_id` integer NOT NULL,
    `oprLevel` varchar(10) NOT NULL
)
;
ALTER TABLE `tblAccountHostMapping` ADD FOREIGN KEY (`account_id`) REFERENCES `tblAccountInfo` (`id`);
ALTER TABLE `tblAccountHostMapping` ADD FOREIGN KEY (`host_id`) REFERENCES `tblHostInfo` (`id`);

CREATE TABLE `tblServiceHostMapping` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `service_id` integer NOT NULL,
    `host_id` integer NOT NULL,
    `oprLevel` varchar(10) NOT NULL
)
;
ALTER TABLE `tblServiceHostMapping` ADD FOREIGN KEY (`host_id`) REFERENCES `tblHostInfo` (`id`);
ALTER TABLE `tblServiceHostMapping` ADD FOREIGN KEY (`service_id`) REFERENCES `tblServiceInfo` (`id`);

CREATE INDEX `tblAccountHostMapping_accountId` ON `tblAccountHostMapping` (`account_id`);
CREATE INDEX `tblAccountHostMapping_hostId` ON `tblAccountHostMapping` (`host_id`);
CREATE INDEX `tblServiceHostMapping_serviceId` ON `tblServiceHostMapping` (`service_id`);
CREATE INDEX `tblServiceHostMapping_hostId` ON `tblServiceHostMapping` (`host_id`);

COMMIT;
