from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_ATTRS_SVG = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'

# Chaque valeur est le contenu intérieur d'un <svg ...>...</svg> (style Feather/Tabler,
# traits simples). Pas de dépendance à une police ou un CDN externe : ça s'affiche
# toujours, même sans connexion à un service tiers.
ICONES_SVG = {
    "bouclier": '<path d="M12 3l7 3v6c0 4.2-2.8 7.4-7 9-4.2-1.6-7-4.8-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "cible": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "loupe": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M20 20l-4.7-4.7"/>',
    "personne-code": '<circle cx="12" cy="8" r="3.2"/><path d="M5 20c0-3.6 3-6 7-6s7 2.4 7 6"/>',
    "alerte": '<path d="M12 4l9 16H3z"/><path d="M12 10v4"/><path d="M12 17.2v.1"/>',
    "cle": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9"/><path d="M16 7l3 3"/><path d="M13.5 9.5l2.5 2.5"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.4 2.3 3.8 5.3 3.8 8.5s-1.4 6.2-3.8 8.5c-2.4-2.3-3.8-5.3-3.8-8.5S9.6 5.8 12 3.5z"/>',
    "presse-papier": '<rect x="6" y="4.5" width="12" height="16" rx="1.5"/><rect x="9" y="3" width="6" height="3" rx="1"/><path d="M9 11h6"/><path d="M9 14.5h6"/><path d="M9 18h4"/>',
    "ecran": '<rect x="3.5" y="4.5" width="17" height="12" rx="1.5"/><path d="M9 20.5h6"/><path d="M12 16.5v4"/>',
    "panier": '<path d="M4 5h2.5l1.3 11.2a2 2 0 002 1.8h7a2 2 0 002-1.8L20 8H7"/><circle cx="10" cy="20.5" r="1.2"/><circle cx="17" cy="20.5" r="1.2"/>',
    "reglages": '<circle cx="12" cy="12" r="3"/><path d="M12 3.5v2.4M12 18.1v2.4M20.5 12h-2.4M5.9 12H3.5M18 6l-1.7 1.7M7.7 16.3L6 18M18 18l-1.7-1.7M7.7 7.7L6 6"/>',
    "lien": '<path d="M9.5 14.5l5-5"/><path d="M13 8l1.8-1.8a3.5 3.5 0 015 5L18 13"/><path d="M11 16l-1.8 1.8a3.5 3.5 0 01-5-5L6 11"/>',
    "outil": '<path d="M14.5 6.5a4 4 0 015.6 5.6L15 17.2 6.8 21 10.8 12.9 15.9 8a4 4 0 01-1.4-1.5z"/><path d="M6.8 21l2-4"/>',
    "fusee": '<path d="M12 3c2.8 1.6 4.5 4.6 4.5 9 0 2-.6 3.7-1.6 5l-2.9 2.5-2.9-2.5c-1-1.3-1.6-3-1.6-5 0-4.4 1.7-7.4 4.5-9z"/><circle cx="12" cy="10.5" r="1.6"/><path d="M9 17.5l-2.5 3M15 17.5l2.5 3"/>',
    "mobile": '<rect x="7.5" y="3" width="9" height="18" rx="2"/><path d="M11 18.3h2"/>',
    "tableau": '<rect x="3.5" y="4" width="17" height="12" rx="1.5"/><path d="M8 20l2-4M16 20l-2-4"/><path d="M7 8.5h6M7 11.5h4"/>',
    "cadenas": '<rect x="5" y="10.5" width="14" height="9.5" rx="1.5"/><path d="M8 10.5V7.5a4 4 0 018 0v3"/>',
    "diplome": '<path d="M12 4L2 8.5 12 13l10-4.5z"/><path d="M6 10.7v5c0 1.4 2.7 2.8 6 2.8s6-1.4 6-2.8v-5"/>',
    "code": '<path d="M9 8l-5 4.5L9 17"/><path d="M15 8l5 4.5-5 4.5"/>',
    "livres": '<path d="M4 5.5c2-1 4.5-1 6.5 0v13c-2-1-4.5-1-6.5 0z"/><path d="M20 5.5c-2-1-4.5-1-6.5 0v13c2-1 4.5-1 6.5 0z"/>',
    "check": '<circle cx="12" cy="12" r="8.5"/><path d="M8.2 12.3l2.6 2.6 5-5.2"/>',
    "recu": '<path d="M6 3.5h12v17l-2.2-1.5L14 20.5l-2-1.5-2 1.5-1.8-1.5L6 20.5z"/><path d="M9 8h6M9 11.5h6M9 15h4"/>',
    "calendrier": '<rect x="3.5" y="5" width="17" height="15.5" rx="1.5"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
    "piece": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5v9"/><path d="M14.7 9.3c-.4-.9-1.4-1.4-2.7-1.4-1.5 0-2.7.8-2.7 2s1.2 1.7 2.7 2 2.7.8 2.7 2-1.2 2-2.7 2c-1.3 0-2.3-.5-2.7-1.4"/>',
    "utilisateurs": '<circle cx="8.5" cy="8.5" r="3"/><circle cx="16.5" cy="9.5" r="2.5"/><path d="M3 20c0-3 2.5-5 5.5-5s5.5 2 5.5 5"/><path d="M14.5 15.3c2.4.4 4 2.1 4 4.7"/>',
}

# Correspondance emoji (déjà saisi dans l'admin) -> clé d'icône ci-dessus.
CORRESPONDANCES = {
    "🛡️": "bouclier", "🛡": "bouclier",
    "🎯": "cible",
    "🔍": "loupe",
    "🧑‍💻": "personne-code", "👨‍💻": "personne-code",
    "🚨": "alerte",
    "🔑": "cle",
    "🌐": "globe",
    "📋": "presse-papier",
    "🖥️": "ecran", "🖥": "ecran",
    "🛒": "panier",
    "⚙️": "reglages", "⚙": "reglages",
    "🔗": "lien",
    "🛠️": "outil", "🛠": "outil",
    "🚀": "fusee",
    "📱": "mobile",
    "👨‍🏫": "tableau", "🧑‍🏫": "tableau",
    "🔐": "cadenas",
    "🎓": "diplome",
    "💻": "code",
    "📚": "livres",
    "✅": "check",
    "🧾": "recu",
    "📅": "calendrier",
    "💰": "piece",
    "👥": "utilisateurs",
}


@register.filter
def icone_vecteur(emoji):
    """
    Affiche une icône SVG intégrée (aucune dépendance externe) correspondant
    à l'emoji stocké en base, ou l'emoji lui-même si aucune correspondance
    n'est trouvée. Utilisation : {{ service.icone|icone_vecteur }}
    """
    cle = CORRESPONDANCES.get((emoji or "").strip())
    contenu = ICONES_SVG.get(cle)
    if contenu:
        return mark_safe(f'<svg {_ATTRS_SVG} width="22" height="22" aria-hidden="true">{contenu}</svg>')
    return emoji
