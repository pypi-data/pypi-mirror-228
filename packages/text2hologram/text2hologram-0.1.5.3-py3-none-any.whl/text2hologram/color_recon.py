import torch
import numpy as np
from odak.learn.tools import circular_binary_mask, zero_pad, crop_center
from odak.learn.wave.util import generate_complex_field, calculate_amplitude
import odak


class holographic_display():
    """
    A class for simulating a holographic display.
    """
    def __init__(self,
                 wavelengths,
                 pixel_pitch = 3.74e-6,
                 resolution = [1920, 1080],
                 volume_depth = 0.01,
                 number_of_depth_layers = 10,
                 image_location_offset = 0.005,
                 pinhole_size = 1500,
                 pad = [True, True],
                 illumination = None,
                 device = None
                ):
        """
        Parameters
        ----------
        wavelengths            : list
                                 List of wavelengths in meters (e.g., 531e-9).
        pixel_pitch            : float
                                 Pixel pitch in meters (e.g., 8e-6).
        resolution             : list
                                 Resolution (e.g., 1920 x 1080).
        volume_depth           : float
                                 Volume depth in meters.
        number_of_depth_layers : int
                                 Number of depth layers.
        image_location_offset  : float
                                 Image location offset in depth.
        pinhole_size           : int
                                 Size of the pinhole aperture in pixel in a 4f imaging system.
        pad                    : list
                                 Set it to list of True bools for zeropadding and cropping each time propagating (avoiding aliasing).
        illumination           : torch.tensor
                                 Provide the amplitude profile of the illumination source.
        device                 : torch.device
                                 Device to be used (e.g., cuda, cpu).
        """
        self.device = device
        if isinstance(self.device, type(None)):
            self.device = torch.device("cpu")
        self.pad = pad
        self.wavelengths = wavelengths
        self.resolution = resolution
        self.pixel_pitch = pixel_pitch
        self.volume_depth = volume_depth
        self.image_location_offset = torch.tensor(image_location_offset, device = device)
        self.number_of_depth_layers = number_of_depth_layers
        self.number_of_wavelengths = len(self.wavelengths)
        self.pinhole_size = pinhole_size
        self.init_distances()
        self.init_amplitude(illumination)
        self.init_aperture()
        self.generate_kernels()


    def init_aperture(self):
        """
        Internal function to initialize aperture.
        """
        self.aperture = circular_binary_mask(
                                             self.resolution[0] * 2,
                                             self.resolution[1] * 2,
                                             self.pinhole_size,
                                            ).to(self.device) * 1.


    def init_amplitude(self, illumination):
        """
        Internal function to set the amplitude of the illumination source.
        """
        self.amplitude = torch.ones(
                                    self.resolution[0],
                                    self.resolution[1],
                                    requires_grad = False,
                                    device = self.device
                                   )
        if not isinstance(illumination, type(None)):
            self.amplitude = illumination


    def init_distances(self):
        """
        Internal function to set the image plane distances.
        """
        if self.number_of_depth_layers > 1:
            self.distances = torch.linspace(
                                            -self.volume_depth / 2.,
                                            self.volume_depth / 2.,
                                            self.number_of_depth_layers,
                                            device = self.device
                                           ) + self.image_location_offset
        else:
            self.distances = torch.tensor([self.image_location_offset], device = self.device)


    def forward(self, input_field, wavelength_id, depth_id):
        """

        Function that represents the forward model in hologram optimization.

        Parameters
        ----------
        input_field         : torch.tensor
                              Input complex input field.
        wavelength_id       : int
                              Identifying the color primary to be used.
        depth_id            : int
                              Identifying the depth layer to be used.

        Returns
        -------
        output_field        : torch.tensor
                              Propagated output complex field.
        """
        if self.pad[0]:
            input_field_padded = zero_pad(input_field)
        else:
            input_field_padded = input_field
        H = self.kernels[depth_id, wavelength_id].detach().clone()
        U_I = torch.fft.fftshift(torch.fft.fft2(torch.fft.fftshift(input_field_padded)))
        U_O = (U_I * self.aperture) * H
        output_field_padded = torch.fft.ifftshift(torch.fft.ifft2(torch.fft.ifftshift(U_O)))
        if self.pad[1]:
            output_field = crop_center(output_field_padded)
        else:
            output_field = output_field_padded
        return output_field


    def generate_kernels(self):
        """
        Internal function to generate light transport kernels.
        """
        if self.pad[0]:
            multiplier = 2
        else:
            multiplier = 1
        self.kernels = torch.zeros(
                                   self.number_of_depth_layers,
                                   self.number_of_wavelengths,
                                   self.resolution[0] * multiplier,
                                   self.resolution[1] * multiplier,
                                   device = self.device,
                                   dtype = torch.complex64
                                  )
        for distance_id, distance in enumerate(self.distances):
            for wavelength_id, wavelength in enumerate(self.wavelengths):
                 self.kernels[distance_id, wavelength_id] = self.generate_kernel(
                                                                                 self.kernels.shape[-2],
                                                                                 self.kernels.shape[-1],
                                                                                 dx = self.pixel_pitch,
                                                                                 wavelength = wavelength,
                                                                                 distance = distance
                                                                                )


    def generate_kernel(self, nu, nv, dx = 8e-6, wavelength = 515e-9, distance = 0.):
        """
        Internal function used for self.propagate().
        """
        x = dx * float(nu)
        y = dx * float(nv)
        fx = torch.linspace(
                            -1 / (2 * dx) + 0.5 / (2 * x),
                            1 / (2 * dx) - 0.5 / (2 * x),
                            nu,
                            dtype = torch.float32,
                            device = self.device
                           )
        fy = torch.linspace(
                            -1 / (2 * dx) + 0.5 / (2 * y),
                            1 / (2 * dx) - 0.5 / (2 * y),
                            nv,
                            dtype = torch.float32,
                            device = self.device
                           )
        FY, FX = torch.meshgrid(fx, fy, indexing='ij')
        HH_exp = 2 * np.pi * torch.sqrt(1 / wavelength ** 2 - (FX ** 2 + FY ** 2))
        distance = torch.tensor([distance], device = self.device)
        H_exp = torch.mul(HH_exp, distance)
        fx_max = 1 / torch.sqrt((2 * distance * (1 / x))**2 + 1) / wavelength
        fy_max = 1 / torch.sqrt((2 * distance * (1 / y))**2 + 1) / wavelength
        H_filter = ((torch.abs(FX) < fx_max) & (torch.abs(FY) < fy_max)).clone().detach()
        H = generate_complex_field(H_filter, H_exp)
        return H


    def reconstruct(self, hologram_phases, laser_powers):
        """
        Internal function to reconstruct a given hologram.


        Parameters
        ----------
        hologram_phases            : torch.tensor
                                     A monochrome hologram phase [m x n].
        laser_powers               : torch.tensor
                                     Laser powers for each hologram phase.
                                     Values must be between zero and one.

        Returns
        -------
        reconstruction_intensities : torch.tensor
                                     Reconstructed frames [w x k x l x m x n].
                                     First dimension represents the number of frames.
                                     Second dimension represents the depth layers.
                                     Third dimension is for the color primaries (each wavelength provided).
        """
        self.number_of_frames = hologram_phases.shape[0]
        reconstruction_intensities = torch.zeros(
                                                 self.number_of_frames,
                                                 self.number_of_depth_layers,
                                                 self.number_of_wavelengths,
                                                 self.resolution[0],
                                                 self.resolution[1],
                                                 device = self.device
                                                )
        for frame_id in range(self.number_of_frames):
            for depth_id in range(self.number_of_depth_layers):
                for wavelength_id in range(self.number_of_wavelengths):
                    laser_power = laser_powers[frame_id][wavelength_id]
                    hologram = generate_complex_field(
                                                      laser_power * self.amplitude,
                                                      hologram_phases[frame_id]
                                                     )
                    reconstruction_field = self.forward(hologram, wavelength_id, depth_id)
                    reconstruction_intensities[frame_id, depth_id, wavelength_id] = calculate_amplitude(reconstruction_field) ** 2
        return reconstruction_intensities


def colored_recon(output_directory,name = 'combined_rgb.png',number_of_depth_layers=3):
    rgb_phase = output_directory+name
    device = torch.device('cuda')
    display = holographic_display(
                                                  wavelengths = [639e-9, 515e-9, 473e-9],
                                                  pixel_pitch = 3.74e-6,
                                                  resolution = [2400, 4094],
                                                  volume_depth = 0.01,
                                                  number_of_depth_layers = number_of_depth_layers,
                                                  image_location_offset = 5e-3,
                                                  pinhole_size = 1500,
                                                  device = device
                                                 )
    hologram_phases = odak.learn.tools.load_image(
                                                  rgb_phase, # sample_hologram
                                                  normalizeby = 255.,
                                                  torch_style = True
                                                 ) * odak.pi * 2.
    # print(hologram_phases)
    # print("shape is ", hologram_phases.shape, hologram_phases.max(),hologram_phases.min())
    laser_powers = torch.tensor([
                                 [1., 0., 0.],
                                 [0., 1., 0.],
                                 [0., 0., 1.],
                                ],
                                device = device
                               )
    reconstructions = display.reconstruct(hologram_phases = hologram_phases.to(device), laser_powers = laser_powers)
    combined_frame = torch.sum(reconstructions, dim = 0)
    # print(reconstructions)
    for depth_id in range(reconstructions.shape[1]):
        # print(combined_frame[depth_id].max(),combined_frame[depth_id].min(),combined_frame[depth_id].mean())
        odak.learn.tools.save_image(
                                    output_directory+'colored_recon_{:04d}.png'.format(depth_id),
                                    combined_frame[depth_id],
                                    cmin = 0.,
                                    cmax = 1.
                                   )
    assert True == True