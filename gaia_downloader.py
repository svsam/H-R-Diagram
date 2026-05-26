#python3 gaia_downloader.py --limit 1000 --output gaia_stellar_data.csv

import os
import csv
import time
import certifi
from pathlib import Path
from astroquery.gaia import Gaia


os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


def build_query(chunk_size, last_source_id):
    query = f"""
    SELECT TOP {chunk_size}
        source_id,
        teff_gspphot AS surface_temperature_K,
        lum_flame AS luminosity_L_sun
    FROM gaiadr3.astrophysical_parameters
    WHERE
        source_id > {last_source_id}
        AND teff_gspphot IS NOT NULL
        AND lum_flame IS NOT NULL
        AND teff_gspphot > 0
        AND lum_flame > 0
        AND classprob_dsc_combmod_star >= 0.5
    ORDER BY source_id ASC
    """

    return query


def append_rows_to_csv(results, output_file, write_header):
    fieldnames = [
        "source_id",
        "surface_temperature_K",
        "luminosity_L_sun",
    ]

    with open(output_file, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        for row in results:
            writer.writerow(
                {
                    "source_id": int(row["source_id"]),
                    "surface_temperature_K": float(row["surface_temperature_K"]),
                    "luminosity_L_sun": float(row["luminosity_L_sun"]),
                }
            )


def download_gaia_hr_data(
    output_file="gaia_hr_data_1million.csv",
    total_rows=1_000_000,
    chunk_size=50_000,
    pause_seconds=2,
):
    Gaia.ROW_LIMIT = -1

    output_path = Path(output_file)

    if output_path.exists():
        output_path.unlink()

    rows_downloaded = 0
    last_source_id = 0
    write_header = True

    while rows_downloaded < total_rows:
        remaining = total_rows - rows_downloaded
        current_chunk_size = min(chunk_size, remaining)

        print(
            f"Downloading chunk: {rows_downloaded:,} / {total_rows:,} rows complete"
        )

        query = build_query(
            chunk_size=current_chunk_size,
            last_source_id=last_source_id,
        )

        try:
            job = Gaia.launch_job_async(
                query=query,
                dump_to_file=False,
            )

            results = job.get_results()

        except Exception as error:
            print("\nA Gaia Archive query failed.")
            print("Try lowering chunk_size, for example to 10000 or 5000.")
            print(f"\nError was:\n{error}")
            raise

        if len(results) == 0:
            print("No more matching Gaia rows found.")
            break

        append_rows_to_csv(
            results=results,
            output_file=output_file,
            write_header=write_header,
        )

        write_header = False
        rows_downloaded += len(results)
        last_source_id = int(results[-1]["source_id"])
        print()

        time.sleep(pause_seconds)

    print("Finished!")
    print(f"Saved file: {output_path.resolve()}")

if __name__ == "__main__":
    download_gaia_hr_data(
        output_file="gaia_hr_data_1million.csv",
        total_rows=1_000_000,
        chunk_size=50_000,
        pause_seconds=2,
    )