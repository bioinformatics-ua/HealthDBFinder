#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import os
# import sys
# import time

# import json
# import numpy as np
import pandas as pd
# import requests


filepath = '/home/biocreative/CAT1/athena-ohdsi-vocabularies/bundle-v2/CONCEPT_RELATIONSHIP.csv'

df = pd.read_csv(filepath, sep='\t')

relation_ids = set(df['relationship_id'])

print(relation_ids)

print(len(relation_ids))
