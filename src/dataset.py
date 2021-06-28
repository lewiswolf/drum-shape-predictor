# core
import json
import os
from typing import TypedDict

# dependencies
from tqdm import tqdm	# CLI progress bar

# src
from settings import settings


class Sample(TypedDict):
	'''
	Class declaration for each data sample.
	'''
	filepath: str
	labels: list


class DatasetMetadata(TypedDict):
	'''
	This class is used when exporting and importing the metadata for the dataset.
	This object and the settings object are compared to ensure a loaded dataset matches
	the project settings.
	'''
	NUM_OF_TARGETS: int
	SAMPLE_RATE: int
	data: list[Sample]


def generateDataset() -> list[Sample]:
	'''
	Generates a dataset of drum sounds and returns the metadata.
	The generated dataset, including the individual .wav files and the metadata.json,
	is saved in ../data.
	'''

	print('Generating dataset... 🎯')
	metadata: DatasetMetadata = {
		'NUM_OF_TARGETS': settings['NUM_OF_TARGETS'],
		'SAMPLE_RATE': settings['SAMPLE_RATE'],
		'data': [],
	}

	# clear dataset folder
	datasetFolder = os.path.join(os.getcwd(), 'data')
	for file in os.listdir(datasetFolder):
		if (file != '.gitignore'):
			os.remove(os.path.join(datasetFolder, file))

	# generate datatset
	with tqdm(
		bar_format='{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}, Elapsed: {elapsed}, ETA: {remaining}, {rate_fmt}  ',
		unit=' data samples',
		total=settings['NUM_OF_TARGETS']
	) as pbar:
		for i in range(settings['NUM_OF_TARGETS']):
			'''
			do stuff
			'''
			pbar.update(1)

	# export metadata json
	with open(os.path.join(os.getcwd(), 'data/metadata.json'), 'w') as json_file:
		json.dump(metadata, json_file)

	return metadata['data']


def loadDataset() -> list[Sample]:
	'''
	Attempts to load a dataset if one has already been generated.
	Compares the metadata of the loaded dataset, and ammends the dataset if necessary.
	'''

	# custom exception if dataset generation settings do not match the project setttings.
	class DatasetIncompatible(Exception):
		pass

	# load a dataset if it exists
	try:
		metadata: DatasetMetadata = json.load(open(os.path.join(os.getcwd(), 'data/metadata.json'), 'r'))

		# if the project settings and data settings do not align, throw error
		if (metadata['NUM_OF_TARGETS'] < settings['NUM_OF_TARGETS'] or metadata['SAMPLE_RATE'] != settings['SAMPLE_RATE']):
			raise DatasetIncompatible

		# if the dataset is bigger than the project settings, trim its size
		if (metadata['NUM_OF_TARGETS'] != settings['NUM_OF_TARGETS']):
			metadata['data'] = metadata['data'][: settings['NUM_OF_TARGETS']]
			
		dataset = metadata['data']

	except (FileNotFoundError, DatasetIncompatible):
		# regenerate new dataset if import fails
		dataset = generateDataset()

	return dataset
