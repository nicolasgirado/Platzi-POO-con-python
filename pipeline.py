import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
news_sites_uids = ['lanacion']


def main():
    _extract()
    _transform()
    _load()


def _extract():
    logger.info('\n\n\nStarting extract process...\n')
    for news_sites_uid in news_sites_uids:
        subprocess.run(['python', 'main.py', news_sites_uid], cwd='./extract')
        subprocess.run(['find', '.', '-name', f'{news_sites_uid}*',
                       '-exec', 'mv', '{}', f'../transform/{news_sites_uid}_.csv', ';'],
                       cwd='./extract')


def _transform():
    logger.info('\n\n\nStarting transform process...\n')
    for news_sites_uid in news_sites_uids:
        dirty_data_filename = f'{news_sites_uid}_.csv'
        clean_data_filename = f'clean_{dirty_data_filename}'
        subprocess.run(['python', 'main.py', dirty_data_filename],
                       cwd='./transform')
        # subprocess.run(['rm', dirty_data_filename],
        #                cwd='./transform')
        subprocess.run(['mv', clean_data_filename, f'../load/{news_sites_uid}.csv'],
                       cwd='./transform')


def _load():
    logger.info('\n\n\nStarting load process...\n')
    for news_sites_uid in news_sites_uids:
        clean_data_filename = f'{news_sites_uid}.csv'
        subprocess.run(['python', 'main.py', clean_data_filename],
                       cwd='./load')


if __name__ == "__main__":
    main()
