# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

import uuid

from elasticsearch import Elasticsearch
from pyhocon import ConfigFactory

from databuilder.extractor.atlas_search_data_extractor import AtlasSearchDataExtractor
from databuilder.job.job import DefaultJob
from databuilder.loader.file_system_elasticsearch_json_loader import FSElasticsearchJSONLoader
from databuilder.publisher.elasticsearch_publisher import ElasticsearchPublisher
from databuilder.task.task import DefaultTask
from databuilder.transformer.base_transformer import NoopTransformer

entity_type = 'Table'
extracted_search_data_path = '/tmp/search_data.json'
process_pool_size = 5

# atlas config
atlas_url = 'localhost'
atlas_port = 21000
atlas_protocol = 'http'
atlas_verify_ssl = False
atlas_username = 'admin'
atlas_password = 'admin'
atlas_search_chunk_size = 200
atlas_details_chunk_size = 10

# elastic config
es = Elasticsearch([
    {'host': 'localhost'},
])

elasticsearch_client = es
elasticsearch_new_index_key = f'tables-{str(uuid.uuid4())}'
elasticsearch_new_index_key_type = 'table'
elasticsearch_index_alias = 'table_search_index'

job_config = ConfigFactory.from_dict(
    {
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ATLAS_URL_CONFIG_KEY}': atlas_url,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ATLAS_PORT_CONFIG_KEY}': atlas_port,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ATLAS_PROTOCOL_CONFIG_KEY}': atlas_protocol,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ATLAS_VALIDATE_SSL_CONFIG_KEY}': atlas_verify_ssl,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ATLAS_USERNAME_CONFIG_KEY}': atlas_username,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ATLAS_PASSWORD_CONFIG_KEY}': atlas_password,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ATLAS_SEARCH_CHUNK_SIZE_KEY}': atlas_search_chunk_size,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ATLAS_DETAILS_CHUNK_SIZE_KEY}': atlas_details_chunk_size,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.PROCESS_POOL_SIZE_KEY}': process_pool_size,
        f'extractor.atlas_search_data.{AtlasSearchDataExtractor.ENTITY_TYPE_KEY}': entity_type,
        f'loader.filesystem.elasticsearch.{FSElasticsearchJSONLoader.FILE_PATH_CONFIG_KEY}': extracted_search_data_path,
        f'loader.filesystem.elasticsearch.{FSElasticsearchJSONLoader.FILE_MODE_CONFIG_KEY}': 'w',
        f'publisher.elasticsearch.{ElasticsearchPublisher.FILE_PATH_CONFIG_KEY}': extracted_search_data_path,
        f'publisher.elasticsearch.{ElasticsearchPublisher.FILE_MODE_CONFIG_KEY}': 'r',
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_CLIENT_CONFIG_KEY}': elasticsearch_client,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_NEW_INDEX_CONFIG_KEY}': elasticsearch_new_index_key,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_DOC_TYPE_CONFIG_KEY}': elasticsearch_new_index_key_type,
        f'publisher.elasticsearch.{ElasticsearchPublisher.ELASTICSEARCH_ALIAS_CONFIG_KEY}': elasticsearch_index_alias,
    }
)

if __name__ == "__main__":
    task = DefaultTask(extractor=AtlasSearchDataExtractor(),
                       transformer=NoopTransformer(),
                       loader=FSElasticsearchJSONLoader())

    job = DefaultJob(conf=job_config,
                     task=task,
                     publisher=ElasticsearchPublisher())

    job.launch()
