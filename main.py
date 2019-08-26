from gremlin_python.driver import client, serializer


client = client.Client('wss://f454303c-0ee0-4-231-b9ee.gremlin.cosmos.azure.com:443/', 'g', 
    username='/dbs/dm_project/colls/tweets', 
    password='nHzRAVKOFkCIiRBcdAaFYz3rPqgtb6vnG4lejVpBQRHQs3RHXlcN5wxm7npkQqAHleZPoeyLNuUHTTRqFwJ2TA==',
    message_serializer=serializer.GraphSONSerializersV2d0()
)

callback = client.submitAsync(
    'g.addV("person").property("id", "thomas").property("firstName", "Thomas").property("age", 44).property("pk", "pk")'
)
