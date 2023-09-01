from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud.src.generic_crud import GenericCRUD
from dotenv import load_dotenv
load_dotenv()

PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 190
PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "profile_profile_local"
DEVELOPER_EMAIL = "idan.a@circ.zone"
obj = {
    'component_id': PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

logger = Logger.create_logger(object=obj)


class ProfileProfile(GenericCRUD):
    def __init__(self) -> None:
        pass

    def insert_profile_profile(self, profile_id1: int, profile_id2: int, relationship_type_id: int, job_title: str = None) -> int:
        json = {
            'profile_id1': profile_id1,
            'profile_id2': profile_id2,
            'relationship_type_id': relationship_type_id,
            'job_title': job_title
        }
        logger.start(object=json)
        data = {
            'profile_id1': profile_id1,
            'profile_id2': profile_id2,
            'relationship_type_id': relationship_type_id,
            'job_title': f"'{job_title}'"
        }
        profile_profile_id = self.insert("profile_profile",
                                         " profile_profile_table", data).get("contacts ids")[0]
        logger.end(object={"profile_profile_id": profile_profile_id})
        return profile_profile_id

    def update_profile_profile_relationship_id(self, relationship_type_id: int, id_collumn_value: int) -> None:
        json = {
            'relationship_type_id': relationship_type_id
        }
        logger.start(object=json)
        data = {
            'relationship_type_id': relationship_type_id
        }
        self.update(schema_name="profile_profile",
                    table_name="profile_profile_table", data_json=data, id_column_name="profile_profile_id", id_column_value=id_collumn_value)
        logger.end("profile_profile updated")

    def delete_profile_profile(self, profile_profile_id: int) -> None:
        json = {
            "profile_profile_id": profile_profile_id,
        }
        logger.start(object=json)
        self.delete(schema_name="profile_profile",
                    table_name="profile_profile_table", data_json=json, id_column_name="profile_profile_id", id_column_value=profile_profile_id)
        logger.end("profile_profile deleted")

    def get_profile_profile(self, profile_profile_id: int) -> any:
        json = {
            "profile_profile_id": profile_profile_id
        }
        logger.start(object=json)
        profile_profile_record = self.get_records_by_id(schema_name="profile_profile",
                                                        table_name="profile_profile_view", id_column_name="profile_profile_id", id_column_value=profile_profile_id)
        logger.end(
            object={"profile_profile_record": str(profile_profile_record)})
        return profile_profile_record
