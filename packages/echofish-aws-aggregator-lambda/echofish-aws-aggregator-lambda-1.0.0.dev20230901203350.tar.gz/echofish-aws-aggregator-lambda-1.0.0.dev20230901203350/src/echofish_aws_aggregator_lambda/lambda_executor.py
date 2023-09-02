# lambda_executor.py

import os
import json
import pandas as pd
from datetime import datetime
from botocore.exceptions import ClientError


TEMPDIR = "/tmp"

class LambdaExecutor:
    ############################################################################
    def __init__(
            self,
            s3_operations,
            dynamo_operations,
            sns_operations,
            table_name,
            done_topic_arn,
    ):
        self.__s3 = s3_operations
        self.__dynamo = dynamo_operations
        self.__sns_operations = sns_operations
        self.__table_name = table_name
        self.__done_topic_arn = done_topic_arn

    ############################################################################
    def __get_table_as_dataframe(
            self,
            ship_name,
            cruise_name,
            sensor_name,
            filter_status: str = None,
    ) -> pd.DataFrame:
        print('get table as dataframe')
        try:
            print(self.__table_name)
            table = self.__dynamo.get_table(table_name=self.__table_name)
            # Note: table.scan() has 1 MB limit on results so pagination is used
            response = table.scan()
            data = response['Items']
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])
        except ClientError as err:
            print('Problem finding the dynamodb table')
            raise err
        # Filter results when there are other cruises
        df = pd.DataFrame(data)
        df = df[(df['SHIP_NAME'] == ship_name) & (df['CRUISE_NAME'] == cruise_name) & (df['SENSOR_NAME'] == sensor_name)]
        ### Don't want to filter successes ###
        if filter_status:
            df_success = df[df['PIPELINE_STATUS'] == "POPULATING_CRUISE_ZARR"]
            if df_success.shape[0] == 0:
               raise
            return df_success
        return df.sort_values(by='START_TIME', ignore_index=True)

    ############################################################################
    def __update_processing_status(
            self,
            file_name: str,
            cruise_name: str,
            pipeline_status: str,
            error_message: str = None,
    ):
        print("Updating processing status.")
        if error_message:
            print(f"Error message: {error_message}")
            self.__dynamo.update_item(
                table_name=self.__table_name,
                key={
                    'FILE_NAME': {'S': file_name},      # Partition Key
                    'CRUISE_NAME': {'S': cruise_name},  # Sort Key
                },
                attribute_names={
                    '#PT': 'PIPELINE_TIME',
                    '#PS': 'PIPELINE_STATUS',
                    '#EM': 'ERROR_MESSAGE',
                },
                expression='SET #PT = :pt, #PS = :ps, #EM = :em',
                attribute_values={
                    ':pt': {
                        'S': datetime.now().isoformat(timespec="seconds") + "Z"
                    },
                    ':ps': {
                        'S': pipeline_status
                    },
                    ':em': {
                        'S': error_message
                    }
                }
            )
        else:
            self.__dynamo.update_item(
                table_name=self.__table_name,
                key={
                    'FILE_NAME': {'S': file_name},      # Partition Key
                    'CRUISE_NAME': {'S': cruise_name},  # Sort Key
                },
                attribute_names={
                    '#PT': 'PIPELINE_TIME',
                    '#PS': 'PIPELINE_STATUS',
                },
                expression='SET #PT = :pt, #PS = :ps',
                attribute_values={
                    ':pt': {
                        'S': datetime.now().isoformat(timespec="seconds") + "Z"
                    },
                    ':ps': {
                        'S': pipeline_status
                    }
                }
            )
        print("Done updating processing status.")

    ############################################################################
    def __publish_done_message(
            self,
            message
    ):
        print("Sending done message")
        self.__sns_operations.publish(self.__done_topic_arn, json.dumps(message))

    ############################################################################
    def __update_processing_status(
            self,
            file_name: str,
            cruise_name: str,
            pipeline_status: str,
            error_message: str = None,
    ):
        print("Updating processing status.")
        if error_message:
            print(f"Error message: {error_message}")
            self.__dynamo.update_item(
                table_name=self.__table_name,
                key={
                    'FILE_NAME': {'S': file_name},      # Partition Key
                    'CRUISE_NAME': {'S': cruise_name},  # Sort Key
                },
                attribute_names={
                    '#PT': 'PIPELINE_TIME',
                    '#PS': 'PIPELINE_STATUS',
                    '#EM': 'ERROR_MESSAGE',
                },
                expression='SET #PT = :pt, #PS = :ps, #EM = :em',
                attribute_values={
                    ':pt': {
                        'S': datetime.now().isoformat(timespec="seconds") + "Z"
                    },
                    ':ps': {
                        'S': pipeline_status
                    },
                    ':em': {
                        'S': error_message
                    }
                }
            )
        else:
            self.__dynamo.update_item(
                table_name=self.__table_name,
                key={
                    'FILE_NAME': {'S': file_name},      # Partition Key
                    'CRUISE_NAME': {'S': cruise_name},  # Sort Key
                },
                attribute_names={
                    '#PT': 'PIPELINE_TIME',
                    '#PS': 'PIPELINE_STATUS',
                },
                expression='SET #PT = :pt, #PS = :ps',
                attribute_values={
                    ':pt': {
                        'S': datetime.now().isoformat(timespec="seconds") + "Z"
                    },
                    ':ps': {
                        'S': pipeline_status
                    }
                }
            )
        print("Done updating processing status.")


    ############################################################################
    def execute(self, input_message):
        ship_name = input_message['shipName']
        cruise_name = input_message['cruiseName']
        sensor_name = input_message['sensorName']
        file_name = input_message['fileName']
        #
        try:
            # store_name = f"{os.path.splitext(file_name)[0]}.zarr"
            # output_zarr_prefix = f"level_1/{ship_name}/{cruise_name}/{sensor_name}"
            # bucket_key = f"data/raw/{ship_name}/{cruise_name}/{sensor_name}/{file_name}"
            # zarr_prefix = os.path.join("level_1", ship_name, cruise_name, sensor_name)
            #
            # TODO: each time message is received, check if all files are done processing
            # if no, do nothing, if yes, update status and send sns email message
            #
            #########################################################################
            # [0] get dynamoDB table info
            df = self.__get_table_as_dataframe(ship_name, cruise_name, sensor_name)
            file_names = list(df['FILE_NAME'])
            #
            ###################################################################
            total_number_of_files = list(df['FILE_NAME'])
            completed_files = []
            failed_files = []
            processing_files = []
            # iterate all files in dataframe
            for file_name in file_names:
                current_status = list( df[df['FILE_NAME'] == file_name]['PIPELINE_STATUS'].values)[0]
                if current_status == 'SUCCESS_RESAMPLE_AND_WRITE_TO_ZARR_STORE' or current_status == 'POPULATING_CRUISE_ZARR':
                    completed_files.append(file_name)
                elif current_status.find('FAIL') >= 0:
                    failed_files.append(file_name)
                else:
                    processing_files.append(file_name)
            # Don't want to send all the file names, just the counts
            if (len(completed_files) + len(failed_files)) == len(total_number_of_files):
                email_message = {
                    "completed_files": len(completed_files),
                    "processing_files": len(processing_files),
                    "failed_files": len(failed_files),
                    "shipName": ship_name,
                    "cruiseName": cruise_name,
                    "sensorName": sensor_name
                }
                self.__publish_done_message(email_message)
                # TODO: update statuses as DONE...
                for file_name in file_names:
                    self.__update_processing_status(
                        file_name=file_name,
                        cruise_name=cruise_name,
                        pipeline_status='SENDING_SNS_MESSAGE',  # TODO: overwriting the dynamo error message???
                    )
            else:
                print(f'Signal from {file_name}, {len(processing_files)} files are still processing.')
                return
            ###################################################################
            ###################################################################
        except Exception as err:
            print(f'Exception encountered: {err}')
        #######################################################################
