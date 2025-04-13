![PyPI - Version](https://img.shields.io/pypi/v/vaapi)
![GitHub License](https://img.shields.io/github/license/BerlinUnited/Visual-Analytics)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/BerlinUnited/Visual-Analytics/build_backend.yml)

# Berlin United Visual Analytics Tool

The goal of of this tool is to make it possible to quickly view, annotate and analyze all of our recorded RoboCup data. To learn more about RoboCup and our team have a look at https://berlin-united.org/ and https://spl.robocup.org/

We are heavily inspired and built upon the previous work of

- https://github.com/bhuman/VideoAnalysis
- https://www2.informatik.hu-berlin.de/~naoth/videolabeling/
- https://docs.berlinunited.org/naoth_tools/rc/

This tool provides a database model and an API for our recorded data along with a Frontend to view and annotate the data. We provide a synchronized view of all logs and external video recordings.
This tool is intended to be used within the Berlin United code ecosystem. For parsing log files we use the [naoth pip package](https://pypi.org/project/naoth/) and for inserting the parsed data in the db we use https://pypi.org/project/vaapi/

A live version can be accessed at https://vat.berlin-united.com/

## Setup locally

Dev environment setup is described [here](docs/dev-setup.md).
