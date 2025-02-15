from .utils import get_opensearch_client

def convert_to_opensearch_format(dynamodb_item):
  item = {}
  for key, value in dynamodb_item.items():
    type_key = list(value.keys())[0]
    if key == 'attributes':
      item[key] = [v[list(v.keys())[0]] for v in value[type_key]]
    else:
      item[key] = value[type_key]
  return item

def handler(event, context):
  client = get_opensearch_client()
  index_name = 'japanese-folktales'
  try:
    for record in event['Records']:
      event_name = record['eventName']
      if event_name in ['INSERT', 'MODIFY']:
        item = convert_to_opensearch_format(record['dynamodb']['NewImage'])
        client.index(index=index_name, body=item, id=item['id'], refresh=True)
        print(f"Successfully indexed document {item['id']}")
      elif event_name == 'REMOVE':
        item = convert_to_opensearch_format(record['dynamodb']['OldImage'])
        try:
          client.delete(index=index_name, id=item['id'], refresh=True)
          print(f"Successfully deleted document {item['id']}")
        except Exception as e:
          print(f"Error deleting document {item['id']}: {e}")
    return {
      'statusCode': 200,
      'body': 'Successfully processed DynamoDB Stream events'
    }
  
  except Exception as e:
      print(f"Error processing records: {str(e)}")
      raise e
