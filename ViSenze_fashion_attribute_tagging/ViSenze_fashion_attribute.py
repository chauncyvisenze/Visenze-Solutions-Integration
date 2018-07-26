#!/usr/bin/python3

import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import os
import glob
import argparse

# Add flags to the program
parser = argparse.ArgumentParser(description='ViSenze recognition fashion attribute tagging')
parser.add_argument('-f','--folder', type=str, metavar='', help='the path of the folder where all images are stored', required=True)
parser.add_argument('-u','--access_key', type=str, metavar='', help='the access key in our ViSenze dashboard', required=True)
parser.add_argument('-p','--secret_key', type=str, metavar='', help='the secret key in our Visenze dashboard', required=True)
parser.add_argument('-o','--output', type=str, metavar='', help='the path of the output csv file', required=True)
args = parser.parse_args()


# Process ViSenze /recognize API response


def process_response(res):
    jd = json.loads(res.text)
    return jd['result'][0]['objects']

# Parse ViSenze /recognize API response


def parse_tag(tag_dict):
    tag_list = []
    for i in range(len(tag_dict)):
        if len(list(tag_dict.values())[i]) > 0:
            for elmt in list(tag_dict.values())[i]:
                new_dict = {}
                new_dict['filename'] = list(tag_dict.keys())[i]
                for tag in elmt['tags']:
                    result = tag['tag'].split(':')
                    key = result[0]
                    val = result[-1]
                    new_dict[key] = val
                tag_list.append(new_dict)
    return tag_list

# Output tagging results into a csv file


def output_to_csv(tag_list):
    df = pd.DataFrame(tag_list)
    cols = list(df)
    cols.insert(0, cols.pop(cols.index('filename')))
    cols.insert(1, cols.pop(cols.index('category')))
    df = df.loc[:, cols]
    return df


# Given a folder path, call ViSenze /recognize API response to obtain fashion attributes


def visenze_fashion_attribute(folder_path,access_key,secret_key, output_path):
    tag_dict = {}

    url = "https://virecognition.visenze.com/v1/image/recognize"
    auth = HTTPBasicAuth(access_key, secret_key)

    index = 0
    print('Starting recognition...')
    for filename in glob.glob(os.path.join(folder_path, '*g')):
        data = {'file':open(filename,'rb'),
                'tag_group':"fashion_attributes",
                'vtt_source':"visenze_admin"
                }
        print ('Waiting for recognition response for file #{}...'.format(index))
        res = requests.post(url=url,auth=auth,files=data)
        print ('Retrieved recognition response for file #{}...'.format(index))
        tag_dict[filename] = process_response(res)
        index += 1

    print('Parsing all responses...')
    tag_list = parse_tag(tag_dict)
    df = output_to_csv(tag_list)
    df.to_csv(output_path, encoding='utf-8', index=False)
    print ('Finished!')


if __name__ == '__main__':
    visenze_fashion_attribute(args.folder,args.access_key,args.secret_key,args.output)