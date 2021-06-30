'''
This file is used to define and configure the project settings.
'''

from typing import TypedDict


class Settings(TypedDict):
	DATASET_SIZE: int		# how many data samples are there in the dataset?
	DATA_LENGTH: float		# length of each sample in the dataset (seconds)
	SAMPLE_RATE: int		# audio sample rate (hz)


# the configurable object
settings: Settings = {
	'DATASET_SIZE': 10,
	'DATA_LENGTH': 5.0,
	'SAMPLE_RATE': 44100,
}
