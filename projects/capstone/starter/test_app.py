import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values


from app import create_app
from models import setup_db, Movie, Actor
from config import Testing


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        config = dotenv_values()
        self.database_name = config["DBNAME"]
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            config["USERNAME"],
            config["PASSWORD"],
            config["HOSTNAME"] + ":" + config["PORT"],
            self.database_name,
        )

        # setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
        # with self.app.app_context():
        #     self.db = self.app.extensions['sqlalchemy'].db

        # Test Data
        self.new_actor_one = {
                "name" : "Richard",
                "age" : 34,
                "gender": "Male"
            }

        self.new_actor_two = {
                "name" : "Diane",
                "age" : 55,
                "gender": "Female"
            }

        self.new_movie_one = {
                "title" : "Minion",
                "release_date" : "22-07-2024"
            }

        self.new_movie_two = {
                "title" : "Richard",
                "release_date" : "31-12-2025"
            }
        
        self.cast_assistant_header = {
            'Authorization': 'Bearer ' + Testing.cast_assistant_token}
        
        self.cast_director_header = {
            'Authorization': 'Bearer ' + Testing.cast_director_token}
        
        self.exec_producer_header = {
            'Authorization': 'Bearer ' + Testing.exec_producer_token}

        


        
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test Cases for Casting Assistant
    def test_get_actors_cast_assistant(self):
        res = self.client().get("/actors", headers=self.cast_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_get_movies_cast_assistant(self):
        res = self.client().get("/movies", headers=self.cast_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # def test_add_actor_cast_assistant(self):
        res = self.client().post("/actors", headers=self.cast_assistant_header, json=self.new_actor_one)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_add_movie_cast_assistant(self):
        res = self.client().post("/movies", headers=self.cast_assistant_header, json=self.new_movie_one)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_update_actor_cast_assistant(self):
        res = self.client().patch("/actors/1", headers=self.cast_assistant_header, json=self.new_actor_two)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_update_movie_cast_assistant(self):
        res = self.client().patch("/movies/1", headers=self.cast_assistant_header, json=self.new_movie_two)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_delete_actor_cast_assistant(self):
        res = self.client().delete("/actors/1", headers=self.cast_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_delete_movie_cast_assistant(self):
        res = self.client().patch("/movies/1", headers=self.cast_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)


    # Test Cases for Casting Director
        
    def test_get_actors_cast_director(self):
        res = self.client().get("/actors", headers=self.cast_director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_get_movies_cast_director(self):
        res = self.client().get("/movies", headers=self.cast_director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_actor_cast_director(self):
        res = self.client().post("/actors", headers=self.cast_director_header, json=self.new_actor_one)
        # print('res1: ', res.get_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        return data["actors"][0]["id"]

    def test_add_movie_cast_director(self):
        res = self.client().post("/movies", headers=self.cast_director_header, json=self.new_movie_one)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_update_actor_cast_director(self):
        res = self.client().patch("/actors/1", headers=self.cast_director_header, json=self.new_actor_two)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        

    # def test_update_movie_cast_director(self):
    #     res = self.client().patch("/movies/1", headers=self.cast_director_header, json=self.new_movie_two)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)

    def test_delete_actor_cast_director(self):
        actor_id = self.test_add_actor_cast_director()
        # print('actor id: ', actor_id)
        res = self.client().delete("/actors/" + str(actor_id), headers=self.cast_director_header)
        # print('res: ', res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        

    def test_delete_movie_cast_director(self):
        res = self.client().delete("/movies/1", headers=self.cast_director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)


    # Test Cases for Executive Producer
        
    def test_get_actors_exec_producer(self):
        res = self.client().get("/actors", headers=self.exec_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_get_movies_exec_producer(self):
        res = self.client().get("/movies", headers=self.exec_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_actor_exec_producer(self):
        res = self.client().post("/actors", headers=self.exec_producer_header, json=self.new_actor_one)
        # print('res1: ', res.get_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        return data["actors"][0]["id"]

    def test_add_movie_exec_producer(self):
        res = self.client().post("/movies", headers=self.exec_producer_header, json=self.new_movie_one)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_update_actor_exec_producer(self):
        res = self.client().patch("/actors/1", headers=self.exec_producer_header, json=self.new_actor_two)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_update_movie_exec_producer(self):
        res = self.client().patch("/movies/3", headers=self.exec_producer_header, json=self.new_movie_two)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_actor_exec_producer(self):
        actor_id = self.test_add_actor_cast_director()
        res = self.client().delete("/actors/" + str(actor_id), headers=self.exec_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # def test_delete_movie_exec_producer(self):
    #     movie_id = self.test_add_movie_exec_producer
    #     res = self.client().delete("/movies/" + str(movie_id), headers=self.exec_producer_header)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()