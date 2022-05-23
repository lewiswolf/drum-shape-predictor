# dependencies
import torch				# pytorch

# src
from .audio_sampler import SamplerSettings
from .input_representation import RepresentationSettings

__all__ = [
	'TorchDataset',
]


class TorchDataset(torch.utils.data.Dataset):
	'''
	Pytorch wrapper for the generated/loaded dataset. Formats the dataset's input data
	into a tensor self.X, and the labels, if present, into a tensor self.Y.
	'''

	dataset_dir: str
	representation_settings: RepresentationSettings
	sampler: str
	sampler_settings: SamplerSettings
	X: torch.Tensor
	Y: torch.Tensor

	def __init__(
		self,
		dataset_dir: str,
		dataset_size: int,
		representation_settings: RepresentationSettings,
		sampler: str,
		sampler_settings: SamplerSettings,
		x_size: tuple[int, ...],
	) -> None:
		''' Initialise dataset. '''
		self.dataset_dir = dataset_dir
		self.representation_settings = representation_settings
		self.sampler = sampler
		self.sampler_settings = sampler_settings
		self.X = torch.zeros((dataset_size,) + x_size)

	def __getitem__(self, i: int) -> tuple[torch.Tensor, torch.Tensor]:
		'''
		Return the data and its labels, if they exist.
		'''
		if not hasattr(self, 'Y'):
			raise ValueError('Dataset contains no data.')
		return self.X[i], self.Y[i]

	def __len__(self) -> int:
		'''
		Return the dataset size.
		'''
		return self.X.shape[0]

	def __setitem__(self, i: int, x: torch.Tensor, y: torch.Tensor) -> None:
		'''
		Set self.X and self.Y at a specific index. If self.Y doesn't already exist,
		it is initialised here.
		'''
		# if self.Y does not yet exist, create the shape for Y
		if not hasattr(self, 'Y'):
			self.Y = torch.zeros((self.__len__(), ) + y.shape)
		# add data samples to self
		self.X[i] = x
		self.Y[i] = y