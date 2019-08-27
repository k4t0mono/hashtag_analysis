from utils import Tweet, api, client


callback = client.submitAsync(
    'g.addV("person").property("id", "thomas").property("firstName", "Thomas").property("age", 44).property("pk", "pk")'
)
