import os
import matplotlib.pyplot as plt

data_dir = r"C:\WSI\specdracula\testdata"
files = sorted(f for f in os.listdir(data_dir) if f.endswith(".origin"))

fig, ax = plt.subplots(figsize=(9, 5))

for fname in files:
    label = fname.split("_")[2]  # e.g. "1.45eV"
    path = os.path.join(data_dir, fname)

    wavelengths = []
    spectra = []

    with open(path, encoding="latin-1") as fh:
        for line in fh:
            parts = line.rstrip("\r\n").split("\t")
            try:
                wl = float(parts[0])
            except (ValueError, IndexError):
                continue
            # parse all numeric columns after the wavelength
            counts = []
            for p in parts[1:]:
                try:
                    counts.append(float(p))
                except ValueError:
                    break
            if counts:
                wavelengths.append(wl)
                spectra.append(counts)

    # spectra[i] = list of counts for row i across all power steps
    # rightmost spectrum = last index across all rows
    rightmost = [row[-1] for row in spectra]
    ax.plot(wavelengths, rightmost, label=label)

ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Counts")
ax.set_title("PL spectra — highest-power spectrum per file")
ax.legend()
fig.tight_layout()
fig.savefig(r"C:\WSI\specdracula\plot.png", dpi=150)
print("Saved plot.png")
