import io
import os
import urllib
import requests
import json
import shutil
import tempfile
import zipfile
import importlib

def exec_post_install(version):

    print(f'Downloading SimCenter damage and loss database.')
    print(f'This will only need to be done once.')

    # pelicun version -> db_dl version
    db_dl_version_map = {
        '3.2b4': 'v1.0.0'
    }

    db_dl_version = db_dl_version_map[version]
    release_url = 'https://api.github.com/repos/NHERI-SimCenter/DB_DamageAndLoss/releases'
    response = requests.get(release_url)
    if response.status_code != 200:
        raise urllib.error.HTTPError(
            code=response.status_code, url=release_url,
            msg=response.reason, hdrs=None, fp=None)
    release_data = json.loads(response.text)
    tags = [x['tag_name'] for x in release_data]
    found = False
    for i, tag in enumerate(tags):
        if tag == db_dl_version:
            found = True
            target_release_data = release_data[i]
            break
    if found is False:
        raise ValueError(
            f'Target release tag {db_dl_version} not found in {release_url}.')

    zipball_url = target_release_data['zipball_url']


    def download_and_extract(zipball_url, target_filenames, output_dir):

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Download the zipball to the temporary directory
        zipball_path = os.path.join(temp_dir, 'temp.zip')
        response = requests.get(zipball_url, stream=True)
        with open(zipball_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        # Extract the zipball
        with zipfile.ZipFile(zipball_path, 'r') as zip_ref:

            # Iterate over all files in the zipball
            for file_info in zip_ref.infolist():
                filename = file_info.filename

                # Compare the filename with the target filename
                basename = os.path.basename(filename)

                if basename == '':
                    continue

                for target_filename in target_filenames:
                    if basename == target_filename:
                        # Extract the file to the temporary directory
                        extracted_file_path = zip_ref.extract(filename, temp_dir)

                        # Determine the output file path
                        output_file_path = os.path.join(output_dir, target_filename)

                        # Create necessary directories
                        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                        # Copy the extracted file to the output directory
                        shutil.copy2(extracted_file_path, output_file_path)

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

    target_filenames = [
        'damage_DB_FEMA_P58_2nd.csv',
        'damage_DB_FEMA_P58_2nd.json',
        'damage_DB_Hazus_EQ_bldg.csv',
        'damage_DB_Hazus_EQ_bldg.json',
        'damage_DB_Hazus_EQ_trnsp.csv',
        'damage_DB_Hazus_EQ_trnsp.json',
        'loss_repair_DB_FEMA_P58_2nd.csv',
        'loss_repair_DB_FEMA_P58_2nd.json',
        'loss_repair_DB_Hazus_EQ_bldg.csv',
        'loss_repair_DB_Hazus_EQ_bldg.json',
        'loss_repair_DB_Hazus_EQ_trnsp.csv',
        'loss_repair_DB_Hazus_EQ_trnsp.json',
        ]

    package_dir = os.path.dirname(importlib.util.find_spec('pelicun').origin)
    output_dir = os.path.join(package_dir, 'resources', 'SimCenterDBDL', 'DB')
    download_and_extract(zipball_url, target_filenames, output_dir)
    from pathlib import Path
    Path(os.path.join(package_dir, 'DBDL_received')).touch()

    print(f'SimCenter damage and loss database downloaded successfully.')
