"""Semantic Facebook selector candidates derived from the working client.

Selectors are kept in the Camofox layer so domain actions express intent
(title, price, composer, OTP, etc.) rather than browser-driver details.
"""

LOGIN_EMAIL = ["input[name='email']", "input[type='email']"]
LOGIN_PASSWORD = ["input[name='pass']", "input[type='password']"]
LOGIN_SUBMIT = [
    "button[name='login']",
    "button[type='submit']",
    "button:has-text('Log In')",
    "button:has-text('Log in')",
]
OTP = [
    "input[name='approvals_code']",
    "input[autocomplete='one-time-code']",
]

MESSAGE_THREAD_LINKS = ["a[href*='/messages/t/']"]
MESSAGE_COMPOSER = [
    "[role='textbox'][contenteditable='true']",
    "div[contenteditable='true'][aria-label*='message' i]",
    "div[contenteditable='true'][data-lexical-editor='true']",
]

MARKETPLACE_IMAGE_INPUT = ["input[type='file'][accept*='image']", "input[type='file']"]
TITLE = [
    "input[aria-label='Title']",
    "input[aria-label='Titre']",
    "input[aria-label='Tytuł']",
    "input[aria-label='Título']",
    "input[aria-label='Titel']",
]
PRICE = [
    "input[aria-label='Price']",
    "input[aria-label='Prix']",
    "input[aria-label='Cena']",
    "input[aria-label='Precio']",
    "input[aria-label='Preis']",
]
DESCRIPTION = [
    "textarea[aria-label='Description']",
    "textarea[aria-label='Description, optional']",
]
CATEGORY = ["[role='combobox'][aria-label='Category']", "[role='combobox'][aria-label='Catégorie']"]
CONDITION = ["[role='combobox'][aria-label='Condition']", "[role='combobox'][aria-label='État']"]
NEXT = [
    "div[aria-label='Next']:not([aria-disabled='true'])",
    "button:has-text('Next')",
]
PUBLISH = [
    "div[aria-label='Publish']:not([aria-disabled='true'])",
    "button:has-text('Publish')",
]
