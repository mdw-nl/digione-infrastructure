#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts


def send_dicoms(folder: str, host: str = "localhost", port: int = 104, aet: str = "STORESCU", aec: str = "ANY-SCP"):
    folder_path = Path(folder)
    if not folder_path.is_dir():
        print(f"Error: '{folder}' is not a valid directory")
        sys.exit(1)

    dcm_files = [f for f in folder_path.rglob("*") if f.is_file()]

    if not dcm_files:
        print(f"No files found in '{folder}'")
        sys.exit(1)

    print(f"Sending {len(dcm_files)} file(s) from '{folder}' to {host}:{port} (AET: {aet}, AEC: {aec})")

    ae = AE(ae_title=aet)
    ae.requested_contexts = StoragePresentationContexts

    assoc = ae.associate(host, port, ae_title=aec)
    if not assoc.is_established:
        print("Failed to establish association")
        sys.exit(1)

    failed = 0
    for dcm_file in dcm_files:
        try:
            ds = dcmread(str(dcm_file))
        except Exception as e:
            print(f"Skipping '{dcm_file.name}': {e}")
            failed += 1
            continue

        status = assoc.send_c_store(ds)
        if status and status.Status == 0x0000:
            print(f"Sent: {dcm_file.name}")
        else:
            print(f"Failed: {dcm_file.name} (status: {status})")
            failed += 1

    assoc.release()

    if failed:
        print(f"Done with {failed} failure(s)")
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send DICOM files to a DICOM server using pynetdicom")
    parser.add_argument("folder", help="Folder containing DICOM files")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=104)
    parser.add_argument("--aet", default="STORESCU", help="Calling AE title")
    parser.add_argument("--aec", default="ANY-SCP", help="Called AE title")
    args = parser.parse_args()

    send_dicoms(args.folder, args.host, args.port, args.aet, args.aec)
