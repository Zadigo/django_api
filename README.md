# APIs for Django

# Responsive

Responsive is a context processor for Django templates that detects if the request is coming from a Mobile and persists the value True or False into the templates.

## Implementing the API

In your settings file, call __from your_project.responsive.responsive_context_processor__ into the list of context processors:

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                ...
                'shop.logic.stripe_context_processors'
            ],
        },
    },
]
```

Once done, you'll be able to create logic specific for mobiles into your templates.
