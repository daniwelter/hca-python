import properties, requests, pprint

from data_bundle_auditor.bundle_auditor import getDataFilesForBundle, auditSchemaFile
from data_bundle_auditor.schema_auditor import loadSchema

pp = pprint.PrettyPrinter(indent=4)

metaDataOntologyFields = {}

def identifyAllDataBundles():
    bundleManifest = properties.ingest_bundle_manifest
    jsonRaw = requests.get(bundleManifest).json()

    uuids = []

    manifests = jsonRaw["_embedded"]["bundleManifests"]

    for manifest in manifests:
        uuids.append(manifest["bundleUuid"])
    return uuids




if __name__ == '__main__':
    uuids = identifyAllDataBundles()

    print("UUIDs loaded")

    for uuid in uuids:
        pp.pprint(uuid)

    summaryData = {}

    for uuid in uuids:
        dataFiles = getDataFilesForBundle(uuid)

        for fileType in dataFiles.keys():
            if(fileType not in metaDataOntologyFields.keys()):
                pp.pprint(fileType)
                properties = loadSchema(fileType)

                metaDataOntologyFields[fileType] = properties
                for p in properties:
                    pp.pprint(" " + p)

            fields = auditSchemaFile(fileType, dataFiles[fileType], metaDataOntologyFields[fileType])

            summaryData[fileType + "_" + uuid] = fields


    for key in summaryData.keys():
        pp.pprint(key)

        for f in summaryData[key]:
            if(type(f) == 'str'):
                pp.pprint(" " + f + " - ")
            else:
                for d in f.keys():
                    pp.pprint(" " + d + " - " + f[d])