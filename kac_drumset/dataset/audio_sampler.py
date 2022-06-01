'''
This file contains the abstract parent class for an AudioSampler. By inheriting from this class, a custom AudioSampler
can be created to work alongside the dataset generator. This file has been designed such that each custom AudioSampler
will maintain functionality and type consistency throughout this codebase.
'''

# core
from abc import ABC, abstractmethod
import math
from typing import Literal, TypedDict, Union

# dependencies
import numpy as np				# maths
import numpy.typing as npt		# typing for numpy
import soundfile as sf			# audio read & write

__all__ = [
	'AudioSampler',
	'SamplerSettings',
]


class SamplerSettings(TypedDict, total=True):
	'''
	These are the minimum requirements for the AudioSampler __init__() method. This type is used to maintain type safety
	when using a custom AudioSampler.
	'''
	duration: float		# duration of the audio file (seconds)
	sample_rate: int	# sample rate


class AudioSampler(ABC):
	'''
	Abstract parent class for an audio sampler. The intended use when deployed:

	sampler = AudioSampler()
	for i in range(N):
		sampler.updateParameters(i)
		sampler.generateWaveform()
		x = sampler.waveform
		y = sampler.getLabels()
		sampler.export('/absolute/filepath/')
	'''

	duration: float						# duration of the audio file (seconds)
	length: int							# length of the audio file (samples)
	sample_rate: int					# sample rate
	waveform: npt.NDArray[np.float64]	# the audio sample itself

	def __init__(self, duration: float, sample_rate: int) -> None:
		''' Initialise sampler. '''
		self.duration = duration
		self.sample_rate = sample_rate
		self.length = math.ceil(duration * sample_rate)
		self.waveform = np.zeros(self.length)

	def export(self, absolutePath: str, bit_depth: Literal[16, 24, 32] = 24) -> None:
		''' Write the generated waveform to a .wav file. '''
		sf.write(absolutePath, self.waveform, self.sample_rate, subtype=f'PCM_{bit_depth}')

	@abstractmethod
	def generateWaveform(self) -> None:
		''' This method should be used to generate and set self.waveform. '''
		pass

	@abstractmethod
	def getLabels(self) -> list[Union[float, int]]:
		''' This method should return the y labels for the generated audio. '''
		pass

	@abstractmethod
	def updateProperties(self, i: Union[int, None] = None) -> None:
		''' This method should be used to update the properties of the sampler when inside a generator loop. '''
		pass

	@abstractmethod
	class Settings(SamplerSettings, total=False):
		'''
		This is an abstract TypedDict used to mirror the type declaration for the customised __init__() method. This allows
		for type safety when using a custom AudioSampler with an arbitrary __init__() method.
		'''
		pass
