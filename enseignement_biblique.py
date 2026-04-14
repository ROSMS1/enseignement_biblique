import streamlit as st

# ─────────────────────────────────────────────
#  CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Enseignement Biblique",
    page_icon="✝️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  CSS MOBILE-FRIENDLY
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { padding: 0.5rem 0.8rem; }
    h1 { font-size: 1.4rem !important; text-align: center; color: #2c5f2e; }
    h2 { font-size: 1.15rem !important; color: #2c5f2e; margin-top: 1.2rem; }
    h3 { font-size: 1.0rem !important; color: #4a7c59; margin-top: 0.8rem; }

    .verse-box {
        background: linear-gradient(135deg, #f0f7f0, #e8f4e8);
        border-left: 4px solid #2c5f2e;
        border-radius: 8px;
        padding: 12px 14px;
        margin: 8px 0;
        font-style: italic;
        font-size: 0.92rem;
        color: #1a3a1c;
    }
    .ref-badge {
        display: inline-block;
        background: #2c5f2e;
        color: white;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: bold;
        margin-bottom: 6px;
    }
    .comment-box {
        background: #fafafa;
        border: 1px solid #ddeedd;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0 14px 0;
        font-size: 0.9rem;
        color: #333;
        line-height: 1.6;
    }
    .key-point {
        background: #fff8e1;
        border-left: 4px solid #f4a21e;
        border-radius: 6px;
        padding: 10px 14px;
        margin: 10px 0;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .section-header {
        background: linear-gradient(90deg, #2c5f2e, #4a7c59);
        color: white;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 14px 0 8px 0;
    }
    .tab-intro {
        background: #e8f5e9;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 0.93rem;
        color: #1b4d1e;
        line-height: 1.65;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.78rem;
        padding: 6px 10px;
        background: #e8f4e8;
        border-radius: 8px;
    }
    .stTabs [aria-selected="true"] { background: #2c5f2e !important; color: white !important; }
    div[data-testid="stExpander"] { border: 1px solid #c8e6c9; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def verse(ref, texte):
    st.markdown(f'<span class="ref-badge">📖 {ref}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="verse-box">{texte}</div>', unsafe_allow_html=True)

def comment(texte):
    st.markdown(f'<div class="comment-box">{texte}</div>', unsafe_allow_html=True)

def key_point(texte):
    st.markdown(f'<div class="key-point">💡 {texte}</div>', unsafe_allow_html=True)

def section(titre):
    st.markdown(f'<div class="section-header">📌 {titre}</div>', unsafe_allow_html=True)

def intro(texte):
    st.markdown(f'<div class="tab-intro">{texte}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ÉTAT DE SESSION — segments dynamiques
# ─────────────────────────────────────────────
if "extra_segments" not in st.session_state:
    st.session_state.extra_segments = []

# ─────────────────────────────────────────────
#  EN-TÊTE
# ─────────────────────────────────────────────
st.markdown("# ✝️ La Voie de l'Abondance et de la Puissance")
st.markdown("<p style='text-align:center;color:#666;font-size:0.85rem;'>Enseignement Biblique — Résumé structuré</p>", unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────────
#  NOMS DES ONGLETS
# ─────────────────────────────────────────────
tab_labels = [
    "1·Abondance", "2·Norme", "3·Sûreté",
    "4·Sujet", "5·Clés", "6·Commencement",
    "7·Abîme", "8·Idiome", "9·Fondements"
]
for i, seg in enumerate(st.session_state.extra_segments):
    tab_labels.append(f"{10+i}·{seg['title'][:8]}")
tab_labels.append("➕ Nouveau")

tabs = st.tabs(tab_labels)

# ══════════════════════════════════════════════
#  SEGMENT 1 — LA VOIE DE L'ABONDANCE
# ══════════════════════════════════════════════
with tabs[0]:
    intro(
        "La <b>voie</b> fait allusion à un chemin à suivre. Il y a une destination à atteindre : <b>DIEU</b>. "
        "L'abondance, c'est ce que Dieu désire pour son peuple — physiquement, mentalement et spirituellement. "
        "La puissance, c'est la force et la capacité de manifester les œuvres de Dieu dans notre vie quotidienne."
    )

    section("Jésus-Christ : La Voie, la Vérité et la Vie")
    verse("Jean 14:6", "Jésus lui dit : Je suis le chemin, la vérité et la vie. Nul ne vient au Père que par moi.")
    comment(
        "Jésus se désigne lui-même comme <b>la voie unique</b> vers Dieu. Ce n'est pas une philosophie parmi d'autres, "
        "mais une déclaration absolue d'identité divine. Suivre la voie de Jésus-Christ, c'est s'engager sur le chemin "
        "qui mène à l'abondance véritable et à la présence de Dieu."
    )
    verse("Jean 4:34", "Jésus leur dit : Ma nourriture est de faire la volonté de celui qui m'a envoyé et d'accomplir son œuvre.")
    verse("Jean 5:30", "Je ne puis rien faire de moi-même... je cherche non ma volonté, mais la volonté de celui qui m'a envoyé.")
    verse("Jean 6:38", "Car je suis descendu du ciel pour faire non ma volonté, mais la volonté de celui qui m'a envoyé.")
    verse("Jean 8:29", "Celui qui m'a envoyé est avec moi ; il ne m'a pas laissé seul, parce que je fais toujours ce qui lui est agréable.")
    verse("Jean 10:30", "Moi et le Père, nous sommes un.")
    verse("Jean 12:49-50", "Car je n'ai pas parlé de moi-même ; mais le Père qui m'a envoyé m'a lui-même prescrit ce que je dois dire et annoncer.")
    comment(
        "Ces versets révèlent la parfaite soumission de Jésus à la volonté du Père. <b>La voie de l'abondance passe par l'obéissance</b> "
        "à la Parole de Dieu, tout comme Jésus ne cherchait pas sa propre volonté mais celle du Père. "
        "Si Jésus lui-même, Fils de Dieu, a choisi l'obéissance totale, combien plus devons-nous nous aligner sur Sa Parole !"
    )
    key_point("La puissance de Dieu se manifeste lorsque nous marchons dans la volonté du Père, comme Jésus en a été l'exemple parfait.")

    section("Choisir une Norme de la Vérité")
    comment(
        "Laisser la Parole <b>s'interpréter elle-même</b> est le principe fondamental pour connaître le vrai dessein de Dieu. "
        "La vérité demeure vérité — qu'on soit d'accord avec elle ou non, qu'on la croie ou non."
    )
    verse("Jean 17:17", "Sanctifie-les par ta vérité : ta parole est la vérité.")
    verse("Deutéronome 30:14-15", "La parole est tout près de toi, dans ta bouche et dans ton cœur... Vois, je mets aujourd'hui devant toi la vie et le bien, la mort et le mal.")
    verse("Deutéronome 30:16", "Je te commande aujourd'hui d'aimer l'Éternel, ton Dieu, de marcher dans ses voies et d'observer ses commandements...")
    verse("Deutéronome 30:19-20", "J'en prends à témoin aujourd'hui le ciel et la terre : j'ai mis devant toi la vie et la mort, la bénédiction et la malédiction. Choisis la vie, afin que tu vives...")
    comment(
        "Dieu n'impose pas : <b>Il propose et laisse le choix</b>. La voie de l'abondance est un chemin ouvert que chaque croyant "
        "doit délibérément choisir. La vérité divine n'est pas conditionnée par notre adhésion — elle est éternelle et immuable."
    )

    section("Nous Aimons Dieu Parce qu'Il Nous a Aimés le Premier")
    verse("Agée 1:5", "C'est pourquoi ainsi parle l'Éternel des armées : Considérez attentivement vos voies.")
    verse("Matthieu 22:29", "Jésus leur répondit : Vous êtes dans l'erreur, parce que vous ne connaissez pas les Écritures, ni la puissance de Dieu.")
    verse("Jean 8:31-32", "Si vous demeurez dans ma parole, vous êtes vraiment mes disciples ; vous connaîtrez la vérité, et la vérité vous affranchira.")
    comment(
        "C'est notre <b>libre arbitre</b> d'obéir à la Parole et de jouir de l'abondance que Dieu a préparée pour nous. "
        "Dieu nous aime en premier — ce n'est pas notre mérite qui attire sa grâce, mais sa nature même d'amour. "
        "En réponse à cet amour, nous choisissons librement de marcher dans ses voies et d'en recevoir tous les bénéfices."
    )
    key_point("L'abondance de Dieu n'est pas réservée à l'élite spirituelle — elle appartient à quiconque choisit de croire et d'obéir à Sa Parole.")

# ══════════════════════════════════════════════
#  SEGMENT 2 — LA PAROLE DE DIEU EST LA NORME
# ══════════════════════════════════════════════
with tabs[1]:
    intro(
        "La Parole de Dieu est l'unique norme absolue de vérité, de foi et de conduite. "
        "Face aux contrefaçons et aux doctrines mensongères, elle demeure l'étalon intouchable "
        "par lequel toute doctrine doit être évaluée."
    )

    section("Les Objectifs du Voleur vs La Mission de Jésus")
    verse("Jean 10:10", "Le voleur ne vient que pour dérober, égorger et détruire. Moi, je suis venu afin que les brebis aient la vie, et qu'elles soient dans l'abondance.")
    comment(
        "Ce verset établit un contraste saisissant. <b>Le voleur (l'adversaire)</b> a trois objectifs précis : "
        "dérober (prendre ce qui ne lui appartient pas), égorger (détruire la vie), détruire (anéantir tout potentiel). "
        "À l'opposé, <b>Jésus vient pour donner la vie en abondance</b> — une vie pleine, entière, débordante. "
        "La norme de Dieu nous protège des stratégies du voleur."
    )
    verse("1 Jean 3:7-8", "Que personne ne vous séduise. Celui qui pratique la justice est juste... Celui qui pèche est du diable, car le diable pèche dès le commencement.")
    verse("Actes 10:38", "Comment Dieu a oint du Saint-Esprit et de puissance Jésus de Nazareth, qui allait de lieu en lieu faisant du bien et guérissant tous ceux qui étaient sous l'emprise du diable, car Dieu était avec lui.")
    comment(
        "Jésus a détruit les œuvres du diable partout où il passait. Cette même puissance est disponible pour le croyant "
        "qui s'appuie sur la Parole comme norme. <b>Faire du bien est la marque de Dieu ; détruire est la marque de l'adversaire.</b>"
    )
    key_point("Toute doctrine qui affaiblit, décourage ou ôte la vie au croyant ne vient pas de Dieu. La Parole de Dieu toujours édifie, libère et donne la vie.")

    section("L'Autorité et l'Intégrité de la Parole Révélée")
    verse("2 Pierre 1:20", "Sachant tout d'abord vous-mêmes qu'aucune prophétie de l'Écriture ne peut être un objet d'interprétation particulière.")
    verse("Genèse 3:15", "Je mettrai inimitié entre toi et la femme, entre ta postérité et sa postérité : celle-ci t'écrasera la tête, et tu lui blesseras le talon.")
    comment("Dieu annonce dès la Genèse la victoire finale du Christ sur le diable — <b>la Parole porte en elle sa propre cohérence prophétique</b> à travers toute l'histoire du salut.")
    verse("Ésaïe 9:6", "Car un enfant nous est né, un fils nous est donné, et la domination reposera sur son épaule...")
    verse("Hébreux 6:18", "Afin que, par deux choses immuables dans lesquelles il est impossible que Dieu mente, nous trouvions un puissant encouragement...")
    verse("Nombres 23:19", "Dieu n'est pas un homme pour mentir, ni fils d'homme pour se repentir. Ce qu'il dit, ne le fera-t-il pas ? Ce qu'il déclare, ne l'accomplira-t-il pas ?")
    verse("Malachie 3:6", "Car moi, l'Éternel, je ne change pas.")
    comment(
        "<b>L'autorité de la Parole repose sur la nature immuable de Dieu lui-même.</b> Dieu ne peut pas mentir. "
        "Ce qu'il a déclaré est accompli dans les faits — son intégrité est le fondement de notre confiance absolue en Sa Parole."
    )

    section("Nous Pouvons Avoir Confiance en Dieu et en Sa Parole")
    verse("2 Pierre 1:21", "Car ce n'est pas par une volonté humaine qu'une prophétie a jamais été apportée, mais c'est poussés par le Saint-Esprit que des hommes ont parlé de la part de Dieu.")
    verse("Romains 16:25-26", "...selon la révélation du mystère gardé caché depuis des temps éternels, mais manifesté maintenant et porté par les Écritures des prophètes à la connaissance de toutes les nations...")
    verse("Éphésiens 3:3-4", "...c'est par révélation que ce mystère m'a été fait connaître... En le lisant, vous pouvez comprendre l'intelligence que j'ai du mystère de Christ.")
    verse("Galates 1:11-12", "Je vous déclare, frères, que l'Évangile qui a été annoncé par moi n'est pas de l'homme ; car je ne l'ai reçu ni appris d'aucun homme, mais par une révélation de Jésus-Christ.")
    verse("Deutéronome 29:29", "Les choses cachées appartiennent à l'Éternel notre Dieu ; mais les choses révélées nous appartiennent à jamais, à nous et à nos enfants.")
    comment(
        "La Parole de Dieu n'est pas une invention humaine — elle est <b>révélée par Dieu lui-même à des hommes inspirés par le Saint-Esprit</b>. "
        "Cette origine divine garantit son autorité et son intégrité absolues. Nous pouvons lui faire totalement confiance."
    )

    section("La Parole de Dieu : Notre Norme Absolue")
    verse("Hébreux 4:12", "Car la parole de Dieu est vivante et efficace, plus tranchante qu'une épée quelconque à deux tranchants, pénétrante jusqu'à diviser âme et esprit...")
    verse("Actes 8:29-31", "L'Esprit dit à Philippe : Avance et approche-toi de ce char. Philippe accourut et entendit l'Éthiopien qui lisait le prophète Ésaïe...")
    comment(
        "La Parole de Dieu est vivante — elle agit, pénètre, discerne. <b>Personne ne va au-delà de ce qu'on lui a enseigné.</b> "
        "C'est pourquoi l'enseignement fidèle de la Parole est crucial : elle fixe le niveau de notre marche avec Dieu. "
        "Plus nous connaissons la Parole, plus nous marchons dans la plénitude de ce que Dieu a prévu pour nous."
    )
    key_point("La Parole de Dieu est notre norme — pas la tradition, pas l'émotion, pas l'expérience humaine. Elle seule juge et éclaire toutes choses.")

# ══════════════════════════════════════════════
#  SEGMENT 3 — LA SÛRETÉ DE NOS JOURS
# ══════════════════════════════════════════════
with tabs[2]:
    intro(
        "Dans un monde instable, la Parole de Dieu est notre ancre, notre sécurité. "
        "Nous pouvons apprendre à retenir la Parole dans notre intelligence, à lui faire confiance, "
        "à y croire et à reconnaître son intégrité et son authenticité absolues."
    )

    section("Retenir la Parole dans Notre Intelligence")
    verse("2 Pierre 1:20-21", "Sachant tout d'abord vous-mêmes qu'aucune prophétie de l'Écriture ne peut être un objet d'interprétation particulière... des hommes ont parlé de la part de Dieu, poussés par le Saint-Esprit.")
    comment(
        "La Parole de Dieu n'est pas une interprétation subjective — elle a une signification précise voulue par son Auteur. "
        "<b>Retenir la Parole dans son intelligence</b>, c'est la lire, l'étudier, la méditer jusqu'à ce qu'elle devienne une certitude intérieure. "
        "C'est ce processus qui produit la foi agissante et la sûreté dans notre marche quotidienne."
    )

    section("La Sincérité n'est pas une Garantie pour la Vérité")
    comment(
        "On peut être sincèrement dans l'erreur. La sincérité est une qualité du cœur, mais elle ne remplace pas "
        "la connaissance exacte de la Vérité. <b>Seule la Parole de Dieu est la norme absolue</b>, au-delà de nos sentiments, "
        "de nos traditions religieuses ou de nos convictions personnelles."
    )
    verse("2 Timothée 3:16", "Toute Écriture est inspirée de Dieu, et utile pour enseigner, pour convaincre, pour corriger, pour instruire dans la justice.")
    verse("Éphésiens 3:3", "C'est par révélation que ce mystère m'a été fait connaître, comme je l'ai déjà écrit en peu de mots.")
    verse("Romains 16:25", "...selon la révélation du mystère gardé caché depuis des temps éternels.")
    verse("Galates 1:11-12", "L'Évangile qui a été annoncé par moi n'est pas de l'homme ; je ne l'ai reçu ni appris d'aucun homme, mais par une révélation de Jésus-Christ.")
    verse("Matthieu 5:18", "Car, je vous le dis en vérité, tant que le ciel et la terre ne passeront point, il ne disparaîtra pas de la loi un seul iota ou un seul trait de lettre...")
    verse("Matthieu 4:4", "Il est écrit : L'homme ne vivra pas de pain seulement, mais de toute parole qui sort de la bouche de Dieu.")
    comment(
        "Jésus lui-même, face aux tentations du diable, répondit par la Parole de Dieu. <b>La Parole est l'arme offensive</b> "
        "qui garantit notre sûreté. Si la sincérité suffisait, Jésus n'aurait pas eu besoin de citer les Écritures."
    )
    key_point("Soyons sincères ET ancrés dans la Parole. La sincérité sans la vérité peut nous conduire loin de Dieu avec un cœur pur mais des pas égarés.")

    section("Ce que Dieu Dit à Propos de Sa Puissance")
    verse("Psaumes 12:7", "Toi, Éternel, tu les garderas, tu les préserveras pour toujours de cette génération.")
    verse("Psaumes 119:105", "Ta parole est une lampe à mes pieds et une lumière sur mon sentier.")
    verse("Psaumes 119:160", "Le fondement de ta parole est la vérité, et toutes les ordonnances de ta justice subsistent éternellement.")
    verse("Ésaïe 33:5-6", "L'Éternel est élevé, car il demeure en haut ; il a rempli Sion de droiture et de justice. Il sera la sécurité de tes temps...")
    verse("Exode 31:18", "Quand il eut achevé de parler avec Moïse sur la montagne du Sinaï, il lui donna les deux tables du témoignage — des tables de pierre écrites du doigt de Dieu.")
    comment(
        "La puissance de la Parole vient de son Auteur divin. <b>Elle est lumière, fondement, sécurité.</b> "
        "Dieu lui-même a écrit de son doigt les premières tables de la loi — signifiant que sa Parole porte l'empreinte directe de sa volonté. "
        "Marcher selon cette Parole, c'est marcher sous la protection directe de Dieu."
    )
    key_point("La Parole de Dieu est la sûreté de nos jours — dans les temps de crise, d'incertitude ou d'épreuve, elle est notre lampe et notre rocher.")

# ══════════════════════════════════════════════
#  SEGMENT 4 — LE SUJET DE TOUTE LA PAROLE
# ══════════════════════════════════════════════
with tabs[3]:
    intro(
        "Toute la Parole de Dieu a un sujet central : <b>Jésus-Christ</b>. "
        "De la Genèse à l'Apocalypse, chaque texte, chaque prophétie, chaque type et ombre pointent vers lui. "
        "C'est lui le passe-partout à toute interprétation juste de la Parole."
    )

    section("Jésus-Christ : Centre de toute la Parole")
    verse("Luc 2:51-52", "Il descendit avec eux et vint à Nazareth, et il leur était soumis... Et Jésus croissait en sagesse, en stature, et en grâce devant Dieu et devant les hommes.")
    verse("Matthieu 4:1-11", "Alors Jésus fut emmené par l'Esprit dans le désert, pour être tenté par le diable... Il est écrit... Il est encore écrit... Car il est écrit...")
    comment(
        "Jésus grandit dans la Parole et répondit à chaque tentation par la Parole écrite. "
        "<b>Il est lui-même le modèle de l'ouvrier de la Parole</b> — il la connaissait, la méditait et la vivait. "
        "Sa victoire dans le désert démontre que la connaissance précise de la Parole écrit notre victoire à l'avance."
    )

    section("Jésus-Christ : Le Passe-Partout à l'Interprétation")
    verse("Jean 1:45", "Philippe rencontra Nathanaël et lui dit : Nous avons trouvé celui dont Moïse a écrit dans la loi, et dont les prophètes ont aussi écrit, Jésus de Nazareth...")
    verse("Luc 24:44-45", "Il leur dit : C'est là ce que je vous disais lorsque j'étais encore avec vous, qu'il fallait que s'accomplît tout ce qui est écrit de moi dans la loi de Moïse, dans les prophètes et dans les psaumes. Alors il leur ouvrit l'intelligence pour comprendre les Écritures.")
    comment(
        "Jésus lui-même a divisé la Parole en <b>trois catégories</b> : la Loi, les Prophètes et les Psaumes. "
        "Et il leur a déclaré que tout cela parlait de lui. L'intelligence des Écritures vient de Jésus-Christ. "
        "Sans lui comme clé de lecture, la Parole reste un texte fermé."
    )
    key_point("Lire la Bible sans voir Jésus-Christ au centre de chaque texte, c'est passer à côté du message essentiel. Il est le sujet de toute la Parole.")

    section("Se Présenter Devant Dieu comme un Ouvrier Éprouvé")
    verse("2 Timothée 2:15", "Efforce-toi de te présenter devant Dieu comme un homme éprouvé, un ouvrier qui n'a pas à rougir, qui dispense droitement la parole de la vérité.")
    verse("1 Thessaloniciens 2:4", "Mais, comme Dieu nous a jugés dignes de nous confier l'Évangile, nous parlons de la sorte, pour plaire non aux hommes, mais à Dieu...")
    verse("Psaumes 138:2", "Je me prosterne vers ton saint temple, et je célèbre ton nom... car tu as magnifié ta parole au-dessus de tout ton nom.")
    verse("Psaumes 119:89", "Éternellement, ô Éternel ! ta parole subsiste dans les cieux.")
    comment(
        "Dieu a <b>magnifié sa Parole au-dessus de son nom</b>. C'est une déclaration extraordinaire. "
        "Cela signifie que la Parole révélée de Dieu est l'expression la plus haute de sa volonté et de sa gloire. "
        "L'ouvrier de la Parole est celui qui prend au sérieux cette réalité et traite la Parole avec le respect qu'elle mérite."
    )

    section("La Parole de Dieu est la Volonté de Dieu")
    verse("Ésaïe 55:8-11", "Car mes pensées ne sont pas vos pensées, et vos voies ne sont pas mes voies... Ainsi en est-il de ma parole, qui sort de ma bouche : elle ne retourne pas à moi sans effet...")
    verse("Colossiens 3:16", "Que la parole de Christ habite parmi vous abondamment...")
    verse("Actes 17:11", "Ces Juifs avaient des sentiments plus nobles que ceux de Thessalonique ; ils reçurent la parole avec beaucoup d'empressement, et ils examinaient chaque jour les Écritures...")
    verse("Jean 5:39", "Vous sondez les Écritures, parce que vous pensez avoir en elles la vie éternelle : ce sont elles qui rendent témoignage de moi.")
    comment(
        "La Parole n'est pas un texte mort — elle produit des effets, elle accomplit la volonté de Dieu sur la terre. "
        "<b>Lire, écouter, étudier la Parole avec diligence</b> est la plus grande clé pour l'ouvrier de Dieu. "
        "Les Béréens en sont le modèle : ils examinaient les Écritures chaque jour."
    )

    section("Lire la Parole : La Plus Grande Clé")
    verse("Exode 24:7", "Il prit le livre de l'alliance et le lut en présence du peuple...")
    verse("Deutéronome 17:18-20", "Quand il sera assis sur son trône royal, il écrira pour lui sur un livre une copie de cette loi... il la lira tous les jours de sa vie...")
    verse("Néhémie 8:8", "Ils lurent dans le livre de la loi de Dieu distinctement, donnant le sens, et l'on comprit ce qui était lu.")
    verse("Éphésiens 3:3-4", "C'est par révélation que ce mystère m'a été fait connaître... En le lisant, vous pouvez comprendre l'intelligence que j'ai du mystère de Christ.")
    comment(
        "La lecture régulière et attentive de la Parole est le premier acte de l'ouvrier de Dieu. "
        "<b>La plus grande clé pour être un ouvrier de la Parole est d'apprendre à aimer lire la Bible.</b> "
        "Continuer à lire la Parole de Dieu et à en faire nos délices — car elle est la sûreté de nos jours."
    )
    key_point("La Parole de Dieu est la volonté de Dieu — connaître l'une, c'est marcher dans l'autre. L'étude fidèle de la Parole est notre plus grand investissement spirituel.")

# ══════════════════════════════════════════════
#  SEGMENT 5 — LES CLÉS À L'INTERPRÉTATION
# ══════════════════════════════════════════════
with tabs[4]:
    intro(
        "La Parole de Dieu s'interprète elle-même. Ce principe fondamental nous protège contre les dérives doctrinales "
        "et les interprétations personnelles. Il existe des règles d'herméneutique que tout croyant peut apprendre "
        "pour comprendre correctement la Parole."
    )

    section("Principe Fondamental : L'Écriture s'interprète elle-même")
    verse("2 Pierre 1:20", "Sachant tout d'abord vous-mêmes qu'aucune prophétie de l'Écriture ne peut être un objet d'interprétation particulière.")
    comment(
        "Ce verset pose la règle d'or de l'interprétation biblique : <b>aucun texte ne s'interprète de manière isolée ou arbitraire</b>. "
        "La signification d'un verset se trouve dans le verset lui-même, dans son contexte immédiat, "
        "et dans l'ensemble de la Parole. L'Écriture éclaire l'Écriture."
    )
    key_point("Trois niveaux d'interprétation : dans le verset lui-même → dans le contexte du passage → dans l'ensemble de la Parole.")

    section("Vérités Bibliques Auxquelles Nous Devons Adhérer")
    comment(
        "Pour interpréter correctement la Parole, il faut toujours identifier :"
        "<br>• <b>La période de temps</b> à laquelle le texte est adressé"
        "<br>• <b>Le destinataire</b> du message (à qui est-il écrit ?)"
        "<br>• <b>Le contexte culturel et linguistique</b> de l'époque"
        "<br>• Le verset difficile doit être compris à la lumière des versets clairs."
    )
    verse("1 Timothée 3:16", "Toute Écriture est inspirée de Dieu, et utile pour enseigner, pour convaincre, pour corriger, pour instruire dans la justice.")

    section("L'Interprétation et l'Application : À Qui est-ce Adressé ?")
    verse("1 Corinthiens 10:31-32", "Soit donc que vous mangiez, soit que vous buviez, soit que vous fassiez quelque autre chose, faites tout pour la gloire de Dieu... ne soyez en scandale ni aux Juifs, ni aux Grecs, ni à l'Église de Dieu.")
    comment(
        "La Parole de Dieu s'adresse à trois groupes principaux : les Juifs, les Nations (Grecs), et l'Église. "
        "<b>Toute interprétation correcte tient compte du destinataire</b>. "
        "Ce qui est adressé à Israël sous la Loi ne s'applique pas nécessairement de la même façon au croyant de l'Église d'aujourd'hui."
    )

    section("Toute la Parole est Utile — mais pas Toute la Parole nous est Directement Adressée")
    verse("Romains 15:4", "Car tout ce qui a été écrit d'avance l'a été pour notre instruction, afin que, par la patience et par la consolation que donnent les Écritures, nous possédions l'espérance.")
    verse("Jacques 5:10", "Prenez, mes frères, pour modèles de souffrance et de patience les prophètes qui ont parlé au nom du Seigneur.")
    comment(
        "Voici l'équilibre parfait : <b>toute la Parole est utile</b> pour instruire, convaincre, corriger. "
        "Mais certaines parties de la Parole ne nous sont pas directement adressées dans cette administration du temps de grâce. "
        "Par exemple, les lois cérémonielles données à Israël ou certaines prophéties spécifiques à des nations particulières. "
        "<b>Nous apprenons de tout — mais nous appliquons en discernant à qui c'est adressé.</b>"
    )
    key_point("Ne pas faire cette distinction conduit à la confusion doctrinale. Diviser droitement la Parole, c'est savoir ce qui est pour nous, ce qui est pour nous apprendre, et ce qui est pour notre instruction.")

# ══════════════════════════════════════════════
#  SEGMENT 6 — AU COMMENCEMENT
# ══════════════════════════════════════════════
with tabs[5]:
    intro(
        "La Parole de Dieu n'a jamais été écrite pour l'incrédule. Elle est écrite pour ceux qui veulent aimer Dieu, "
        "connaître la vérité et être humbles et disciplinés selon cette vérité. "
        "Comprendre les fondements de la création nous ancre dans la certitude de qui est Dieu."
    )

    section("La Parole : Notre Norme de Croyance et d'Action")
    verse("Hébreux 11:3", "C'est par la foi que nous comprenons que le monde a été formé par la parole de Dieu, en sorte que ce qu'on voit n'a pas été fait de ce qui est visible.")
    verse("2 Pierre 1:3", "Sa divine puissance nous a donné tout ce qui contribue à la vie et à la piété, par la connaissance de celui qui nous a appelés par sa propre gloire et par sa vertu.")
    verse("Genèse 1:1", "Au commencement, Dieu créa les cieux et la terre.")
    comment(
        "Ce premier verset de la Bible pose les fondements de tout : <b>Dieu est l'origine de tout ce qui existe</b>. "
        "Croire en ce commencement, c'est croire en la souveraineté absolue de Dieu sur la création. "
        "La foi qui comprend la création comprend aussi que le même Dieu créateur est capable d'agir dans notre vie quotidienne."
    )

    section("Jésus-Christ dans la Présence de Dieu au Commencement")
    verse("Matthieu 1:18", "Voici comment arriva la naissance de Jésus-Christ. Marie, sa mère, avait été fiancée à Joseph ; et, avant qu'ils eussent habité ensemble, elle se trouva enceinte par le Saint-Esprit.")
    verse("Jean 1:1-4", "Au commencement était la Parole, et la Parole était avec Dieu, et la Parole était Dieu. Elle était au commencement avec Dieu. Toutes choses ont été faites par elle... En elle était la vie.")
    comment(
        "Jésus-Christ — la Parole — était présent <b>dès le commencement</b>. Il n'est pas une création de Dieu "
        "mais l'agent de toute création. Cette vérité est capitale : "
        "celui qui nous sauve et nous donne l'abondance est le même qui a créé l'univers. "
        "<b>Dieu est l'Initiateur du salut ; Jésus-Christ en est l'Agent et le Moyen.</b>"
    )

    section("La Terre Devint Informe et Vide")
    verse("Genèse 1:1-2", "Au commencement, Dieu créa les cieux et la terre. La terre était informe et vide : il y avait des ténèbres à la surface de l'abîme...")
    verse("Ézéchiel 28:12-17", "...Tu étais le sceau de la perfection, plein de sagesse, accompli en beauté... Tu étais parfait dans tes voies, depuis le jour où tu fus créé, jusqu'à ce que l'iniquité ait été trouvée en toi.")
    verse("Jérémie 4:23", "Je regardai la terre, et voici, elle était informe et vide ; les cieux, et leur lumière avait disparu.")
    comment(
        "La terre que nous décrivons en Genèse 1:2 n'est pas la création originelle de Dieu — elle est le résultat "
        "de la chute de l'adversaire (Lucifer / Satan). <b>Ézéchiel 28 nous révèle qu'il était parfait jusqu'au jour "
        "où l'iniquité fut trouvée en lui</b>. Son péché et sa rébellion ont conduit à la dévastation décrite en Genèse 1:2. "
        "Jérémie 4:23 confirme cette désolation — c'est l'œuvre de la rébellion, non de Dieu."
    )
    key_point("Dieu ne crée pas le chaos — il le remédie. Chaque fois que l'adversaire dévaste, Dieu restaure et remet en ordre.")

    verse("Jean 1:5", "La lumière luit dans les ténèbres, et les ténèbres ne l'ont point reçue.")
    comment(
        "Face aux ténèbres qui couvraient l'abîme, Dieu dit : 'Que la lumière soit !' — <b>Jésus est cette lumière</b> "
        "qui brille dans toute dévastation. Dans notre vie aussi, là où l'adversaire a semé le désordre, "
        "la Parole de Dieu apporte lumière, ordre et restauration."
    )

# ══════════════════════════════════════════════
#  SEGMENT 7 — LA SURFACE DE L'ABÎME
# ══════════════════════════════════════════════
with tabs[6]:
    intro(
        "Genèse 1 nous révèle des réalités cosmiques profondes sur la structure de la création. "
        "Comprendre l'abîme, les cieux, et les terres successifs nous permet de saisir "
        "l'ampleur du plan de Dieu à travers l'histoire de la création et de la rédemption."
    )

    section("Qu'est-ce que la Surface de l'Abîme et l'Étendue ?")
    verse("Genèse 1:2", "La terre était informe et vide ; il y avait des ténèbres à la surface de l'abîme, et l'Esprit de Dieu se mouvait au-dessus des eaux.")
    verse("1 Jean 1:5", "Dieu est lumière, et il n'y a point en lui de ténèbres.")
    comment(
        "L'abîme représente le chaos et les ténèbres résultant de la chute de Satan. "
        "<b>L'Esprit de Dieu planait au-dessus de ces eaux</b> — signe que Dieu n'avait pas abandonné sa création "
        "malgré la dévastation. Sa puissance créatrice était prête à intervenir. "
        "Dieu est lumière : là où il intervient, les ténèbres fuient."
    )
    verse("Genèse 1:2-5", "Dieu dit : Que la lumière soit ! Et la lumière fut... Il sépara la lumière des ténèbres.")
    verse("Genèse 1:14-19", "Dieu dit : Que des luminaires se forment dans l'étendue des cieux, pour séparer le jour et la nuit...")
    comment(
        "Dieu instaure un <b>ordre cosmique parfait</b> : il sépare, il nomme, il organise. "
        "Les luminaires sont des signes pour les saisons, les jours et les années — "
        "Dieu est un Dieu d'ordre et de précision, pas de confusion."
    )

    section("Les Trois Cieux et les Trois Terres")
    verse("Genèse 1:1", "Au commencement, Dieu créa les cieux et la terre. [1ère terre]")
    verse("Genèse 1:2", "La terre était informe et vide... [2ème état de la terre — dévastation par Satan]")
    verse("Apocalypse 21:1", "Je vis un nouveau ciel et une nouvelle terre ; car le premier ciel et la première terre avaient disparu... [3ème terre — à venir]")
    verse("2 Pierre 3:5-6", "...Par la parole de Dieu, des cieux existaient et une terre... le monde d'alors périt submergé par l'eau.")
    comment(
        "La Parole révèle trois états successifs de la terre :"
        "<br><b>1. La première création</b> — parfaite, créée par Dieu (Genèse 1:1)"
        "<br><b>2. La dévastation</b> — suite à la chute de Satan (Genèse 1:2)"
        "<br><b>3. La nouvelle création</b> — à venir, parfaite et éternelle (Apocalypse 21:1)"
        "<br>Nous vivons actuellement dans la période de restauration entre la 2ème et la 3ème création."
    )

    section("Dieu Prépare et Restaure la Terre")
    verse("Genèse 6:1", "Et il arriva que lorsque les hommes commencèrent à se multiplier sur la face de la terre...")
    verse("Genèse 4:16-17", "Caïn s'éloigna de la face de l'Éternel et habita dans le pays de Nod, à l'orient d'Éden. Caïn connut sa femme...")
    comment(
        "La Parole nous révèle que la masse terrestre unique de Genèse s'est transformée. "
        "<b>Événements clés ayant précédé la division des continents :</b>"
        "<br>• Le déluge au temps de Noé — la terre était encore une seule masse, ce qui explique l'inondation totale"
        "<br>• La dispersion à Babel — les peuples dispersés sur la face d'une terre encore unifiée"
        "<br>• La division au temps de Péleg (Genèse 10:25) — 'En son temps la terre fut divisée'"
        "<br>Ces événements majeurs expliquent la géographie telle que nous la connaissons aujourd'hui."
    )
    key_point("Dieu est souverain sur l'histoire de la création. Chaque changement géographique ou cosmique s'inscrit dans son plan et est révélé dans sa Parole.")

# ══════════════════════════════════════════════
#  SEGMENT 8 — L'IDIOME DE PERMISSION
# ══════════════════════════════════════════════
with tabs[7]:
    intro(
        "Un idiome est un usage de mots particulier à une langue ou à une culture, dont les mots ne doivent pas être pris "
        "dans leur sens littéral. L'idiome hébreu de permission est crucial pour comprendre la Parole "
        "et ne jamais attribuer le mal à Dieu."
    )

    section("Comprendre l'Idiome Hébreu de Permission")
    verse("Exode 10:20", "Mais l'Éternel endurcit le cœur de Pharaon, et Pharaon ne laissa pas partir les enfants d'Israël.")
    comment(
        "En lecture littérale, ce verset semble dire que Dieu lui-même a endurci le cœur de Pharaon. "
        "Mais l'idiome hébreu de permission nous éclaire : <b>la forme causative en hébreu exprime souvent une permission</b>, "
        "non une action directe. Le sens réel est : 'Dieu permit que le cœur de Pharaon soit endurci.' "
        "Pharaon a lui-même fait le choix de s'endurcir — Dieu a simplement respecté son libre arbitre."
    )
    key_point("Reconnaître l'idiome hébreu de permission nous permet de diviser droitement la Parole et de ne jamais attribuer le mal, la maladie ou la destruction à Dieu.")

    section("Genèse 6 et le Déluge — Application de l'Idiome")
    verse("Genèse 6:8-13", "Mais Noé trouva grâce aux yeux de l'Éternel... La terre était corrompue devant Dieu, la terre était pleine de violence. Dieu vit la terre, et voici qu'elle était corrompue...")
    comment(
        "Dieu ne détruit pas pour le plaisir. En Genèse 6, la violence et la corruption viennent des hommes et de l'adversaire. "
        "<b>Dieu 'permit' le déluge</b> comme conséquence directe des choix humains et comme moyen de préserver "
        "la lignée de Noé par laquelle viendrait le Sauveur. Son plan de salut guidait chaque décision."
    )

    section("Le Plan de Dieu pour la Création")
    verse("Genèse 1:9-13", "Dieu dit : Que les eaux qui sont sous le ciel se rassemblent en un seul lieu... Et la terre produisit de la verdure...")
    verse("Genèse 1:14", "Dieu dit : Que des luminaires se forment dans l'étendue des cieux, pour séparer le jour et la nuit ; que ce soient des signes pour les saisons, pour les jours et pour les années.")
    comment(
        "Dieu est un Dieu de plan et d'ordre. La création n'est pas le fruit du hasard, "
        "mais d'une <b>intention précise et organisée</b>. Chaque élément créé a une fonction, une place, une signification. "
        "Ce même Dieu planificateur a un plan pour ta vie — un plan de bien, non de mal (Jérémie 29:11)."
    )

    section("L'Adversaire Dévaste — Dieu Restaure")
    verse("Genèse 1:24-25", "Dieu dit : Que la terre produise des animaux vivants selon leur espèce... Dieu vit que cela était bon.")
    verse("Matthieu 22:36-37", "Maître, quel est le plus grand commandement dans la loi ? Jésus lui répondit : Tu aimeras le Seigneur ton Dieu de tout ton cœur, de toute ton âme et de toute ta pensée.")
    comment(
        "Après que l'adversaire eut rendu la terre informe et vide, Dieu la remet méthodiquement en ordre — "
        "jour après jour, il restaure, sépare, nomme et bénit. <b>La raison d'être de l'univers est la terre. "
        "La raison d'être de la terre est l'homme. La raison d'être de l'homme est d'aimer Dieu, de l'adorer et de communier avec lui.</b>"
    )
    key_point("Dieu n'est jamais la source du mal, de la maladie ou de la destruction. Il est toujours celui qui restaure, guérit et remet en ordre. L'idiome de permission nous préserve de cette erreur doctrinale grave.")

# ══════════════════════════════════════════════
#  SEGMENT 9 — LES FONDEMENTS DE TOUTE VIE
# ══════════════════════════════════════════════
with tabs[8]:
    intro(
        "Genèse établit les fondements de toute vie humaine. L'homme est un être tripartite — corps, âme et esprit — "
        "créé à l'image de Dieu pour vivre en communion avec lui. "
        "Comprendre cette réalité est la clé pour vivre dans la plénitude du dessein de Dieu."
    )

    section("L'Homme : Corps, Âme et Esprit")
    verse("Genèse 1:26", "Dieu dit : Faisons l'homme à notre image, selon notre ressemblance...")
    verse("Jean 4:24", "Dieu est Esprit, et il faut que ceux qui l'adorent l'adorent en esprit et en vérité.")
    comment(
        "L'homme a été créé à l'<b>image de Dieu</b> — et Dieu est Esprit. "
        "Cela révèle que l'aspect le plus profond de l'homme n'est pas son corps physique, mais son esprit. "
        "Les trois dimensions de l'être humain : <br>"
        "• <b>Corps</b> : formé de la poussière de la terre (Genèse 2:7) <br>"
        "• <b>Âme</b> : le siège de la vie biologique, dans le sang (Lévitique 17:11) <br>"
        "• <b>Esprit</b> : créé par Dieu — la dimension qui communique avec Dieu (Genèse 1:28)"
    )
    verse("Proverbes 1:7", "La crainte de l'Éternel est le commencement de la sagesse ; les fous méprisent la sagesse et l'instruction.")

    section("Le Souffle de Vie")
    verse("Genèse 2:4-7", "...L'Éternel Dieu forma l'homme de la poussière de la terre, il souffla dans ses narines un souffle de vie et l'homme devint un être vivant.")
    verse("Ésaïe 42:5", "Ainsi parle Dieu, l'Éternel, qui a créé les cieux... qui a donné un souffle au peuple qui la parcourt et un esprit à ceux qui marchent sur elle.")
    verse("Luc 1:35", "L'ange lui répondit : Le Saint-Esprit viendra sur toi, et la puissance du Très-Haut te couvrira de son ombre...")
    comment(
        "Le souffle de vie que Dieu a insufflé dans l'homme est <b>un acte d'amour unique dans toute la création</b>. "
        "Aucune autre créature ne reçoit ce souffle divin direct. "
        "Cela confère à l'homme une dignité extraordinaire et une capacité unique de communion avec Dieu."
    )

    section("La Volonté de Dieu : Expérimenter le Bien, Éviter le Mal")
    verse("Genèse 2:8-9", "L'Éternel Dieu planta un jardin en Éden, à l'orient... L'Éternel Dieu fit pousser du sol des arbres de toute espèce, agréables à voir et bons à manger ; il y avait aussi au milieu du jardin l'arbre de la vie...")
    verse("Genèse 2:10-17", "Un fleuve sortait d'Éden pour arroser le jardin... L'Éternel Dieu donna cet ordre à l'homme : Tu pourras manger de tous les arbres du jardin ; mais tu ne mangeras pas de l'arbre de la connaissance du bien et du mal, car le jour où tu en mangeras, tu mourras.")
    comment(
        "Dieu avait clairement enseigné à l'homme la différence entre le bien et le mal. "
        "<b>Il voulait que l'homme expérimente le bien et évite le mal</b> — non par contrainte, "
        "mais par connaissance et par choix libre. Les bénédictions de Dieu appartiennent à ceux qui choisissent la vie "
        "en obéissant à sa Parole."
    )
    key_point("Dieu avait tout préparé pour que l'homme vive dans l'abondance. Le mal n'est pas venu de Dieu — il est venu d'un choix libre fait contre la Parole de Dieu.")

    section("La Compagne dans la Relation du Mariage")
    verse("Genèse 2:18", "L'Éternel Dieu dit : Il n'est pas bon que l'homme soit seul ; je lui ferai une aide semblable à lui.")
    verse("Genèse 2:21-24", "L'Éternel Dieu forma une femme de la côte qu'il avait prise de l'homme... C'est pourquoi l'homme quittera son père et sa mère, et s'attachera à sa femme, et ils deviendront une seule chair.")
    comment(
        "Le mariage n'est pas une invention humaine ou culturelle — <b>c'est une institution divine</b>, établie par Dieu "
        "dès les fondements de la création. L'homme et la femme sont deux êtres distincts mais complémentaires, "
        "créés pour vivre en unité et en abondance ensemble. "
        "Dieu a établi la vie aussi parfaitement que possible, donnant à l'homme et à la femme le choix, "
        "selon le libre arbitre, de vivre cette vie abondamment."
    )
    key_point("Les fondements de toute vie sont posés en Genèse : la création tripartite de l'homme, la relation avec Dieu, et la communauté dans le mariage. Revenir à ces fondements, c'est revenir à l'original de Dieu.")

# ══════════════════════════════════════════════
#  SEGMENTS DYNAMIQUES ajoutés par l'utilisateur
# ══════════════════════════════════════════════
for i, seg in enumerate(st.session_state.extra_segments):
    with tabs[9 + i]:
        intro(seg.get("intro", ""))
        if seg.get("contenu"):
            st.markdown(seg["contenu"])
        if seg.get("versets"):
            section("Versets du Segment")
            for v in seg["versets"]:
                st.markdown(f'<span class="ref-badge">📖 {v["ref"]}</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="verse-box">{v["texte"]}</div>', unsafe_allow_html=True)
        if seg.get("note"):
            key_point(seg["note"])

# ══════════════════════════════════════════════
#  ONGLET : AJOUTER UN NOUVEAU SEGMENT
# ══════════════════════════════════════════════
with tabs[-1]:
    st.markdown("## ➕ Ajouter un Nouveau Segment")
    st.markdown("Complète le formulaire ci-dessous pour ajouter un nouveau segment d'enseignement.")

    with st.form("nouveau_segment_form", clear_on_submit=True):
        titre = st.text_input("📌 Titre du Segment *", placeholder="Ex : LA GRÂCE ET LA FOI")
        intro_text = st.text_area("📝 Introduction du Segment", placeholder="Décris le sujet principal de ce segment...", height=100)
        contenu = st.text_area("📖 Contenu / Développement", placeholder="Explications, arguments bibliques, commentaires...", height=150)

        st.markdown("**Versets Bibliques (jusqu'à 5 versets)**")
        versets = []
        for j in range(1, 6):
            cols = st.columns([1, 2])
            with cols[0]:
                ref = st.text_input(f"Référence {j}", placeholder="Ex : Jean 3:16", key=f"ref_{j}")
            with cols[1]:
                texte = st.text_input(f"Texte {j}", placeholder="Texte du verset...", key=f"txt_{j}")
            if ref and texte:
                versets.append({"ref": ref, "texte": texte})

        note_cle = st.text_input("💡 Point Clé (facultatif)", placeholder="La vérité principale à retenir...")

        submitted = st.form_submit_button("✅ Ajouter le Segment", use_container_width=True)
        if submitted:
            if titre.strip():
                st.session_state.extra_segments.append({
                    "title": titre.strip(),
                    "intro": intro_text.strip(),
                    "contenu": contenu.strip(),
                    "versets": versets,
                    "note": note_cle.strip()
                })
                st.success(f"✅ Segment « {titre} » ajouté avec succès ! Rechargez la page pour voir le nouvel onglet.")
                st.balloons()
            else:
                st.error("⚠️ Le titre du segment est obligatoire.")

    if st.session_state.extra_segments:
        st.divider()
        st.markdown(f"**{len(st.session_state.extra_segments)} segment(s) ajouté(s) dans cette session :**")
        for seg in st.session_state.extra_segments:
            st.markdown(f"✅ {seg['title']}")
        if st.button("🗑️ Supprimer tous les segments ajoutés", type="secondary"):
            st.session_state.extra_segments = []
            st.rerun()

# ─────────────────────────────────────────────
#  PIED DE PAGE
# ─────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center;color:#aaa;font-size:0.78rem;'>"
    "✝️ Enseignement Biblique — Que la Parole de Dieu soit la sûreté de nos jours"
    "</p>",
    unsafe_allow_html=True
)
