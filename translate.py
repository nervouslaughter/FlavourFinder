from google.cloud import translate_v2 as translate

# Initialize the client
translate_client = translate.Client.from_service_account_json('credents.json')
text = 'Hello, how are you?'
source_language = 'en'
target_language = 'es'
translation = translate_client.translate(text, source_language=source_language, target_language=target_language)
print(translation['input'])
print(translation['translatedText'])
