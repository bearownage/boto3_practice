import graphene
import boto3 
import requests 
import json
from decimal import Decimal

from config import movie_api_key
from config import aws_key
from config import aws_secret_key


#GraphSQL Code just hear will replace soon

#class Query(graphene.ObjectType):
#  hello = graphene.String(name=graphene.String(default_value="World"))
#
#  def resolve_hello(self, info, name):
#    return 'Hello ' + name

#schema = graphene.Schema(query=Query)
#result = schema.execute('{ hello }')
#print(result.data['hello']) # "Hello World"

search_string = "batman"
response = requests.get("https://api.themoviedb.org/3/search/movie?api_key="
        + movie_api_key + "&language=en-US&query=" + search_string + "&page=1&include_adult=false")

if response.status_code == 200:
    #print('Success!')
    #
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret_key, region_name="us-east-2")

    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table('films')

    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    print(table.creation_date_time)
    #print(response.content)
    result = json.loads(response.text)
    
    #print(type(result['results']))
    for movie in result['results']:
        #print(movie))
        movie_id = movie['id']
        title = movie['title']
        release_date = movie['release_date']
        rating = Decimal(str(movie['vote_average']))
        description = movie['overview']
        popularity = Decimal(str(movie['popularity']))

        table.put_item(
                Item={
                    'movie_id' : movie_id,
                    'title' : title,
                    'release_date' : release_date,
                    'rating' : rating,
                    'description' : description,
                    'popularity' : popularity
                
                    }
                )

        #print( title + " " + release_date + " " + str(rating) + " " + description
        #        + " " + str(popularity))
        #print()
elif response.status_code == 404:
    print('Not Found.')
