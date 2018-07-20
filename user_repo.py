#!/usr/bin/env python
from properties import MONGO_DOCKER, MONGO_LOCAL
from bson import ObjectId
from pymongo import MongoClient
import logging
from pprint import pprint


# for dockerised version
#client = MongoClient(MONGO_DOCKER)

# for local deployment
client = MongoClient(MONGO_LOCAL)

db = client.text3
collection = db.users

def create_one(document):
    '''
    Saves a document to the database
    :param document: the document to be saved
    :return: the newly created document's ID as string
    '''
    try:
        result = collection.insert_one(document).inserted_id
    except:
        logging.error("CANNOT SAVE TO MONGODB!")
        raise ValueError
    logging.info('CREATED: ' + str(result))
    return str(result)


def get_by_id(id):
    '''
    Gets a document by its ID
    :param id: the required document's ID
    :return: the required document in a JSON format (_id converted to string)
    '''
    entry = None
    try:
        entry = collection.find_one({'_id': ObjectId(id)})
    except:
        logging.error("ERROR DURING FETCH FROM MONGODB!")
    if entry:
        entry['_id'] = str(entry['_id'])
        logging.info('FETCHED: ' + str(entry))
    return entry


def get_by_name_and_pw(user_name, pw):
    try:
        user = collection.find_one({"username": user_name, "password": pw})
        user['_id'] = str(user['_id'])
    except:
        logging.error("ERROR DURING FETCH FROM MONGODB!")
        return None
    logging.info('FETCHED: ' + str(user))
    return user


def get_by_name(user_name):
    try:
        user = collection.find_one({"username": user_name})
        user['_id'] = str(user['_id'])
    except:
        logging.error("ERROR DURING FETCH FROM MONGODB!")
        return None
    logging.info('FETCHED: ' + str(user))
    return user


def delete_by_id(id):
    '''
    Deletes a document by ID
    :param id: the document's ID to be deleted
    :return: True (if successful)
    '''
    try:
        result = collection.delete_one({'_id': ObjectId(id)}).acknowledged
    except:
        logging.error("ERROR DURING DELETION FROM MONGODB!")
        return None
    logging.info('DELETED: ' + str(id))
    return result


def get_ids_str():
    '''
    Returns the available document IDs
    :return: List of document ID (_id) strings
    '''
    id_list = []
    try:
        documents = collection.find({})
        for document in documents:
            id_list.append(str(document['_id']))
    except:
        logging.error("ERROR DURING GETTING IDS FROM MONGODB!")
        return None
    logging.info('FOUND: ' + str(id_list))
    return id_list

def _example():
    '''
    example usage, going through the lifecycle of a document and prints it
    :return: None
    '''

    res = get_by_id("5af997faaf2f4605ec1b2642")
    print(res)

    test_data = { "username" : "user001",
                   "password" : "pass1234"}
    res = create_one(test_data)
    print('CREATED: ')
    pprint(res)
    res = get_by_id(res)
    print('FETCHED: ')
    pprint(res)
    res = get_by_name_and_pw("user001", "pass1234")
    print('FETCHED: ')
    pprint(res)
    res = delete_by_id(res['_id'])
    print('DELETED: ')
    pprint(res)


if __name__ == '__main__':
    _example()
