from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Correspondance emoji -> icône vectorielle Tabler (https://tabler.io/icons).
# Si un emoji saisi dans l'admin n'est pas dans cette liste, on l'affiche
# tel quel (aucune donnée existante n'est perdue ou cassée).
CORRESPONDANCES = {
    "🛡️": "shield-check",
    "🛡": "shield-check",
    "🎯": "target-arrow",
    "🔍": "zoom-scan",
    "🧑‍💻": "user-code",
    "👨‍💻": "user-code",
    "🚨": "alert-triangle",
    "🔑": "key",
    "🌐": "world",
    "📋": "clipboard-list",
    "🖥️": "device-desktop",
    "🖥": "device-desktop",
    "🛒": "shopping-cart",
    "⚙️": "settings",
    "⚙": "settings",
    "🔗": "link",
    "🛠️": "tools",
    "🛠": "tools",
    "🚀": "rocket",
    "📱": "device-mobile",
    "👨‍🏫": "chalkboard",
    "🧑‍🏫": "chalkboard",
    "🔐": "lock",
    "🎓": "school",
    "💻": "code",
    "📚": "books",
    "✅": "circle-check",
    "🧾": "receipt",
    "📅": "calendar",
    "💰": "coin",
    "👥": "users",
}


@register.filter
def icone_vecteur(emoji):
    """
    Affiche l'icône vectorielle correspondant à l'emoji stocké en base,
    ou l'emoji lui-même si aucune correspondance n'est trouvée.
    Utilisation dans un template : {{ service.icone|icone_vecteur }}
    """
    nom_icone = CORRESPONDANCES.get((emoji or "").strip())
    if nom_icone:
        return mark_safe(f'<i class="ti ti-{nom_icone}" aria-hidden="true"></i>')
    return emoji
