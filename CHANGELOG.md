# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Guiding Principles:
* Changelogs are for humans, not machines.
* There should be an entry for every single version.
* The same types of changes should be grouped.
* Versions and sections should be linkable.
* The latest version comes first.
* The release date of each version is displayed.
* Mention whether you follow Semantic Versioning.

Types of changes:
Added - for new features
Changed - for changes in existing functionality
Deprecated - for soon-to-be removed features
Removed - for now removed features
Fixed - for any bug fixes
Security - in case of vulnerabilities
-->

## [0.9.0] - 2025-11-06

### Security

- Updated Alpine base image to v3.22
- Internal tracking ticket: CASMHMS-6551

## [0.8.0] - 2025-03-14

### Security

- Updated image dependencies for security updates
- Used virtual environment for pip installs in Dockerfiles
- Fixed some build warnings in the Dockerfile
- s/docker compose/docker-compose/ in docker compose file

## [0.7.0] - 2022-07-29

### Changed

- Updated hms-mountain-discovery to build using GitHub Actions instead of Jenkins.
- Pull images from artifactory.algol60.net instead of arti.dev.cray.com.
- Updated and fixed runUnitTest.sh.

## [0.6.0] - 2021-11-03

### Fixed

- Stop including disabled components in operations.

## [0.5.1] - 2021-08-10

### Changed

- Added GitHub configuration files.

## [0.5.0] - 2021-07-20

### Changed

- Add support for building within the CSM Jenkins.

## [0.4.1] - 2021-04-14

### Changed

- Updated Dockerfiles to pull base images from Artifactory instead of DTR.

## [0.4.0] - 2021-02-02

### Changed

- Updated license files.

## [0.3.0] - 2021-01-14

### Changed

- Updated license file.

## [0.2.0] - 2020-09-04

### Security

- CASMHMS-2989 - Updated hms-mountain-discovery to use latest trusted baseOS images.

## [0.1.0] - 2020-03-11

### Fixed

- use latest version of flask for synthetic-sls

## [0.0.3] - 2019-11-20

### Fixed

- added logic so that an empty targets list from HSM causes program exit, because passing an empty list to CAPMC causes EVERYTHING to be returned.

## [0.0.2] - 2019-11-18

### Fixed

- corrrected the Jenkinsfile to build for mountain-discovery

## [0.0.1] - 2019-11-13

### Added

- This is the initial release.
