from enum import Enum


# TODO: We should order them by alphabet of the Entity

class ActionName(Enum):
    ADD_LOG = "add"
    ANALYZE_FACIAL_IMAGE = "analyzeFacialImage"
    CREATE_USER = "createUser"
    EVENT = "event"
    GENDER_DETECTION = "process"    
    GET_ALL_GROUPS = "getAllGroups"
    GET_GROUP_BY_ID = "getGroupById"
    GET_GROUP_BY_NAME = "getGroupByName"
    GRAPHQL = "graphql"
    LOGIN = "login"
    TIMELINE = "timeline"
    UPDATE_USER = "updateUser"
    VALIDATE_JWT = "validateJwt"
    CREATE_GROUP_PROFILE="createGroupProfile"
    DELETE_GROUP_PROFILE="deleteGroupProfile"
    GET_GROUP_PROFILE_BY_GROUP_ID_PROFILE_ID="getGroupProfileByGroupIdProfileId"
    