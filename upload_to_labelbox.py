#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
from graphqlclient import GraphQLClient


# TODO: Muss hier wirklich das "setupComplete"-Feld so aussehen?
def completeSetupOfProject(project_id, dataset_id, labeling_frontend_id):
    res_str = client.execute("""
    mutation CompleteSetupOfProject($projectId: ID!, $datasetId: ID!, $labelingFrontendId: ID!) {
      updateProject(
        where: {
          id: $projectId
        },
        data: {
          setupComplete: "2018-11-29T20:46:59.521Z",
          datasets: {
            connect: {
              id: $datasetId
            }
          },
          labelingFrontend: {
            connect: {
              id: $labelingFrontendId
            }
          }
        }
      ){
        id
      }
    }
    """, {
        'projectId': project_id,
        'datasetId': dataset_id,
        'labelingFrontendId': labeling_frontend_id
    })

    res = json.loads(res_str)
    return res['data']['updateProject']['id']


def configure_interface_for_project(ontology, project_id, interface_id, organization_id):
    res_str = client.execute("""
      mutation ConfigureInterfaceFromAPI($projectId: ID!, $customizationOptions: String!, $labelingFrontendId: ID!, $organizationId: ID!) {
        createLabelingFrontendOptions(data: {
          customizationOptions: $customizationOptions,
          project: {
            connect: {
              id: $projectId
            }
          }
          labelingFrontend: {
            connect: {
              id: $labelingFrontendId
            }
          }
          organization: {
            connect: {
              id: $organizationId
            }
          }
        }){
          id
        }
      }
    """, {
        'projectId': project_id,
        'customizationOptions': json.dumps(ontology),
        'labelingFrontendId': interface_id,
        'organizationId': organization_id,
    })

    res = json.loads(res_str)
    return res['data']['createLabelingFrontendOptions']['id']


def create_prediction_model(name, version):
    res_str = client.execute("""
      mutation CreatePredictionModelFromAPI($name: String!, $version: Int!) {
        createPredictionModel(data: {
          name: $name,
          version: $version
        }){
          id
        }
      }
    """, {
        'name': name,
        'version': version
    })

    res = json.loads(res_str)
    return res['data']['createPredictionModel']['id']


def attach_prediction_model_to_project(prediction_model_id, project_id):
    res_str = client.execute("""
      mutation AttachPredictionModel($predictionModelId: ID!, $projectId: ID!) {
        updateProject(where: {
          id: $projectId
        }, data: {
          activePredictionModel: {
            connect: {
              id: $predictionModelId
            }
          }
        }){
          id
        }
      }
    """, {
        'predictionModelId': prediction_model_id,
        'projectId': project_id
    })

    res = json.loads(res_str)
    return res['data']['updateProject']['id']


def create_prediction(label, prediction_model_id, project_id, data_row_id):
    res_str = client.execute("""
      mutation CreatePredictionFromAPI($label: String!, $predictionModelId: ID!, $projectId: ID!, $dataRowId: ID!) {
        createPrediction(data: {
          label: $label,
          predictionModelId: $predictionModelId,
          projectId: $projectId,
          dataRowId: $dataRowId,
        }){
          id
        }
      }
    """, {
        'label': label,
        'predictionModelId': prediction_model_id,
        'projectId': project_id,
        'dataRowId': data_row_id
    })

    res = json.loads(res_str)
    return res['data']['createPrediction']['id']



def create_datarow(row_data, external_id,dataset_id):
    res_str = client.execute("""
      mutation CreateDataRowFromAPI($rowData: String!, $externalId: String, $datasetId: ID!) {
        createDataRow(data: {
          externalId: $externalId,
          rowData: $rowData,
          dataset: {
            connect: {
              id: $datasetId
            }
          }
        }){
          id
        }
      }
    """, {
        'rowData': row_data,
        'externalId': external_id,
        'datasetId': dataset_id
    })

    res = json.loads(res_str)
    return res['data']['createDataRow']['id']



#
#
#
#
#



def upload(path):
    # Vlt kann man das hier noch etwas schoener laden!
    with open("/home/thahnen/GitHub/labelbox-scripts-etc/.api.key") as fd:
        key = fd.readline()

    # Connect to the Labelbox-Endpoint
    client = GraphQLClient("https://api.labelbox.com/graphql")
    client.inject_token(key)
    
    # Die JSON-Datei vorfinden und einlesen
    # sollte folgende Form haben:
    #
    # [
    #   {
    #       "frame_nr" : <Nr des Frames>
    #       "image_url" : "https://127.0.0.1:8000/<Name der Bilddatei>",
    #       "external_id" : "<Name der Bilddatei>"
    #       "prediction_label" : {
    #           object : [
    #               {
    #                   "geometry" : [
    #                       {
    #                           "x" : "<X-Koord.>", "y" : "<Y-Koord.>"
    #                       }, ... (4 mal aber nur weil Rechteck, aber kp ob mit oder gegen Uhrzeigersinn!)
    #                   ]
    #               }, ...
    #           ]
    #       }
    #   }, ...
    # ]
    #
    json_path = os.path.join(path, "darkflow_parsed.json")
    if not os.path.exists(json_path):
        return 1
    
    data = []
    try:
        data = json.load(json_path)
    except Exception as e:
        return 2

    # User Information for the Organization Id!
    user_info = json.loads(client.execute("""
        query GetUserInformation {
            user {
                id
                organization {
                    id
                }
            }
        }
    """))["data"]["user"]

    org_id = user_info["organization"]["id"]

    # Get the folder name, usefull for the name of the dataset as well as the project
    project_folder_name = path.split("/")[-2:][0].split("/")[0]
    folder_name = path.split("/")[-1:].split("/")[0]

    # Based on this names build the project and its datasets name
    project_dataset_name = f"DVS_F102 {project_folder_name} {folder_name}"

    # Every Project gets its own Dataset!
    # they use the data from the Darkflow-NNs!
    project_id = json.loads(client.execute("""
        mutation CreateProjectFromAPI($name: String!) {
            createProject(data: {
                name: $name
            }){
                id
            }
        }
    """, {'name': project_dataset_name}))['data']['createProject']['id']
    print(f"Created Project '{project_dataset_name}'")

    dataset_id = json.loads(client.execute("""
        mutation CreateDatasetFromAPI($name: String!) {
            createDataset(data: {
                name: $name
            }){
                id
            }
        }
    """, {'name': project_dataset_name}))['data']['createDataset']['id']
    print(f"Created Dataset '{project_dataset_name}'")

    # Set Interface for this specific project!
    # based on our own build Labeling-Interface-JSON!
    interface_id = json.loads(client.execute("""
        query GetImageLabelingInterfaceId {
            labelingFrontends(where: {
                iframeUrlPath: "https://image-segmentation-v4.labelbox.com"
            }){
                id
            }
        }
    """))['data']['labelingFrontends'][0]['id']

    labeling_interface = {
        "classifications": [],
        "tools": [
            {
                "tool": "rectangle",
                "name": "object",
                "color": "#F09300",
                "classifications": [
                    {
                        "name": "label-klasse",
                        "instructions": "Label-Klasse",
                        "type": "radio",
                        "options": [
                            {
                                "value": "person",
                                "label": "Person"
                            }, {
                                "value": "personengruppe",
                                "label": "Personengruppe"
                            }, {
                                "value": "fahrradfahrer",
                                "label": "Fahrradfahrer"
                            }, {
                                "value": "anderes",
                                "label": "Anderes"
                            }
                        ],
                        "required": true
                    }, {
                        "name": "label_id",
                        "instructions": "Label (id, id+id, id|id)",
                        "type": "text",
                        "options": [
                            {
                                "value": "",
                                "label": ""
                            }
                        ],
                        "required": true
                    }
                ]
            }
        ]
    }

    configure_interface_for_project(labeling_interface, project_id, interface_id, org_id)
    print("Interface added to project!")

    # Complete Setup of this specific project!
    completeSetupOfProject(project_id, dataset_id, interface_id)

    # Create Prediction
    prediction_model_id = create_prediction_model("Darkflow", 1)
    attach_prediction_model_to_project(prediction_model_id, project_id)
    print(f"Created prediction {prediction_model_id}")

    # Create and upload datarow!
    # But beware not to send more than 300 requests per minute!
    amount_uploads = 0
    time_allowed = 1/150    # because there are two requests each loop!
    for elem in data:
        begin = time.time()
        try:
            data_row_id = create_datarow(row["image_url"], row["external_id"], dataset_id)
            print(f"Created DataRow : {data_row_id})

            prediction_id = create_prediction(json.dumps(row["prediction_label"]), prediction_model_id, project_id, data_row_id)
            print(f"Created Prediction: {prediction_id}")

            duration = time.time()-begin
            if (duration < time_allowed):
                time.sleep((time_allowed-duration)*1.05)    # waits to not get over the allowed amount of request
        except Exception as e:
            # What shall we do with this drunken sailor?
            pass
    
    


if __name__ == "__main__":
    if len(sys.argv == 2):
        path = sys.argv[1]
        if os.path.exists(path) and os.path.isdir(path):
            try:
                status = upload(path)
            except Exception as e:
                print(e)
                exit(1)

            if status == 1:
                print("Es wurde im Ordner keine JSON-Datei gefunden!")
            elif status == 2:
                print("Die JSON-Datei konnte nicht gelesen werden!")
            else:
                print("Datensatz erfolgreich hochgeladen!")
                exit(0)
        else:
            print("Bei dem angegebenen Pfad handelt es sich nicht um ein Verzeichnis!")
    else:
        print("Es muss ein Ordner angegeben werden, der alle Bilder und die jeweiligen Frame-Infos fuer den Datensatz enthaellt!")
    
    exit(1)
