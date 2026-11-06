# MEngSc bioluminescence toolkit

Code I wrote by hand between 2022 and 2023 for my MEngSc in Biomedical Engineering at Stellenbosch University. The thesis built a computer vision pipeline that measures how much a sample inhibits the bioluminescence of *Aliivibrio fischeri*, as a field toxicity test for soil and water.

Thesis: [Stellenbosch University repository](https://scholar.sun.ac.za/handle/10019.1/129109)

This is research code kept as it was written. It is not packaged, and many scripts contain hard-coded local paths.

## Contents

| Folder | What it is |
| --- | --- |
| `firmware/` | Arduino sketches for comparing light sensors: TSL2591, AS7341 spectral sensor, BH1750 and a light-dependent resistor. Includes lux conversion against known values and an OLED FeatherWing readout. |
| `sensor-data/` | Python scripts that read sensor output over serial and process the light readings. |
| `pi-camera/` | Raspberry Pi camera capture interface for imaging plates. |
| `cv-pipeline/` | OpenCV and scikit-image work on plate images: the main bioluminescence pipeline, SSIM and MSE comparison across image batches, colour histograms, region-of-interest detection in video and segmentation. |
| `cv-pipeline/figures/` | Example outputs, such as SSIM difference curves for the ATZ and Zn treatments. |

## Experimental design (from the pipeline notes)

Each experiment used 8 plates: 2 controls and 6 treated at 1x, 2x, 5x, 10x, 25x and 50x. Each group had about 300 time-stamped images. The pipeline compares treated plates with controls over time to estimate a detection limit.

## Dependencies

- Arduino libraries: SparkFun AS7341X, BH1750, Waveshare TSL2591, Adafruit GFX and SSD1306. They are not included here.
- Python: OpenCV, NumPy, SciPy, scikit-image and Matplotlib.
