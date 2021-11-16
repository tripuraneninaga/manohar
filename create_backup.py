from app.api.utils import *
from app.aws.s3_client import upload_to_s3
from app.setup_structlog import get_logger

BACKUP_DIR = {
    'dashboards': 'backup/dashboards/',
    'data_models': 'backup/data_models/'
}

_logger = get_logger(__name__)


def create_dashboards_backup():
    try:
        dashboards = get_all_dashboards()
        dir_name = BACKUP_DIR['dashboards'] + 'backup_' + datetime.now().strftime('%Y-%b-%dT%H%M%SZ') + '/'
        _logger.info('Uploading dashboard file to s3')
        for dashboard in dashboards:
            title = dashboard.get('title')
            file_name = f'{title}_' if title else '_'
            file_name = file_name + dashboard.get('_id', '') + '.dash'
            if not upload_to_s3(content=dashboard, dir_name=dir_name, file_name=file_name):
                _logger.info('Failed to upload dashboard to s3.', id=dashboard.get('_id'), title=dashboard.get('title'))
        _logger.info('Finished Creating dashboards backup')
    except DashboardsGetException:
        _logger.error('Could not create backup. Error getting dashboards.')


def create_data_models_backup():
    try:
        data_model_ids = get_all_data_model_ids()
        dir_name = BACKUP_DIR['data_models'] + 'backup_' + datetime.now().strftime('%Y-%b-%dT%H%M%SZ') + '/'
        _logger.info('Uploading data model files to s3')
        for entry in data_model_ids:
            oid = entry.get('oid')
            data_model = get_data_model(oid)
            if data_model is None:
                continue
            title = data_model.get('title', '')
            file_name = f'{title}_{oid}.smodel'
            if not upload_to_s3(content=data_model, dir_name=dir_name, file_name=file_name):
                _logger.info('Failed to upload data model to s3.', id=oid, title=data_model.get('title'))
        _logger.info('Finished creating Data Models backup.')
    except DataModelsGetException:
        _logger.error('Could not create backup. Error getting Data Models.')
