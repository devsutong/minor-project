from django.test import TestCase
from channels.testing import HttpCommunicator
from .consumers import SocketConsumer

class MyTests(TestCase):
    async def test_my_consumer(self):
        communicator = HttpCommunicator(SocketConsumer, "GET", "/chats/")
        response = await communicator.get_response()
        self.assertEqual(response["body"], b"test response")
        self.assertEqual(response["status"], 200)