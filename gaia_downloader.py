from astroquery.gaia import Gaia
from pathlib import Path
import argparse
import re

def build_query(limit: int) -> str:
    query = f"""

    SELECT TOP {limit}
        source_id,

        teff_gspphot AS surface_temperature_K,
        teff_gspphot_lower AS surface_temperature_K_lower,
        teff_gspphot_upper AS surface_temperature_K_upper,

        lum_flame AS luminosity_Lsun,
        lum_flame_lower AS luminosity_Lsun_lower,
        lum_flame_upper AS luminosity_Lsun_upper,

    FROM gaiadr3.astrophysical_parameters

    WHERE
        teff_gspphot IS NOT NULL 
        AND lum_flame IS NOT NULL
        AND teff_gspphot >0
        AND lum_flame > 0
        AND classprob_dsc_combmod_star >= 0.5
    """
    return query

def download_data(output_file: str, limit: int):
    query = build_query(limit)
    
    print(f"Output file: {output_file}")

    Gaia.ROW_LIMIT = -1

    job = Gaia.launch_job_async(
        query=query,
        output_file=output_file,
        output_format='csv',
        dump_to_file=True,
    )

    print(f"Download completed. Data saved to {Path(output_file).resolve()}")

def main():
    parser = argparse.ArgumentParser(
        description="Download stellar data from Gaia DR3 with specific parameters."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=1_000_000_000,
        help="Maximum number of rows to download."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="gaia_stellar_data.csv",
        help="Output CSV filename.",
    )

    args = parser.parse_args()

    download_data(
        output_file=args.output,
        limit=args.limit,
    )

if __name__ == "__main__":
    main()
