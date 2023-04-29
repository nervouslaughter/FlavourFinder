from google.cloud import translate_v2 as translate

# Initialize the client
def translate_review(rev, target_language = "en"):
    translate_client = translate.Client.from_service_account_json('credents.json')
    text = rev
    result = translate_client.detect_language(text)
    source_lang = result["language"]
    translation = translate_client.translate(text, source_language=source_lang, target_language=target_language)
    return (translation['translatedText'])

print(translate_review("Bonjour?"))
