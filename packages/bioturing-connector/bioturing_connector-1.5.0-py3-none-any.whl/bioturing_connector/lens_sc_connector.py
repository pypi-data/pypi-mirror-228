"""Python package for submitting/getting data from Lens SC"""

import os
import pandas as pd
import numpy as np

from typing import List
from typing import Union
from pathlib import Path
from urllib.parse import urljoin

from .common import get_uuid
from .common import decode_base64_array

from .common import common
from .typing import Species
from .typing import StudyType
from .typing import TechnologyType
from .typing import UNIT_RAW
from .typing import INPUT_LENS_SC
from .common.https_agent import HttpsAgent


class LensSCConnector:
  """
  	Create a connector object to submit/get data from BioTuring Lens Single-cell
  	(Xenium/Cosmx/Vizgen/Proteomics)
  """

  def __init__(self, host: str, token: str, ssl: bool = True):
    """
      Args:
        host:
          The URL of the BioTuring Lens server, only supports HTTPS connection
          Example: https://lens_sc.bioturing.com
        token:
          The API token to verify authority. Generated in-app.
    """
    self.__host = host
    self.__token = token
    self.__https_agent = HttpsAgent(self.__token, ssl)


  def _check_vizgen_version_2(self, study_type, all_input_files):
    if study_type != StudyType.VIZGEN.value:
      return study_type
    for i in all_input_files:
      if i.lower().endswith('.parquet'):
        return StudyType.VIZGEN_V2.value
    return StudyType.VIZGEN.value


  def _check_valid_input_lens_sc(
      self,
      server_files_path,
      server_folders_path,
      study_type,
    ):
    input_files = INPUT_LENS_SC[study_type]['files'].values()
    input_folders = INPUT_LENS_SC[study_type]['folders'].values()
    file_paths = []
    folder_paths = []
    for f in input_files:
      try:
        file_path = [x for x in server_files_path if x.lower().endswith(f)][0]
        file_paths.append(file_path.split('/')[-1])
      except Exception as e:
        raise ValueError('Cannot find ***{} in selected folder. Error: {}'.format(f, e))
    for f in input_folders:
      try:
        folder_path = [x for x in server_folders_path if x.lower().endswith(f)][0]
        folder_paths.append(folder_path.split('/')[-1])
      except Exception as e:
        raise ValueError('Cannot find {} in selected folder. Error: {}'.format(f, e))
    return file_paths, folder_paths


  def _get_required_files_fols_lens_sc(self, server_dir_path, study_type):
    all_files_fols = [
      os.path.join(server_dir_path, x)
      for x in os.listdir(server_dir_path)
    ]
    all_files = [
      x for x in all_files_fols if os.path.isfile(x)
    ]
    all_folders = [
      x for x in all_files_fols if os.path.isdir(x)
    ]
    study_type = self._check_vizgen_version_2(study_type, all_files_fols)
    return self._check_valid_input_lens_sc(all_files, all_folders, study_type)


  def _upload_fol_lens_sc(self, group_id, batch_info, study_type):
    final_file_names = []
    final_files = []
    try:
      for batch in batch_info:
        files_path, fols_path = self._get_required_files_fols_lens_sc(
          batch['folder'],
          study_type
        )
        zip_path = os.path.join(
          batch['folder'], '{}.zip'.format(batch['name'])
        )

        print ('Zipping neccesary files of batch [{}]. \nLocation: {}'.format(batch['name'], zip_path))
        final_file_names.append('{}.zip'.format(batch['name']))
        final_files.append(zip_path)
        os.system('cd {} && zip -r {} {} && cd -'.format(
          batch['folder'],
          zip_path,
          ' '.join(files_path + fols_path)
        ))

      print ('Uploading all files to server...')
      output_dir = common.upload_local(
        final_file_names,
        [Path(zip_path)],
        group_id,
        study_type,
        self.__token,
        self.__host
      )

    except Exception as e:
      raise e

    finally:
      for zip_path in final_files:
        print ('Delete zip files: [{}]'.format(zip_path))
        os.system('rm {}'.format(zip_path))

    return output_dir


  def test_connection(self):
    """Test the connection with the host
    """
    url = urljoin(self.__host, 'api/v1/test_connection')

    print(f'Connecting to host at {url}')
    res = self.__https_agent.post(url=url)
    if res and 'status' in res and res['status'] == 200:
      print(f'Connection successful: {res["message"]}')
    else:
      print('Connection failed')


  def get_user_groups(self):
    """
      Get all the data sharing groups available for the current token
      ------------------
      Returns:
        [{
          'group_id': str (uuid),
          'group_name': str
        }, ...]
    """
    url = urljoin(self.__host, 'api/v1/get_user_groups')

    res = self.__https_agent.post(url=url)
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def _submit_study(
    self,
    group_id: str,
    study_id: str = None,
    name: str = 'To be detailed',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.XENIUM.value,
    technology_type: str = TechnologyType.LENS_SC.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    neg_controls_percentage: Union[int, float] = None,
  ):
    if study_id is None:
      study_id = get_uuid()

    if min_counts is None:
      min_counts = 0

    if min_genes is None:
      min_genes = 0

    if max_counts is None:
      max_counts = 1e9

    if max_genes is None:
      max_genes = 1e9

    if neg_controls_percentage is None:
      neg_controls_percentage = 100

    study_info = {
      'study_hash_id': study_id,
      'name': name,
      'authors': authors if authors else [],
      'abstract': abstract
    }

    return {
      'species': species,
      'group_id': group_id,
      'filter_params': {
        'min_counts': min_counts,
        'min_genes': min_genes,
        'max_counts': max_counts,
        'max_genes': max_genes,
        'neg_controls_percentage': neg_controls_percentage,
      },
      'study_type': technology_type,
      'platform': study_type,
      'study_info': study_info,
    }


  def submit_study_from_s3_lens_sc(
    self,
    group_id: str,
    batch_info: List[dict] = [],
    study_id: str = None,
    name: str = 'To be detailed',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.XENIUM.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    neg_controls_percentage: Union[int, float] = None,
  ):
    """
      Submit multiple single cell - spatial folders.
      ----------
      Args:
        group_id
          ID of the group to submit the data to.
        batch_info
          File path and batch name information, the path should exclude bucket path!
          Example:
            [{
              'name': 'study_1',
              'folder': 's3_path/study_folder',
            }, {...}]
        study_id
          If no value is provided, default id will be a random uuidv4 string
        name
          Name of the study.
        authors
          Authors of the study.
        abstract
          Abstract of the study.
        species
          Species of the study.
          Support:  Species.HUMAN.value
                    Species.MOUSE.value
                    Species.PRIMATE.value
                    Species.OTHERS.value
        study_type:
          The format of the study
          Support:  StudyType.VIZGEN.value
                    StudyType.COSMX.value
                    StudyType.XENIUM.value
        min_counts
          Minimum number of counts required for a cell to pass filtering.
        min_genes
          Minimum number of genes expressed required for a cell to pass filtering.
        max_counts
          Maximum number of counts required for a cell to pass filtering.
        max_genes
          Maximum number of genes expressed required for a cell to pass filtering.
        neg_controls_percentage
          Maximum number of control/negative genes percentage required for a cell to pass filtering.
          Ranging from 0 to 100
      """
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      study_type,
      TechnologyType.LENS_SC.value,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      neg_controls_percentage,
    )
    data['batch_info'] = {o['name']: o for o in batch_info}

    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/submit_study_from_s3'),
      body=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return common.get_submission_log(
      group_id=group_id, task_id=task_id, https_agent=self.__https_agent, host=self.__host
    )


  def submit_study_from_s3_proteomics(
    self,
    group_id: str,
    batch_info: dict = dict(),
    study_id: str = None,
    name: str = 'To be detailed',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None
  ):
    """
      Submit one Proteomics image.
      --------
      Args:
        group_id
          ID of the group to submit the data to.
        batch_info
          File path and batch name information, the path should EXCLUDE bucket path!
          Example:
            {
              'image': 's3_path/image.ome.tiff'
            }
        study_id
          If no value is provided, default id will be a random uuidv4 string
        name
          Name of the study.
        authors
          Authors of the study.
        abstract
          Abstract of the study.
        species
          Species of the study.
          Support:  Species.HUMAN.value
                    Species.MOUSE.value
                    Species.PRIMATE.value
                    Species.OTHERS.value
        min_counts
          Minimum number of counts required for a cell to pass filtering.
        min_genes
          Minimum number of genes expressed required for a cell to pass filtering.
        max_counts
          Maximum number of counts required for a cell to pass filtering.
        max_genes
          Maximum number of genes expressed required for a cell to pass filtering.
      """
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      -1,
      TechnologyType.PROTEOMICS.value,
      min_counts,
      min_genes,
      max_counts,
      max_genes
    )
    batch_info['name'] = batch_info['image']
    data['batch_info'] = [batch_info]

    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/submit_study_from_s3'),
      body=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return common.get_submission_log(
      group_id=group_id, task_id=task_id, https_agent=self.__https_agent, host=self.__host
    )


  def submit_study_from_local_lens_sc(
    self,
    group_id: str,
    batch_info: List[dict] = [],
    study_id: str = None,
    name: str = 'To be detailed',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.XENIUM.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    neg_controls_percentage: Union[int, float] = None,
  ):
    """
      Submit multiple single cell - spatial folders.
      -------
      Args:
        group_id
          ID of the group to submit the data to.
        batch_info
          File path and batch name information
          Example:
            [{
              'name': 'dataset_1',
              'folder': 'server_path/dataset_folder_1',
            }, {...}]
        study_id
          If no value is provided, default id will be a random uuidv4 string
        name
          Name of the study.
        authors
          Authors of the study.
        abstract
          Abstract of the study.
        species
          Species of the study.
          Support:  Species.HUMAN.value
                    Species.MOUSE.value
                    Species.PRIMATE.value
                    Species.OTHERS.value
        study_type:
          The format of the study
          Support:  StudyType.VIZGEN.value
                    StudyType.COSMX.value
                    StudyType.XENIUM.value
        min_counts
          Minimum number of counts required for a cell to pass filtering.
        min_genes
          Minimum number of genes expressed required for a cell to pass filtering.
        max_counts
          Maximum number of counts required for a cell to pass filtering.
        max_genes
          Maximum number of genes expressed required for a cell to pass filtering.
        neg_controls_percentage
          Maximum number of control/negative genes percentage required for a cell to pass filtering.
          Ranging from 0 to 100
      """

    if len(np.unique([x['name'] for x in batch_info])) != len(batch_info):
      raise Exception('Names of batches must be unique')

    output_dir = self._upload_fol_lens_sc(group_id, batch_info, study_type)

    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      study_type,
      TechnologyType.LENS_SC.value,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      neg_controls_percentage,
    )
    data['study_path'] = output_dir
    data['batch_info'] = [o['name'] for o in batch_info]

    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/submit_study_from_local'),
      body=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return common.get_submission_log(
      group_id=group_id, task_id=task_id, https_agent=self.__https_agent, host=self.__host
    )


  def submit_study_from_local_proteomics(
    self,
    group_id: str,
    batch_info: dict = dict(),
    study_id: str = None,
    name: str = 'To be detailed',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None
  ):
    """
      Submit one Proteomics image.
      -------
      Args:
        group_id
          ID of the group to submit the data to.
        batch_info
          File path and batch name information
          Example:
            {
              'image': 'server_path/image.ome.tiff'
            }
        study_id
          If no value is provided, default id will be a random uuidv4 string
        name
          Name of the study.
        authors
          Authors of the study.
        abstract
          Abstract of the study.
        species
          Species of the study.
          Support:  Species.HUMAN.value
                    Species.MOUSE.value
                    Species.PRIMATE.value
                    Species.OTHERS.value
        min_counts
          Minimum number of counts required for a cell to pass filtering.
        min_genes
          Minimum number of genes expressed required for a cell to pass filtering.
        max_counts
          Maximum number of counts required for a cell to pass filtering.
        max_genes
          Maximum number of genes expressed required for a cell to pass filtering.
      """
    study_type = -1
    batch_info['name'] = batch_info['image'].split('/')[-1]
    file_names = [batch_info['name']]
    files = [batch_info['image']]
    output_dir = common.upload_local(
      file_names,
      [Path(x) for x in files],
      group_id,
      study_type,
      self.__token,
      self.__host
    )

    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      study_type,
      TechnologyType.PROTEOMICS.value,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
    )
    data['study_path'] = output_dir
    data['batch_info'] = [batch_info['name']]

    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/submit_study_from_local'),
      body=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return common.get_submission_log(
      group_id=group_id, task_id=task_id, https_agent=self.__https_agent, host=self.__host
    )


  def query_genes(
    self,
    species: str,
    study_id: str,
    gene_names: List[str],
    unit: str = UNIT_RAW
  ):
    """
      Query genes expression in study.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study hash ID
        gene_names : list of str
          Querying gene names. If gene_names=[], full matrix will be returned
        unit: str
          Expression unit, UNIT_LOGNORM or UNIT_RAW. Default is UNIT_RAW
      --------------
      Returns
        expression_matrix : csc_matrix
          Expression matrix, shape=(n_cells, n_genes)
    """
    data = {
      'species': species,
      'study_id': study_id,
      'gene_names': gene_names,
      'unit': unit
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/query_genes'),
      body=data
    )
    return common.parse_query_genes_result(result)


  def get_metadata(
    self,
    species: str,
    study_id: str
  ):
    """
      Get full metadata of a study.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study hash ID
      -------------
      Returns
        Metadata: pd.DataFrame
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/get_metadata'),
      body=data
    )
    common.check_result_status(result)
    metadata_dict = result['data']
    metadata_df = pd.DataFrame(metadata_dict)
    return metadata_df


  def get_barcodes(
    self,
    species: str,
    study_id: str
  ):
    """
      Get barcodes of a study.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study hash ID
      -------------
      Returns
        Barcodes: List[str]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/get_barcodes'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def get_features(
    self,
    species: str,
    study_id: str
  ):
    """
      Get features of a study.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study hash ID
      -------------
      Returns
        Features: List[str]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/get_features'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def get_all_studies_info_in_group(
    self,
    species: str,
    group_id: str
  ):
    """
      Get info of all studies within group.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        group_id: str,
          Group hash id (uuid)
      -------------
      Returns
        [
          {
            'uuid': str (uuid),
            'study_hash_id': str (GSE******),
            'study_title': str,
            'created_by': str
          }, ...
        ]
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/get_all_studies_info_in_group'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def list_all_custom_embeddings(
    self,
    species: str,
    study_id: str
  ):
    """
      List out all custom embeddings in a study
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study id (uuid)
      -------------
      Returns
        [
          {
          'embedding_id': str,
          'embedding_name': str
          }, ...
        ]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/list_all_custom_embeddings'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def retrieve_custom_embedding(
    self,
    species: str,
    study_id: str,
    embedding_id: str
  ):
    """
      Retrive custom embedding array in the study
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study id (uuid)
        embedding_id: str,
          Embedding id (uuid)
      -------------
      Returns
        embedding_arr: np.ndarray
    """
    data = {
      'species': species,
      'study_id': study_id,
      'embedding_id': embedding_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/retrieve_custom_embedding'),
      body=data
    )
    common.check_result_status(result)
    coord_arr = result['data']['coord_arr']
    coord_shape = result['data']['coord_shape']
    return decode_base64_array(coord_arr, 'float32', coord_shape)


  def submit_metadata_from_dataframe(
    self,
    species: str,
    study_id: str,
    df: pd.DataFrame
  ):
    """
      Submit metadata dataframe directly to platform
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study id (uuid)
        df: pandas DataFrame,
          Barcodes must be in df.index!!!!
      -------------
      Returns
        'Successful' or Error log
    """
    metadata_dct = common.dataframe2dictionary(df)
    data = {
      'species': species,
      'study_id': study_id,
      'metadata_dct': metadata_dct
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/submit_metadata_dataframe'),
      body=data
    )
    common.check_result_status(result)
    return 'Successful'


  def submit_metadata_from_local(
    self,
    species: str,
    study_id: str,
    file_path: str
  ):
    """
      Submit metadata to platform with local path
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study id (uuid)
        file_path: local path leading to metadata file,
          Barcodes must be in the fist column
          File suffix must be in .tsv/.csv
      -------------
      Returns
        'Successful' or Error log
    """
    df = common.read_csv(file_path, index_col=0)
    return self.submit_metadata_from_dataframe(
      species,
      study_id,
      df
    )


  def submit_metadata_from_s3(
    self,
    species: str,
    study_id: str,
    file_path: str
  ):
    """
      Submit metadata to platform with s3 path
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study id (uuid)
        file_path: path in s3 bucket leading to metadata file,
          Barcodes must be in the fist column
          File suffix must be in .tsv/.csv
          file_path SHOULD NOT contain s3_bucket path configured in the platform
              E.g.  realpath: 's3://bucket/folder/metadata.tsv'
                    file_path: 'folder/metadata.tsv'
      -------------
      Returns
        'Successful' or Error log
    """
    data = {
      'species': species,
      'study_id': study_id,
      'file_path': file_path
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/submit_metadata_s3'),
      body=data
    )
    common.check_result_status(result)
    return 'Successful'


  def get_ontologies_tree(
    self,
    species,
    group_id,
  ):
    """
      Get metadata ontologies tree
      ------
      Args:
        species: str,
          Species of the study.
          Support:  Species.HUMAN.value
                    Species.MOUSE.value
                    Species.PRIMATE.value
                    Species.OTHERS.value
        group_id
          ID of the group.
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/get_ontologies'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def assign_standardized_meta(
    self,
    species,
    group_id,
    study_id,
    metadata_field,
    metadata_value,
    root_name,
    leaf_name,
  ):
    """
      Assign standardized term to metadata
      -------
      Args:
        species: str
          Species of the study.
          Support:  Species.HUMAN.value
                    Species.MOUSE.value
                    Species.PRIMATE.value
                    Species.OTHERS.value
        group_id: str
          ID of the group to submit the data to.
        study_id: str
          ID of the study (uuid)
        metadata_field: str
          ~ column name of meta dataframe in platform (eg: author's tissue)
        metadata_value: str
          ~ metadata value within the metadata field (eg: normal lung)
        root_name: str
          name of root in btr ontologies tree (eg: tissue)
        leaf_name: str
          name of leaf in btr ontologies tree (eg: lung)
    """
    ontologies_tree = self.get_ontologies_tree(species, group_id)
    root_id, leaf_id = common.parse_root_leaf_name(
      ontologies_tree,
      root_name,
      leaf_name
    )
    data = {
      'species': species,
      'group_id': group_id,
      'study_id': study_id,
      'group': metadata_field,
      'name': metadata_value,
      'root_id': root_id,
      'leaf_id': leaf_id,
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/assign_standardized_term'),
      body=data
    )
    common.check_result_status(result)
    return 'Successul'