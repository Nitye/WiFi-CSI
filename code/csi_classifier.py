import os
import re
import argparse
import numpy as np
import matplotlib.pyplot as plt
import csiread
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", type=str, required=True, help="Path to folder containing .dat files")
args = parser.parse_args()

PATTERN = re.compile(r"user\d+-(\d+)-(\d+)-(\d+)-(\d+)-r(\d+)\.dat")
def parse_label(filename):
    m = PATTERN.match(os.path.basename(filename))
    if not m:
        return None
    room, loc, gesture, torso, rep = m.groups()
    return int(loc)

def extract_features(filepath):
    """
    Returns a 1D feature vector from one .dat file.

    Features:
      - Mean amplitude per subcarrier, per antenna pair  (30 x 3 = 90 values)
      - Std  amplitude per subcarrier, per antenna pair  (90 values)
      - Mean phase diff between antenna pairs 0-1 and 0-2 (30 x 2 = 60 values)
    Total: 240-dim vector
    """
    try:
        csi = csiread.Intel(filepath, nrxnum=3, ntxnum=1, pl_size=0)
        csi.read()
    except Exception as e:
        return None

    data = csi.csi  # shape: (N_packets, 1, 3, 30)  — complex
    if data is None or data.shape[0] < 10:
        return None

    amp   = np.abs(data[:, 0, :, :])    # (N, 3, 30)  amplitudes
    phase = np.angle(data[:, 0, :, :])  # (N, 3, 30)  phases

    mean_amp = amp.mean(axis=0)   # (3, 30)
    std_amp  = amp.std(axis=0)    # (3, 30)

    pdiff_01 = (phase[:, 0, :] - phase[:, 1, :]).mean(axis=0)  # (30,)
    pdiff_02 = (phase[:, 0, :] - phase[:, 2, :]).mean(axis=0)  # (30,)

    feature = np.concatenate([
        mean_amp.flatten(),   # 90
        std_amp.flatten(),    # 90
        pdiff_01,             # 30
        pdiff_02,             # 30
    ])                        # = 240

    return feature

print(f"Scanning {args.data_dir} ...")
all_files = [f for f in os.listdir(args.data_dir) if f.endswith(".dat")]
print(f"Found {len(all_files)} .dat files")

X, y = [], []
skipped = 0

for fname in all_files:
    label = parse_label(fname)
    if label is None:
        skipped += 1
        continue

    fpath = os.path.join(args.data_dir, fname)
    feat  = extract_features(fpath)
    if feat is None:
        skipped += 1
        continue

    X.append(feat)
    y.append(label)

print(f"Loaded {len(X)} samples | skipped {skipped}")
print(f"Unique locations: {sorted(set(y))}")

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\n{'='*50}")
print(f"Accuracy: {acc*100:.1f}%")
print(f"{'='*50}")
print(classification_report(y_test, y_pred, target_names=[f"loc_{l}" for l in sorted(set(y))]))