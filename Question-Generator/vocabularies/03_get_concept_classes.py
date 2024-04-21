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

df = pd.read_csv(filepath, sep='\t')

concept_class_ids = set(df['concept_class_id'])

print(concept_class_ids)

print(len(concept_class_ids))
