from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud.src.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger


PHONE_LOCAL_PYTHON_COMPONENT_ID = 200
PHONE_LOCAL_PYTHON_COMPONENT_NAME = 'phone-local'

object_init = {
    'component_id': PHONE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': PHONE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": "jenya.b@circ.zone"
}
logger = Logger.create_logger(object=object_init)


class PhonesLocal(GenericCRUD):
    def __init__(self) -> None:
        pass

    def get_phone_number_by_profile_id(profile_id: int) -> list:
        logger.start("Return phone number by profile id",
                     object={"profile_id": profile_id})
        try:
            data = GenericCRUD.get_records_by_id("telephone", "telephone_table_should_be_merged_into_phone_table",
                                                 profile_id, profile_id)
            profile_id = data[0][0]
            phone_number = data[0][2]
            logger.end("return list with id and phone number", object={
                       'profile_id': profile_id, 'phone_num': phone_number})
            return profile_id, phone_number
        except Exception as e:
            logger.exception(object=e)
            logger.end()
            raise Exception
