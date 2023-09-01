import os
import argparse
from datetime import datetime

from .data_manager import S3DataManager

def my_path(file):
    return os.path.dirname(os.path.realpath(file))

def file_path(base, fn):
    return os.path.join(base, fn)

def extension_match(filename, extensions):
    for ext in extensions:
        if f'.{ext}' in filename:
            return True
    return False

def generate_relative_download_path(directory):
    date_string = datetime.now().date().strftime("%Y-%m-%d")
    folder_name = f'/{directory}_{date_string}/'

    path = os.path.join(os.path.expanduser('~') + folder_name)
    base_path = os.path.dirname(path)
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
    
    return base_path

def create_download_folder(path):
    path = path.strip()
    if '/' not in path:
        return generate_relative_download_path(path)
    
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except Exception:
            print(f'Invalid path {path}')
            return ""
    return path

def main():
    parser = argparse.ArgumentParser(description='s3fetch')
    parser.add_argument('-p', '--s3_path', type=str, required=True, help='S3 path')
    parser.add_argument('-d', '--download_path', type=str, default='download', help='Download path')
    parser.add_argument('-e', '--extensions', type=str, default='json', help="Specify the file extensions to download (use '|' as separator) (default: 'json')")
    args = parser.parse_args()

    s3_conn = S3DataManager(
        os.getenv('AWS_ACCESS_KEY_ID', default=None),
        os.getenv('AWS_SECRET_ACCESS_KEY', default=None),
        os.getenv('AWS_S3_REGION', default=None),
        os.getenv('S3_BUCKET_NAME', default=None),
    )
    
    extensions = [ext.strip() for ext in args.extensions.split('|')]
    download_path = create_download_folder(args.download_path)

    filenames = s3_conn.list_objects_recursive(prefix=args.s3_path)
    count = 1
    num_files = len(filenames)
    for fn in filenames:
        if not extension_match(fn, extensions):
            print(f"skipping {fn}")
            count += 1
            continue

        print(f"processing {count}/{num_files} -- {fn}")
        new_path = create_download_folder(os.path.dirname(file_path(download_path, fn)))
        s3_conn.download_file(fn, os.path.join(new_path, os.path.basename(fn)))
        count += 1


if __name__ == '__main__':
    main()