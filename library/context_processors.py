from django.apps import apps

def model_list(request):
    # Fetch all models in the project
    models = apps.get_models()
    return {'models': models}
