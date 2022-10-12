# geoe3-quality-dashboard
GeoE3 quality dashboard - method for scoring services using metadata and monitoring information. You can read more about the project at https://geoe3.eu/ and https://geoe3platform.eu/geoe3/




## Source of the dashboard data

1. Dataset metadata (data provider)
2. Service metadata OR Service description Capabilities document (data or service provider)
3. Quality evaluation results (part of the GeoE3 project)
4. Service availability information (Spatineo)

Sources 1 and 2 are XML files that can be downloaded from wherever catalogues they reside from

Source 3 is still undecided how to retrieve the information. The Quality software is based on FME and the workbench which analyses the actual contenst of the dataset. It could produce a machine readable file that the dashboard could read in. Currently it produces CSV files but it is unclear how those can be integrated into the process. Needs work.

Source 4 data will be downloaded from an API that Spatineo will provide. Details are still to be decided.

## The evaluation process

1. Start with a list of datasets, the each dataset includes the following information:
    - link to dataset metadata
    - link to servie metadata for a (single) service that is used to disseminate the dataset
    - linkage to the Quality evaluation results (TBD)
    - linkage to the service availability information (TBD)
2. Configuration file that includes viewpoints, their dimensions, all the way up to metrics. Each metric includes extraction rules on how to extract information to evaluate that metric for a particular dataset
    - an exatraction rule may target one of the sources (dataset metadata, service metadata, quality software output, or availability information)
3. Configuration also includes the evaluation criteria used to assess whether the extraction output meets requirements => gives a score for that metric
4. Scores are then combined up the quality hierarchy with weights applied (weights are stored in the configuration file)
5. Output in tabular format (for example CSV) so that it is easily usable in the dashboard application (for example Power BI)

## Configuration file format


### Extraction rules

```
  ... 
  "extractionRule": {
    "source": "dataset-metadata", 
    "type": "xpath",
    "rule": ".//gmd:MD_Metadata/gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString"
  }
```

`source` = one of `dataset-metadata`, `service-metadata`, `quality-evaluation`, `service-description` (e.g. WFS Capabilities document), or `service-availability`


