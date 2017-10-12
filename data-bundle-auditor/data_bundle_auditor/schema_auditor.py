import json, requests, pprint
import properties

basePath = properties.base_url

def loadSchema(schema):

    req = requests.get(basePath + schema + ".json")
    ontologyProperties = []

    if(req.status_code == requests.codes.ok):
        jsonRaw = req.json()


        pp = pprint.PrettyPrinter(indent=4)

        properties = jsonRaw["properties"]

        for prop in properties:
            # pp.pprint(properties[prop])

            if ("$ref" in properties[prop]):
                if(properties[prop]["$ref"].find("ontology.json") != -1):
                    # print("Property " + prop + " should be mapped to an ontology term")
                    ontologyProperties.append(prop)
            elif("type" in properties[prop] and (properties[prop]["type"] == "array" and "$ref" in properties[prop]["items"])):
                if(properties[prop]["items"]["$ref"].find("ontology.json") != -1):
                    # print("Property " + prop + " should be mapped to an ontology term")
                    ontologyProperties.append(prop)
                # else:
            #         once the basic auditor works, add a recursive loop here that goes over each sub file and gets the relevant properties as well
            # else:
                # print("Property " + prop + " does not require mapping to an ontology term")
    else:
        print(basePath + schema + ".json does not exist")


    return ontologyProperties




if __name__ == '__main__':
    properties = loadSchema("sample.json")

    for p in properties:
        print(p)

    print("Properties loaded")