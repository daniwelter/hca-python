import properties, requests, pprint

pp = pprint.PrettyPrinter(indent=4)

query_parameter = properties.replica_query_parameter

def getDataFilesForBundle(uuid):
    # bundle -> files -> check 'name' for .json extension -> get UUID

    dataStoreBundle = properties.data_store_bundle

    jsonRaw = requests.get(dataStoreBundle + uuid + query_parameter).json()

    files = jsonRaw["bundle"]["files"]

    fileUuids = {}

    for file in files:
       if(file["name"].find(".json") != -1):
            name = file["name"].split(".")[0]
            uuid = file["uuid"]
            pp.pprint(name + " " + uuid)
            fileUuids[name] = uuid

    return fileUuids #return dictionary file-name : uuid



def auditSchemaFile(schemaFileType, uuid, fields):

    dataStoreFile = properties.data_store_file

    # url = dataStoreFile + uuid + query_parameter
    #
    # pp.pprint(url)
    # pp.pprint(schemaFileType)
    # pp.pprint(fields)

    fileJson = requests.get(dataStoreFile + uuid + query_parameter).json()

    schemaFields = {}

    for field in fields:
        if(field in fileJson):
            val = fileJson[field]["text"]
            pp.pprint(field + " - " + val)
            schemaFields[field] = val

        else:
            # pp.pprint(field + " not found in schema file for " + schemaFileType + " " + uuid)
            schemaFields[field] = "n/a"
            pp.pprint(field + " - n/a")

    #get the correct file back, then audit the fields listed in the schema as ontolgy fields
    return schemaFields  #return dictionary field : value




if __name__ == '__main__':
    properties = getDataFilesForBundle("sample.json")

    for p in properties:
        print(p)

    print("Properties loaded")

