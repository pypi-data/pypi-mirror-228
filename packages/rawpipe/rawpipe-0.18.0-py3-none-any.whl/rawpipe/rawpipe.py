"""
A collection of reference ISP algorithms.
"""

import numbers               # built-in library
import time                  # built-in library
from typing import Type      # built-in library
from typing import Tuple     # built-in library
from typing import Sized     # built-in library
from typing import Iterable  # built-in library
from typing import Optional  # built-in library
from typing import Callable  # built-in library
import numpy as np           # pip install numpy
import cv2                   # pip install opencv-python


######################################################################################
#
#  P U B L I C   A P I
#
######################################################################################


class Algorithms:
    """
    A collection of ISP algorithms. See help(rawpipe) for documentation.
    """

    def __init__(self, verbose=False):
        """
        Initialize self. If verbose is True, progress information will be printed
        to stdout.
        """
        self.verbose = verbose

    def clip(self, frame: np.ndarray, lo: float = 0.0, hi: float = 1.0) -> np.ndarray:
        """
        Clip all pixels in the given frame to [lo, hi]. The frame may be in either
        RGB or raw format.
        """
        t0 = time.time()
        frame_out = np.clip(frame, lo, hi)
        self._vprint(f"{_elapsed(t0)} - clipping from {self._minmax(frame)} to [{lo:.2f}, {hi:.2f}]")
        return frame_out

    def bayer_split(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split the given Bayer frame into four single-color frames.
        """
        ch1 = frame[0::2, 0::2]
        ch2 = frame[0::2, 1::2]
        ch3 = frame[1::2, 0::2]
        ch4 = frame[1::2, 1::2]
        return ch1, ch2, ch3, ch4

    def bayer_combine(self,
                      ch1: np.ndarray,
                      ch2: np.ndarray,
                      ch3: np.ndarray,
                      ch4: np.ndarray) -> np.ndarray:
        """
        Interleave the given Bayer channels into a complete frame.
        """
        frame = np.zeros(np.array(ch1.shape) * 2, dtype=ch1.dtype)
        frame[0::2, 0::2] = ch1
        frame[0::2, 1::2] = ch2
        frame[1::2, 0::2] = ch3
        frame[1::2, 1::2] = ch4
        return frame

    def downsample(self, frame: np.ndarray, iterations: int = 1) -> np.ndarray:
        """
        Downsample the given RGB or grayscale frame by a factor of two in both
        directions, that is, to a quarter of its original size, using a simple
        2 x 2 box filter. This is repeated for a given number of iterations. If
        iterations is zero, the frame is returned untouched. See resize() for
        arbitrary resizing with proper interpolation.
        """
        if iterations >= 1:
            t0 = time.time()
            dt = frame.dtype
            orgh, orgw = frame.shape[:2]
            for _ in range(iterations):
                ch1, ch2, ch3, ch4 = self.bayer_split(frame)
                frame = np.stack((ch1, ch2, ch3, ch4))
                frame = np.mean(frame, axis=0)
            if issubclass(dt.type, numbers.Integral):
                frame = np.rint(frame)
            frame = frame.astype(dt)
            imgh, imgw = frame.shape[:2]
            factor = f"{2**iterations} x {2**iterations}"
            self._vprint(f"{_elapsed(t0)} - downsampling [{factor}] from {orgw} x {orgh} to {imgw} x {imgh}")
        return frame

    def resize(self, frame: np.ndarray, target_width: int, target_height: int) -> np.ndarray:
        """
        Resize the given RGB frame to the given target width and height using Lanczos
        interpolation. If target width and height are the same as current width and
        height, the frame is returned untouched.
        """
        t0 = time.time()
        orgh, orgw = frame.shape[:2]
        dsth, dstw = int(target_height), int(target_width)
        if (dstw, dsth) != (orgw, orgh):
            dt = frame.dtype
            frame = frame.astype(np.float32) if dt == np.float16 else frame
            assert frame.dtype in [np.float32, np.float64, np.uint8, np.uint16], f"unsupported dtype: {dt}"
            frame = cv2.resize(frame, (dstw, dsth), cv2.INTER_LANCZOS4)
            frame = frame.astype(dt)
            dsth, dstw = frame.shape[:2]
            self._vprint(f"{_elapsed(t0)} - resizing [Lanczos] from {orgw} x {orgh} to {dstw} x {dsth}")
        return frame

    def subtract(self, frame: np.ndarray, blacklevels: Iterable) -> np.ndarray:
        """
        Subtract per-channel black levels from the given frame, but do not linearize.
        For demosaiced RGB frames, blacklevels must contain three values; for raw Bayer
        frames, four values are required. The caller is responsible for making sure
        that the per-channel levels are in the same Bayer order as the frame itself.
        """
        t0 = time.time()
        levels = np.asarray(blacklevels, dtype=frame.dtype)
        if frame.ndim == 3:  # already demosaiced
            assert levels.size == 3, levels
            frame = np.maximum(frame, levels)
            frame = frame - levels
        else:  # raw Bayer
            assert levels.size == 4, levels
            rggb = list(self.bayer_split(frame))
            rggb = [np.maximum(ch, level) - level for ch, level in zip(rggb, levels)]
            frame = self.bayer_combine(*rggb)
        self._vprint(f"{_elapsed(t0)} - subtracting black levels {levels}: range = {self._minmax(frame)}")
        return frame

    def linearize(self,
                  frame: np.ndarray,
                  blacklevel: float = None,
                  whitelevel: float = None,
                  num_clipped: int = 1000) -> np.ndarray:
        """
        Linearize the given frame such that pixels are first clipped to the range
        [BL, WL] and then remapped to [0, 1], where BL and WL are the given black
        level and white level, respectively. If blacklevel is None, it is taken to
        be the Nth smallest pixel value within the frame, where N = num_clipped+1.
        A missing whitelevel is similarly estimated as the Nth largest pixel value.
        This algorithm is format-agnostic, although it's typically applied on raw
        sensor data.
        """
        minmax = self._minmax(frame)
        if blacklevel is None:
            t0 = time.time()
            percentile = num_clipped / frame.size * 100.0
            blacklevel = np.percentile(frame, percentile)
            self._vprint(f"{_elapsed(t0)} - estimating black level: {percentile:5.2f}th percentile = {blacklevel:.2f}")
        if whitelevel is None:
            t0 = time.time()
            percentile = (1.0 - num_clipped / frame.size) * 100.0
            whitelevel = np.percentile(frame, percentile)
            self._vprint(f"{_elapsed(t0)} - estimating white level: {percentile:5.2f}th percentile = {whitelevel:.2f}")
        assert whitelevel > blacklevel, f"{whitelevel} is not greater than {blacklevel}"
        frame = np.clip(frame, blacklevel, whitelevel)
        frame = frame.astype(np.float32)
        t0 = time.time()
        frame -= blacklevel
        frame = frame / (whitelevel - blacklevel)
        ranges = f"{minmax} => [{blacklevel:.2f}, {whitelevel:.2f}] => {self._minmax(frame)}"
        self._vprint(f"{_elapsed(t0)} - linearizing: range = {ranges}")
        return frame

    def demosaic(self,
                 frame: np.ndarray,
                 bayer_pattern: str,
                 downsample: bool = False) -> np.ndarray:
        """
        Demosaic the given sensor raw frame using the Edge Aware Demosaicing (EAD)
        algorithm. Bayer order must be specified by the caller, and must be "RGGB",
        "GBRG", "BGGR", or "GRBG". The frame must be in floating-point format with
        all pixel values in the [0, 1] range.

        If the 'downsample' flag is True, RGB values are picked from the raw Bayer
        pattern as-is, without any interpolation other than averaging the greens.
        This reduces the size of the image by a factor of 2 x 2. In 'downsample'
        mode, pixel values need not be in [0, 1] range.
        """
        t0 = time.time()
        if not downsample:
            assert np.all((frame >= 0.0) * (frame <= 1.0)), "demosaic() requires pixel values in range [0, 1]"
            bayer_to_cv2 = {"RGGB": cv2.COLOR_BAYER_BG2RGB_EA,
                            "GBRG": cv2.COLOR_BAYER_GR2RGB_EA,
                            "BGGR": cv2.COLOR_BAYER_RG2RGB_EA,
                            "GRBG": cv2.COLOR_BAYER_GB2RGB_EA}
            dt = frame.dtype
            frame = np.rint(frame * 65535).astype(np.uint16)
            frame = cv2.cvtColor(frame, bayer_to_cv2[bayer_pattern.upper()])
            frame = frame / 65535.0
            frame = frame.astype(dt)
            method = "EAD"
        else:
            channels = self.bayer_split(frame)
            bayer_to_index = {"RGGB": [0, 1, 2, 3],
                              "GBRG": [2, 0, 3, 1],
                              "BGGR": [3, 1, 2, 0],
                              "GRBG": [1, 0, 3, 2]}
            indices = bayer_to_index[bayer_pattern.upper()]
            r = channels[indices[0]]
            g = (channels[indices[1]] + channels[indices[2]]) / 2.0
            b = channels[indices[3]]
            frame = np.dstack((r, g, b))
            method = "downsample"
        self._vprint(f"{_elapsed(t0)} - demosaicing [{method}, {bayer_pattern}]: range = {self._minmax(frame)}")
        return frame

    def lsc(self, frame: np.ndarray, lscmap: np.ndarray) -> np.ndarray:
        """
        Multiply the given RGB/raw frame by the given lens shading correction (LSC)
        map. If the frame is in Bayer raw format, the LSC map must have the same
        size and Bayer order as the frame; otherwise, results will be unpredictable.
        In case of an RGB frame, the LSC map is automatically rescaled to match the
        frame. Also, the LSC map may be grayscale to correct vignetting only, or RGB
        to correct vignetting and/or color shading. If lscmap is None, the frame is
        returned untouched.
        """
        if lscmap is not None:
            t0 = time.time()
            imgh, imgw = frame.shape[:2]
            lsch, lscw = lscmap.shape[:2]
            need_resize = lscmap.shape[:2] != frame.shape[:2]
            if need_resize:
                dt = lscmap.dtype
                xgrid = np.linspace(0, lscw - 1, imgw)
                ygrid = np.linspace(0, lsch - 1, imgh)
                mgrid = np.dstack(np.meshgrid(xgrid, ygrid, indexing="xy"))
                lscmap = lscmap.astype(np.float32) if dt == np.float16 else lscmap
                lscmap = cv2.remap(lscmap, mgrid.astype(np.float32), None, cv2.INTER_LINEAR)
                lscmap = lscmap.astype(dt)
            if lscmap.ndim < frame.ndim:
                lscmap = np.atleast_3d(lscmap)  # {RGB, monochrome} => RGB
            frame = frame * lscmap
            with np.printoptions(formatter={'float': lambda x: f"{x:.3f}"}):
                if lscmap.ndim == 3:  # RGB
                    gains = np.amax(lscmap, axis=(0, 1))
                if lscmap.ndim == 2:  # assume Bayer raw, ignore grayscale
                    gains = np.array([np.amax(c) for c in self.bayer_split(lscmap)])
                self._vprint(f"{_elapsed(t0)} - applying LSC with max gains {gains}: range = {self._minmax(frame)}")
        return frame

    def wb(self, frame: np.ndarray, gains: Sized, bayer_pattern: str = None) -> np.ndarray:
        """
        Multiply the RGB channels of the given frame by the given white balance
        coefficients. If there are only two coefficients instead of three, they
        are applied on the R and B channels. If gains is None, the frame is
        returned untouched.
        """
        if gains is not None:
            t0 = time.time()
            wb = np.asarray(gains, dtype=frame.dtype)
            wb = np.insert(wb, 1, 1.0) if len(wb) == 2 else wb
            if frame.ndim == 3:  # RGB mode
                mode = "RGB"
                frame = frame * wb
            if frame.ndim == 2:  # Bayer mode
                assert bayer_pattern is not None, "wb() requires bayer_pattern for raw Bayer frames"
                assert bayer_pattern in ["RGGB", "BGGR", "GRBG", "GBRG"], bayer_pattern
                mode = bayer_pattern
                order = ["RGB".index(ch) for ch in bayer_pattern.upper()]
                wb = wb[order]  # BGGR => [2, 1, 1, 0]
                wb = wb.reshape(4, 1, 1)
                channels = self.bayer_split(frame)
                channels = channels * wb
                frame = self.bayer_combine(*channels)
            with np.printoptions(formatter={'float': lambda x: f"{x:.3f}"}):
                wb = wb.flatten()
                self._vprint(f"{_elapsed(t0)} - applying WB gains {mode} = {wb}: range = {self._minmax(frame)}")
        return frame

    def ccm(self, frame: np.ndarray, matrix: np.ndarray, clip=False) -> np.ndarray:
        """
        Apply the given global or per-pixel color correction matrix/-es on the
        given RGB frame. If the 'clip' flag is True, input colors are clipped to
        [0, 1] to avoid "pink sky" artifacts caused by the combination of clipped
        highlights and less-than-1.0 coefficients in the CCM. No attempt is made
        at gamut mapping or highlight recovery. If matrix is None, the frame is
        returned untouched.
        """
        if matrix is not None:
            assert matrix.ndim >= 2, f"invalid CCM dimensions: {matrix.shape}"
            assert frame.dtype in [np.float16, np.float32, np.float64], f"expected floating-point pixels, not {frame.dtype}"
            assert matrix.shape[-1] == frame.shape[-1], f"matrix {matrix.shape} and frame {frame.shape} dimensions do not match"
            if clip:
                frame = self.clip(frame, 0, 1)
            t0 = time.time()
            matrix = matrix.astype(frame.dtype)
            if matrix.ndim == 2:
                frame = np.einsum("ij,...j->...i", matrix, frame)  # (3, 3) x (H, W, 3) => (H, W, 3)
                with np.printoptions(formatter={'float': lambda x: f"{x:.2f}"}):
                    sums = f"with column sums {np.sum(matrix, axis=0).T}"
                    self._vprint(f"{_elapsed(t0)} - applying global CCM {sums}: range = {self._minmax(frame)}")
            else:
                assert matrix.shape[:-2] == frame.shape[:-1], f"matrix {matrix.shape} and frame {frame.shape} dimensions do not match"
                frame = np.einsum("...ij,...j->...i", matrix, frame)  # (H, W, 3, 3) x (H, W, 3) => (H, W, 3)
                with np.printoptions(formatter={'float': lambda x: f"{x:.2f}"}):
                    self._vprint(f"{_elapsed(t0)} - applying per-pixel CCMs: range = {self._minmax(frame)}")
        return frame

    def srgb_to_xyz(self, frame: np.ndarray):
        """
        Convert the given sRGB frame to CIE XYZ using the standard conversion matrix.
        """
        t0 = time.time()
        matrix = np.asarray([[ 0.4124,  0.3576,  0.1805],
                             [ 0.2126,  0.7152,  0.0722],
                             [ 0.0193,  0.1192,  0.9505]])
        frame = np.einsum("ij,...j->...i", matrix, frame)  # (3, 3) x (H, W, 3) => (H, W, 3)
        self._vprint(f"{_elapsed(t0)} - converting from sRGB to CIE XYZ: range = {self._minmax(frame)}")
        return frame

    def xyz_to_srgb(self, frame: np.ndarray):
        """
        Convert the given CIE XYZ frame to sRGB using the standard conversion matrix.
        """
        t0 = time.time()
        matrix = np.asarray([[ 3.2406, -1.5372, -0.4986],
                             [-0.9689,  1.8758,  0.0415],
                             [ 0.0557, -0.2040,  1.0570]])
        frame = np.einsum("ij,...j->...i", matrix, frame)  # (3, 3) x (H, W, 3) => (H, W, 3)
        self._vprint(f"{_elapsed(t0)} - converting from CIE XYZ to sRGB: range = {self._minmax(frame)}")
        return frame

    def gamut(self,
              frame: np.ndarray,
              mode: str = "ACES",
              limit=None,
              thr=0.8,
              p=5.0) -> np.ndarray:
        """
        Compress out-of-gamut (negative) RGB colors into the visible gamut using
        the ACES gamut mapping algorithm. If mode is not "ACES", the frame is
        returned untouched.

        The concepts of distance limit, gamut protection threshold (thr) and
        compression curve power (p) can be visualized with an interactive tool
        at https://www.desmos.com/calculator/54aytu7hek.

        As an example, when RGB equals [-5 1 2], the maximum color component is 2,
        the corresponding absolute distances are [7 1 0], and relative distances
        [3.5 0.5 0.0]. If the distance limit is, for example, 2.0, the R component
        will remain negative (out of gamut). However, if limit is None, the limit
        will be automatically set just high enough (>= 3.5) that all pixels are
        brought into gamut.
        """
        if mode == "ACES":
            assert p >= 1, f"compression curve power must be >= 1.0; was {p:.3f}"
            t0 = time.time()
            dt = frame.dtype
            minmax = self._minmax(frame)
            frame = frame.astype(np.float32) if dt == np.float16 else frame
            frame, limit = _aces_gamut(frame, p, thr, limit)
            frame = frame.astype(dt)
            range_str = f"range = {minmax} => {self._minmax(frame)}"
            self._vprint(f"{_elapsed(t0)} - gamut mapping [{mode}, limit={limit}, thr={thr}, p={p}]: {range_str}")
        return frame

    def tonemap(self, frame: np.ndarray, mode: str = "Reinhard", **kwargs) -> np.ndarray:
        """
        Apply the given tonemapping method on the given RGB frame. The available
        methods and their keyword arguments are as follows:

          * Reinhard: "Photographic tone reproduction for digital images" (2002)

          * KimKautz: "Consistent tone reproduction" (2008)
             - black: target display minimum luminance in cd/m2; default = 0.3
             - white: target display maximum luminance in cd/m2; default = 300
             - c1: brightness/detail tradeoff; default = 3.0
             - c2: display efficiency factor; default = 0.8

        If mode is not one of the above, the frame is returned untouched.
        """
        if mode in ["Reinhard", "KimKautz"]:
            minmax = self._minmax(frame)
            t0 = time.time()
            dt = frame.dtype
            if mode == "Reinhard":
                frame = silent.clip(frame, 0, np.inf)
                frame = frame.astype(np.float32)  # can't handle any other dtypes
                algo = cv2.createTonemapReinhard(gamma=1.0, intensity=0.0, light_adapt=0.0, color_adapt=0.0)
                cv2.setLogLevel(2)  # 2 = LOG_LEVEL_ERROR
                frame = algo.process(frame)  # causes a spurious internal warning in OpenCV 4.5
                cv2.setLogLevel(3)  # 3 = LOG_LEVEL_WARNING
            elif mode == "KimKautz":
                frame = _tmo_kim_kautz(frame, **kwargs)
            frame = frame.astype(dt)
            self._vprint(f"{_elapsed(t0)} - tonemapping [{mode}]: range = {minmax} => {self._minmax(frame)}")
        return frame

    def chroma_denoise(self,
                       frame: np.ndarray,
                       strength: int = 6,
                       winsize: int = 17) -> np.ndarray:
        """
        Apply non-local means denoising (Buades et al. 2011) on the given RGB frame.
        Input colors are clipped to [0, 1] prior to denoising. Increasing the values
        of filter strength and search window size make the denoising more aggressive
        and more time-consuming. If strength is 0, the frame is returned untouched.
        """
        if strength > 0:
            maxval, dtype = (255, np.uint8)  # OpenCV denoising can't handle 16-bit color
            frame = self.clip(frame * maxval + 0.5, 0, maxval)
            t0 = time.time()
            frame = frame.astype(dtype)
            frame = cv2.fastNlMeansDenoisingColored(frame, h=0, hColor=strength, searchWindowSize=winsize)
            frame = frame.astype(np.float32) / maxval
            self._vprint(f"{_elapsed(t0)} - chroma denoising [s={strength:.2f}, w={winsize}]: range = {self._minmax(frame)}")
        return frame

    def saturate(self,
                 frame: np.ndarray,
                 booster: Optional[Callable[[np.ndarray], np.ndarray]]) -> np.ndarray:
        """
        Apply the caller-provided boost function on the given RGB frame. The input
        frame is converted to HSL color space and the S channel given as the sole
        input to the boost function. Input RGB colors are clipped to [0, 1] before
        converting to HSL. If booster is None, the frame is returned untouched.

        Example:
          img = rawpipe.saturate(img, lambda x: x ** 0.75)
        """
        if booster is not None:
            t0 = time.time()
            dt = frame.dtype
            frame = frame.astype(np.float32) if dt == np.float16 else frame
            input_range = self._minmax(frame)
            frame = np.clip(frame, 0.0, 1.0)
            hsl = _transform_srgb_to_hsl(frame)
            hsl[..., 1] = booster(hsl[..., 1])  # saturation boost
            hsl[..., 1] = np.clip(hsl[..., 1], 0, 1)  # may be -eps or 1+eps
            frame = _transform_hsl_to_srgb(hsl)
            frame = frame.astype(dt)
            self._vprint(f"{_elapsed(t0)} - applying HSL saturation boost: range = {input_range} => {self._minmax(frame)}")
        return frame

    def gamma(self,
              frame: np.ndarray,
              mode: str = "sRGB",
              lut: np.ndarray = None) -> np.ndarray:
        """
        Apply rec709 or sRGB gamma or a custom tone curve on the given frame.
        Input colors are clipped to [0, 1] to avoid any arithmetic exceptions.
        In "LUT" mode, the frame is quantized to match the number of entries N
        in the look-up table; for example, if N=64, the output frame will have
        6-bit colors (and severe banding). This algorithm is format-agnostic.
        If mode evaluates to False, the frame is returned untouched.
        """
        assert mode in ["sRGB", "rec709", "LUT"] or not mode, f"Unrecognized mode '{repr(mode)}'"
        if mode in ["sRGB", "rec709", "LUT"]:
            t0 = time.time()
            dt = frame.dtype
            realmode = mode
            input_range = self._minmax(frame)
            frame = np.clip(frame, 0, 1)  # can't handle values outside of [0, 1]
            if realmode in ["sRGB", "rec709"]:
                bpp = 14
                maxval = 2 ** bpp - 1
                lut = np.linspace(0, 1, 2 ** bpp)
                mode = "LUT"
                if realmode == "sRGB":
                    assert lut is not None
                    srgb_lo = 12.92 * lut
                    srgb_hi = 1.055 * np.power(lut, 1.0 / 2.4) - 0.055
                    threshold_mask = (lut > 0.0031308)
                    lut = srgb_hi * threshold_mask + srgb_lo * (~threshold_mask)
                    lut = lut * maxval
                if realmode == "rec709":
                    assert lut is not None
                    srgb_lo = 4.5 * lut
                    srgb_hi = 1.099 * np.power(lut, 0.45) - 0.099
                    threshold_mask = (lut > 0.018)
                    lut = srgb_hi * threshold_mask + srgb_lo * (~threshold_mask)
                    lut = lut * maxval
            if mode == "LUT":
                assert lut is not None
                lut = lut.astype(dt)
                maxval = len(lut) - 1
                frame = silent.quantize(frame, maxval)  # [0, 1] ==> [0, maxval]
                frame = lut[frame]                     # [0, maxval] ==> [0, maxval]
                frame = frame / float(maxval)          # [0, maxval] ==> [0, 1]
            self._vprint(f"{_elapsed(t0)} - applying gamma curve [{realmode}]: range = {input_range} => {self._minmax(frame)}")
        return frame

    def degamma(self, frame: np.ndarray, mode: str = "sRGB") -> np.ndarray:
        """
        Apply standard sRGB inverse gamma on the given frame. If mode evaluates to
        False, the frame is returned untouched.
        """
        assert mode in ["sRGB"] or not mode, f"Unrecognized mode '{repr(mode)}'"
        if mode in ["sRGB"]:
            t0 = time.time()
            srgb_lo = frame / 12.92
            srgb_hi = np.power((frame + 0.055) / 1.055, 2.4)
            threshold_mask = (frame > 0.04045)
            input_range = self._minmax(frame)
            frame = srgb_hi * threshold_mask + srgb_lo * (~threshold_mask)
            self._vprint(f"{_elapsed(t0)} - applying inverse gamma curve [{mode}]: range = {input_range} => {self._minmax(frame)}")
        return frame

    def quantize(self,
                 frame: np.ndarray,
                 maxval: int,
                 dtype: Type = np.uint16) -> np.ndarray:
        """
        Clip the given frame to [0, 1], rescale it to [0, maxval], and convert
        it to the given dtype with proper rounding. This algorithm is format-
        agnostic.
        """
        t0 = time.time()
        minmax = self._minmax(frame)
        frame = np.clip(frame * maxval + 0.5, 0, maxval)
        frame = frame.astype(dtype)
        self._vprint(f"{_elapsed(t0)} - clipping to [0, 1] and quantizing to {np.dtype(dtype).name}: range = {minmax} => [0, {maxval}]")
        return frame

    def quantize8(self, frame: np.ndarray) -> np.ndarray:
        """
        Clip the given frame to [0, 1], rescale it to [0, 255], and convert it
        to np.uint8. This algorithm is format-agnostic.
        """
        frame = self.quantize(frame, maxval=255, dtype=np.uint8)
        return frame

    def quantize16(self, frame: np.ndarray) -> np.ndarray:
        """
        Clip the given frame to [0, 1], rescale it to [0, 65535], and convert it
        to np.uint16. This algorithm is format-agnostic.
        """
        frame = self.quantize(frame, maxval=65535, dtype=np.uint16)
        return frame

    def _vprint(self, message: str, **kwargs):
        if self.verbose:
            print(message, **kwargs)

    def _minmax(self, frame: np.ndarray) -> str:
        if self.verbose:
            minmax_str = f"[{np.min(frame):.2f}, {np.max(frame):.2f}]"
            return minmax_str
        return ""


######################################################################################
#
#  G L O B A L S
#
######################################################################################


verbose = Algorithms(verbose=True)
silent = Algorithms(verbose=False)
quiet = silent


######################################################################################
#
#  I N T E R N A L   F U N C T I O N S
#
######################################################################################


def _divide(nominator: np.ndarray,
            denominator: np.ndarray,
            zero_threshold: float = 0.0) -> np.ndarray:
    """
    Divide nominator by denominator, substituting zero for not-a-numbers and
    divide-by-zeros while retaining infinities. In particular, the following
    rules apply:

      x / 0 = 0
      x / inf = 0
      x / nan = 0
      inf / 0 = 0
      inf / inf = 0
      inf / nan = 0
      nan / x = 0
      inf / x = inf

    Arguments:
      - nominator: ndarray of arbitrary shape
      - denominator: ndarray that can be broadcast to nominator
      - zero_threshold: treat absolute values smaller than this as zero

    Returns:
      - result of nominator / denominator, with divide-by-zeros and other
        NaNs replaced with zeros; ndarray with the same shape as nominator
    """
    nominator = np.asarray(nominator)
    denominator = np.asarray(denominator)
    nonzero = np.abs(denominator) > zero_threshold
    finite = np.isfinite(denominator)
    valid = nonzero * finite  # logical AND
    zeros = np.zeros_like(nominator)
    if not np.issubdtype(zeros.dtype, np.floating):
        zeros = zeros.astype(np.float64)
    result = np.divide(nominator, denominator, out=zeros, where=valid)
    result = np.nan_to_num(result, posinf=np.inf, neginf=-np.inf)
    return result


def _transform_srgb_to_hsl(frame: np.ndarray) -> np.ndarray:
    rgb = frame
    cmax = np.max(rgb, axis=-1)  # (H, W, 3) => (H, W)
    cmin = np.min(rgb, axis=-1)  # (H, W, 3) => (H, W)
    delta = cmax - cmin  # (H, W)
    r, g, b = np.moveaxis(rgb, -1, 0)  # (H, W, 3) => (3, H, W)
    z_mask = delta == 0.0  #  (H, W; bool)
    r_mask = (r == cmax) & ~z_mask
    g_mask = (g == cmax) & ~z_mask
    b_mask = (b == cmax) & ~z_mask
    hue = np.zeros_like(delta)  # (H, W)
    sat = np.zeros_like(delta)
    div = lambda a, b, mask: a[mask] / b[mask]
    hue[r_mask] = (60.0 * div(g - b, delta, r_mask) + 360) % 360
    hue[g_mask] = 60.0 * div(b - r, delta, g_mask) + 120
    hue[b_mask] = 60.0 * div(r - g, delta, b_mask) + 240
    lum = 0.5 * (cmax + cmin)  # (H, W)
    sat = 1 - np.abs(2 * lum - 1)  # can be 0.0 even if lum > 0.0
    z_mask = (delta == 0.0) | (sat == 0.0)
    sat[~z_mask] = div(delta, sat, ~z_mask)  # leave zeros as zeros
    hsl = np.dstack((hue, sat, lum))  # (H, W, 3)
    return hsl


def _transform_hsl_to_srgb(frame: np.ndarray) -> np.ndarray:
    hue, sat, lum = np.moveaxis(frame, -1, 0)  # (H, W, 3) => (3, H, W)
    c = (1 - np.abs(2 * lum - 1)) * sat  # (H, W)
    x = c * (1 - np.abs((hue / 60) % 2 - 1))
    m = lum - c / 2
    zeros = np.zeros_like(c)
    gte60 = hue >= 60
    gte120 = hue >= 120
    gte180 = hue >= 180
    gte240 = hue >= 240
    gte300 = hue >= 300
    hue0 = ~gte60  # [0, 60)
    hue60 = gte60 & ~gte120  # [60, 120)
    hue120 = gte120 & ~gte180  # [120, 180)
    hue180 = gte180 & ~gte240  # [180, 240)
    hue240 = gte240 & ~gte300  # [240, 300)
    hue300 = gte300  # [300, 360)
    dstack = lambda a, b, c, mask: np.dstack((a[mask], b[mask], c[mask]))
    rgb = np.empty_like(frame)
    rgb[hue0] = dstack(c, x, zeros, hue0)
    rgb[hue60] = dstack(x, c, zeros, hue60)
    rgb[hue120] = dstack(zeros, c, x, hue120)
    rgb[hue180] = dstack(zeros, x, c, hue180)
    rgb[hue240] = dstack(x, zeros, c, hue240)
    rgb[hue300] = dstack(c, zeros, x, hue300)
    rgb = rgb + m[..., np.newaxis]
    return rgb


def _aces_gamut(rgb: np.ndarray, power: float, threshold, limit) -> np.ndarray:

    # threshold is the percentage of core gamut to protect; must be < 1.0

    thr = np.clip(threshold, 0.0, 0.9999)
    thr = np.tile(thr, 3 if np.isscalar(thr) else 1)
    thr = thr.reshape([1] * (rgb.ndim - 1) + [3])  # (1, 3) or (1, 1, 3)

    # distance is relative to per-pixel maximum color; >1.0 means out of gamut

    max_rgb = np.max(rgb, axis=-1, keepdims=True)  # (H, W, 1)
    dist = _divide(max_rgb - rgb, np.abs(max_rgb))  # (H, W, 3); >= 0.0

    # limit is the maximum distance that will be squeezed into the gamut;
    # colors further than that will remain out of gamut, but less than before

    if limit is None:
        # auto-compute RGB-wise distance limits, ignoring below-mean pixels
        bright = max_rgb[..., 0] > np.mean(max_rgb)  # (H, W) mask
        limit = np.max(dist[bright], axis=0)  # global per-channel maximum
        limit = np.clip(limit, 1.01, np.inf)  # limit must be >= 1.01

    def compress(dist, power, thr, lim):
        """
        compression function plot: https://www.desmos.com/calculator/54aytu7hek

        assumptions:
          dist in [0, ~2]
          power in [1, ~20]
          thr in [0, 1)
          lim in [1, ~2]
        """

        # precalculate per-frame constants

        invp = 1 / power  # [~0.05, 1]
        src_domain = lim - thr  # range on the x axis to compress from; always > 0
        dst_domain = 1.0 - thr  # range on the x axis to compress to; <= src_domain
        rel_domain = src_domain / dst_domain  # always >= 1, typically 1..10
        pow_domain = rel_domain ** power  # always >= 1, can be very large if p >> 1
        pow_domain = (pow_domain - 1) ** invp  # ~rel_domain, if p >> 1 or lim >> 1
        s = src_domain / pow_domain  # > dst_domain; ~dst_domain, if p >> 1 or lim >> 1

        # apply per-pixel operations; example:
        #
        #   p=4, thr=0.8, lim=1.2 ==> s ≃ 0.2033:
        #      src_domain = 1.2 - 0.8 = 0.4
        #      dst_domain = 1.0 - 0.8 = 0.2
        #      rel_domain = 0.4 / 0.2 = 2.0
        #      pow_domain = (2.0 ** 4 - 1) ^ 0.25 = 15 ^ 0.25 ≃ 1.968
        #      s = 0.4 / 15 ^ 0.25 ≃ 0.2033
        #
        #   s=0.2033:
        #
        #      dist = 1.2 ==> 0.99699
        #      dist = 1.0 ==> denom = 1.0 => 2 ^ 0.25 => cdist = 0.8 + 0.2 / 2 ^ 0.25 = 0.9682

        denom = (dist - thr) / s  # example: denom = (1.2 - 0.8) / 0.2 = 0.4 / 0.2 = 2.0
        denom = np.clip(denom, 0, np.inf)  # (dist - thr) < 0 for most pixels
        denom = (1 + denom ** power) ** invp  # example: denom = (1 + 2 ** 4) ** 0.25 = (1 + 16) ** 0.25 = 17 ** 0.25 = 2.0305
        cdist = thr + (dist - thr) / denom  # example: cdist = 0.8 + (1.2 - 0.8) / 2.0305 = 0.8 + 0.4 / 2.0305 = 0.8 + 0.19699 = 0.99699
        return cdist

    # Compress channel-wise distances to max{RGB}; note that max{RGB} remains
    # unchanged. For example, RGB = (-0.1, 0.02, 2.5) might get compressed to
    # (0.0, 0.05, 2.5).

    cdist = compress(dist, power, thr, limit)
    crgb = max_rgb - cdist * max_rgb
    return crgb, limit


def _tmo_kim_kautz(rgb: np.ndarray, black: float = 0.3, white: float = 300, c1: float = 3.0, c2: float = 0.8) -> np.ndarray:
    """
    Applies the "Consistent tone reproduction" tonemapping method by Kim & Kautz (2008)
    on the given linear sRGB frame.

    Arguments:
      - rgb: HDR image to tonemap; range = [0, >1], shape (..., 3)
      - black: target display minimum luminance in cd/m2
      - white: target display maximum luminance in cd/m2
      - c1: brightness/detail tradeoff, recommended value 3.0
      - c2: display efficiency factor = log10(255) / log10(white / black);
            <1.0 for typical LDR displays, >1.0 for displays that can
            reproduce more than 256 distinguishable levels of brightness

    Returns:
      - tonemapped image in linear sRGB; not normalized or clipped
    """
    xyz = silent.srgb_to_xyz(rgb)
    xyz = silent.clip(xyz, 0, np.inf)
    lum_in = xyz[..., 1].copy()
    lum_log = np.log10(lum_in + 1e-6)
    mu = np.mean(lum_log)

    # Compute the ratio between display & scene dynamic ranges (k1).
    # The dynamic range of the display is typically lower than that
    # of the scene, so usually k1 < 1.

    display_dr = np.log10(white / black)
    scene_dr = np.max(lum_log) - np.min(lum_log)
    k1 = display_dr / scene_dr

    # Compute linear tonemapped luminance

    sigma = scene_dr / c1
    w = 10 ** (-0.5 * ((lum_log - mu) ** 2) / sigma ** 2)
    k2 = (1 - k1) * w + k1
    lum_out = 10 ** (c2 * k2 * (lum_log - mu) + mu)

    # Multiply XYZ values by the luminance ratio and convert to sRGB. If the
    # input luminance is near-zero (less than 1e-6), the output color becomes
    # zero, as well. This is to avoid near-infinity luminance ratios blowing
    # up the output dynamic range and defeating the purpose of tone mapping.

    lum_ratio = _divide(lum_out, lum_in, 1e-6)
    xyz[..., 0] *= lum_ratio
    xyz[..., 1] *= lum_ratio
    xyz[..., 2] *= lum_ratio
    rgb_out = silent.xyz_to_srgb(xyz)

    # Return as linear sRGB with out-of-gamut colors retained

    return rgb_out


def _elapsed(t0: float) -> str:
    elapsed = (time.time() - t0) * 1000
    elapsed_str = f"{elapsed:8.2f} ms"
    return elapsed_str
