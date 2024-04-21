#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import os
# import sys
# import time

# import json
# import numpy as np
import pandas as pd
# import requests


filepath = '/home/biocreative/CAT1/athena-ohdsi-vocabularies/bundle-v2/CONCEPT.csv'

concept_ids = set()

with open(filepath, mode='r', encoding='utf-8') as fp:
    for line in fp:
        concept_id, concept_name, domain_id, vocabulary_id, \
        concept_class_id, standard_concept, concept_code, \
        valid_start_date, valid_end_date, invalid_reason = line.split('\t')
        #
        concept_ids.add(concept_id)


filepath2 = '/home/biocreative/CAT1/CAT1-Question-Generator/datasets/sqllab_untitled_query_2_20240330T192808.csv'
# filepath2 = '/home/biocreative/CAT1/CAT1-Question-Generator/datasets/sqllab_untitled_query_2_20240330T193153.csv'

df = pd.read_csv(filepath2)

dataset_concept_ids = {str(i) for i in set(df['concept_id'])}

print(dataset_concept_ids - concept_ids)
