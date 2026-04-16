import streamlit as st
import sqlite3
from datetime import datetime
try:
    import anthropic
    ANTHROPIC_OK = True
except ImportError:
    ANTHROPIC_OK = False

st.set_page_config(
    page_title="Bible Memory ✝️",
    page_icon="✝️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════
# CSS MOBILE-FIRST
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
:root{
    --gold:#C9A84C;--dark:#0A0A18;--mid:#12122A;
    --card:#181830;--accent:#E94560;--text:#F0E6D3;
    --green:#27AE60;--purple:#8E44AD;--blue:#2471A3;
    --border:#252545;--orange:#E67E22;
}
.stApp{background:var(--dark);color:var(--text);font-family:'Segoe UI',sans-serif;}
.app-header{text-align:center;padding:1.2rem 0 .5rem;
    background:linear-gradient(180deg,#181830 0%,transparent 100%);
    border-radius:0 0 20px 20px;margin-bottom:.8rem;}
.app-title{font-size:2rem;font-weight:900;color:var(--gold);
    text-shadow:0 0 30px rgba(201,168,76,.6);margin:0;}
.app-sub{color:#777;font-size:.78rem;margin:.3rem 0 0;letter-spacing:1px;}
.sec-title{font-size:1rem;font-weight:800;color:var(--gold);
    border-bottom:2px solid var(--gold);padding-bottom:.25rem;margin:1rem 0 .6rem;}
.sub-title{font-size:.88rem;font-weight:700;color:var(--orange);
    margin:.8rem 0 .3rem;text-transform:uppercase;letter-spacing:.5px;}
.card{background:var(--card);border-radius:14px;padding:.9rem;
    margin:.5rem 0;border:1px solid var(--border);}
.card-gold{border-left:4px solid var(--gold);}
.card-red{border-left:4px solid var(--accent);}
.card-green{border-left:4px solid var(--green);}
.card-purple{border-left:4px solid var(--purple);}
.card-blue{border-left:4px solid var(--blue);}
.card-orange{border-left:4px solid var(--orange);}
.verse-box{background:rgba(201,168,76,.06);border-radius:10px;
    padding:.8rem;font-size:.88rem;line-height:1.8;color:var(--text);
    border-left:3px solid var(--gold);margin:.4rem 0;}
.ref-tag{color:var(--gold);font-weight:800;font-size:.82rem;
    display:block;margin-bottom:.3rem;}
.story-box{background:rgba(142,68,173,.1);border-radius:10px;
    padding:.8rem;font-style:italic;font-size:.84rem;
    line-height:1.7;color:#ddd;border:1px solid rgba(142,68,173,.3);}
.mnemo-box{background:rgba(39,174,96,.1);border-radius:10px;
    padding:.8rem;font-size:.86rem;color:#2ECC71;
    border:1px solid rgba(39,174,96,.3);line-height:1.6;}
.ref-pill{display:inline-block;background:rgba(36,113,163,.2);color:#5DADE2;
    border:1px solid rgba(36,113,163,.4);border-radius:20px;
    font-size:.7rem;font-weight:700;padding:2px 8px;margin:2px;}
.seg-header{background:linear-gradient(135deg,#1a1a35,#0a0a18);
    border-radius:14px;padding:1rem;margin:.5rem 0;
    border:2px solid var(--gold);}
.seg-num-badge{background:var(--gold);color:#0A0A18;font-weight:900;
    border-radius:50%;width:36px;height:36px;display:inline-flex;
    align-items:center;justify-content:center;font-size:1rem;
    margin-right:.5rem;flex-shrink:0;}
.stat-card{background:var(--card);border-radius:12px;padding:.8rem;
    text-align:center;border:1px solid var(--border);}
.stat-num{font-size:1.8rem;font-weight:900;color:var(--gold);margin:0;}
.stat-lbl{font-size:.7rem;color:#888;margin:0;}
.stButton>button{background:linear-gradient(135deg,var(--gold),#8B6914);
    color:#0A0A18;font-weight:800;border:none;border-radius:10px;
    padding:.55rem;transition:all .2s;width:100%;}
.stButton>button:hover{opacity:.85;transform:translateY(-1px);}
.stTextInput input,.stTextArea textarea{
    background:var(--mid)!important;color:var(--text)!important;
    border:1px solid var(--border)!important;border-radius:8px!important;}
div[data-testid="stExpander"]{
    background:var(--card);border:1px solid var(--border);border-radius:12px;}
.point-item{padding:.4rem .6rem;margin:.2rem 0;
    background:rgba(255,255,255,.03);border-radius:8px;
    border-left:2px solid var(--orange);font-size:.84rem;color:#ddd;}
.key-truth{background:rgba(201,168,76,.08);border-radius:10px;
    padding:.7rem;border:1px solid rgba(201,168,76,.3);
    font-size:.85rem;color:#F0E6D3;line-height:1.6;margin:.4rem 0;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DONNÉES COMPLÈTES — 12 SEGMENTS (Louis Segond)
# ══════════════════════════════════════════════════════════
SEGMENTS = [
    {
        "num": 1,
        "titre": "La Voie de l'Abondance et de la Puissance",
        "couleur": "#C9A84C",
        "intro": (
            "La **voie** fait allusion à un chemin à suivre. Il y a une destination à atteindre : "
            "c'est **DIEU**. L'abondance, c'est ce que Dieu désire pour son peuple — "
            "prospérer physiquement, mentalement et spirituellement. "
            "La **puissance**, c'est la force et la capacité de réaliser les choses "
            "et de manifester la puissance de Dieu."
        ),
        "sections": [
            {
                "titre": "Jésus Christ : La Voie, la Vérité et la Vie",
                "contenu": "Jésus n'est pas seulement un guide — Il est le chemin lui-même. "
                    "Il ne pointe pas vers la vérité, Il EST la vérité. "
                    "Il ne donne pas la vie, Il EST la vie.",
                "versets": [
                    {
                        "ref": "Jean 14:6",
                        "texte": "Jésus lui dit : Je suis le chemin, la vérité, et la vie. "
                            "Nul ne vient au Père que par moi."
                    },
                    {
                        "ref": "Jean 4:34",
                        "texte": "Jésus leur dit : Ma nourriture est de faire la volonté de celui "
                            "qui m'a envoyé, et d'accomplir son oeuvre."
                    },
                    {
                        "ref": "Jean 6:38",
                        "texte": "Car je suis descendu du ciel pour faire, non ma volonté, "
                            "mais la volonté de celui qui m'a envoyé."
                    },
                    {
                        "ref": "Jean 10:30",
                        "texte": "Moi et le Père nous sommes un."
                    },
                ],
            },
            {
                "titre": "Choisir une Norme de la Vérité",
                "contenu": "La vérité c'est la vérité, que l'on soit d'accord avec elle ou non, "
                    "qu'on la croie ou non — elle demeure. Laisser la Parole s'interpréter "
                    "elle-même pour voir le vrai dessein de Dieu.",
                "versets": [
                    {
                        "ref": "Jean 17:17",
                        "texte": "Sanctifie-les par ta vérité : ta parole est la vérité."
                    },
                    {
                        "ref": "Deutéronome 30:19-20",
                        "texte": "J'en prends aujourd'hui à témoin contre vous le ciel et la terre : "
                            "j'ai mis devant toi la vie et la mort, la bénédiction et la malédiction. "
                            "Choisis la vie, afin que tu vives, toi et ta postérité."
                    },
                    {
                        "ref": "Jean 8:31-32",
                        "texte": "Jésus dit alors aux Juifs qui avaient cru en lui : "
                            "Si vous demeurez dans ma parole, vous êtes vraiment mes disciples ; "
                            "vous connaîtrez la vérité, et la vérité vous affranchira."
                    },
                ],
            },
            {
                "titre": "Notre Choix selon le Libre Arbitre",
                "contenu": "Nous aimons Dieu parce que Dieu nous a aimés le premier. "
                    "C'est notre choix, selon le libre arbitre, d'obéir à Sa Parole "
                    "et de jouir de l'abondance qu'Il a pour nous.",
                "versets": [
                    {
                        "ref": "Aggée 1:5",
                        "texte": "Maintenant, ainsi parle l'Éternel des armées : "
                            "Portez votre attention sur vos voies !"
                    },
                    {
                        "ref": "Matthieu 22:29",
                        "texte": "Jésus leur répondit : Vous êtes dans l'erreur, parce que vous ne "
                            "comprenez ni les Écritures ni la puissance de Dieu."
                    },
                ],
            },
        ],
        "mnemo": "🛣️ J-V-T-V = JÉSUS : Voie – Vérité – (et la) Vie\n"
            "Retiens : Jean 14:6 = Chapitre 14, verset 6\n"
            "→ 1+4 = 5 lettres dans 'JESUS' ✓\n"
            "📌 Jésus = GPS parfait : il ne recalcule jamais, il EST déjà arrivé !",
        "histoire": "Un automobiliste perdu dans le désert appelle un GPS. La voix répond : "
            "'Je suis JÉSUS — le Chemin, la Vérité et la Vie.' L'homme dit : 'Recalcul en cours ?' "
            "Jésus : 'Non. Je ne recalcule jamais. Je suis déjà arrivé là où tu vas.' "
            "L'homme suit. Il arrive dans un jardin d'abondance totale. "
            "Le GPS dit : 'Profitez — c'est tout pour vous.' Fin du trajet. Début de la vie.",
        "verite_cle": "Dieu veut que son peuple prospère physiquement, mentalement et spirituellement. "
            "Ce n'est pas une option — c'est Son désir dès la création !",
    },
    {
        "num": 2,
        "titre": "La Parole de Dieu est la Norme",
        "couleur": "#E94560",
        "intro": (
            "La Parole de Dieu est notre norme absolue de croyance et d'action. "
            "Personne ne va au-delà de ce qu'on lui a enseigné. "
            "Il est donc essentiel de connaître et d'étudier la Parole."
        ),
        "sections": [
            {
                "titre": "Les Objectifs du Voleur vs Jésus",
                "contenu": "Le voleur entre furtivement. Ses 3 objectifs : **dérober**, **égorger**, **détruire**. "
                    "Jésus au contraire est venu pour donner la vie — et la vie en abondance. "
                    "Ces deux réalités s'opposent radicalement.",
                "versets": [
                    {
                        "ref": "Jean 10:10",
                        "texte": "Le voleur ne vient que pour dérober, égorger et détruire ; "
                            "moi, je suis venu afin que les brebis aient la vie, "
                            "et qu'elles soient dans l'abondance."
                    },
                    {
                        "ref": "1 Jean 3:8",
                        "texte": "Celui qui pèche est du diable, car le diable pèche dès le commencement. "
                            "Le Fils de Dieu a paru afin de détruire les oeuvres du diable."
                    },
                    {
                        "ref": "Actes 10:38",
                        "texte": "Comment Dieu a oint de l'Esprit Saint et de force Jésus de Nazareth, "
                            "qui allait de lieu en lieu faisant du bien et guérissant tous ceux qui "
                            "étaient tyrannisés par le diable, car Dieu était avec lui."
                    },
                ],
            },
            {
                "titre": "L'Autorité et l'Intégrité de la Parole Révélée",
                "contenu": "Dieu ne peut pas mentir. Sa Parole est immuable. "
                    "Ce qu'Il a promis, Il l'accomplit. "
                    "C'est le fondement de notre confiance.",
                "versets": [
                    {
                        "ref": "2 Pierre 1:20",
                        "texte": "Sachez d'abord vous-mêmes qu'aucune prophétie de l'Écriture "
                            "ne peut être un objet d'interprétation particulière."
                    },
                    {
                        "ref": "Hébreux 6:18",
                        "texte": "Afin que, par deux choses immuables, dans lesquelles il est impossible "
                            "que Dieu mente, nous trouvions un puissant encouragement, nous dont "
                            "le refuge a été de saisir l'espérance qui nous était proposée."
                    },
                    {
                        "ref": "Nombres 23:19",
                        "texte": "Dieu n'est pas un homme pour mentir, ni un fils d'homme pour se repentir. "
                            "Ce qu'il a dit, ne le fera-t-il pas ? Ce qu'il a déclaré, "
                            "ne l'exécutera-t-il pas ?"
                    },
                    {
                        "ref": "Malachie 3:6",
                        "texte": "Car je suis l'Éternel, je ne change pas."
                    },
                ],
            },
            {
                "titre": "Nous Pouvons Avoir Confiance en Sa Parole",
                "contenu": "La Parole de Dieu est vivante et efficace. "
                    "Elle pénètre jusqu'à la division de l'âme et de l'esprit. "
                    "Elle est notre boussole et notre lumière.",
                "versets": [
                    {
                        "ref": "Hébreux 4:12",
                        "texte": "Car la parole de Dieu est vivante et efficace, plus tranchante "
                            "qu'une épée quelconque à deux tranchants, pénétrante jusqu'à partager "
                            "âme et esprit, jointures et moelles ; elle juge les sentiments "
                            "et les pensées du coeur."
                    },
                    {
                        "ref": "Romains 16:25-26",
                        "texte": "Or, à celui qui a le pouvoir de vous affermir selon mon évangile "
                            "et la prédication de Jésus Christ — selon la révélation du mystère "
                            "gardé dans le silence pendant des temps éternels, mais manifesté "
                            "maintenant — à lui soit la gloire."
                    },
                ],
            },
        ],
        "mnemo": "⚖️ VOLEUR 3D vs JÉSUS 3V\n"
            "❌ Voleur : Dérober – Détruire – Décimer\n"
            "✅ Jésus : Vie – Victoire – Volume d'abondance\n"
            "📌 Jean 10:10 → '10 sur 10' = Note parfaite de la Parole !",
        "histoire": "Un cambrioleur arrive avec un grand sac marqué 'DESTRUCTION'. "
            "Il vole la joie, casse l'espoir, détruit la paix. Il repart satisfait. "
            "Cinq minutes plus tard, Jésus arrive avec un camion-citerne rempli d'abondance. "
            "Il répare tout, remplit chaque pièce de vie débordante. "
            "Il pose sur la porte : 'VERROU INCASSABLE — Parole de Dieu.' "
            "Le cambrioleur revient. La porte ne cède pas. Fin.",
        "verite_cle": "Personne ne va au-delà de ce qu'on lui a enseigné. "
            "La qualité de notre vie spirituelle dépend de la qualité de notre connaissance de la Parole.",
    },
    {
        "num": 3,
        "titre": "La Sûreté de Nos Jours",
        "couleur": "#27AE60",
        "intro": (
            "Nous pouvons apprendre à retenir la Parole dans notre intelligence, "
            "à avoir confiance en elle, à croire cette Parole, "
            "à voir son intégrité et l'authenticité de la vérité. "
            "La sincérité n'est **pas** une garantie pour la vérité."
        ),
        "sections": [
            {
                "titre": "La Sincérité ne Garantit pas la Vérité",
                "contenu": "On peut être sincèrement dans l'erreur. "
                    "La sincérité est une qualité de coeur, mais elle ne remplace pas "
                    "la connaissance de la vérité. Seule la Parole de Dieu est la norme.",
                "versets": [
                    {
                        "ref": "2 Timothée 3:16",
                        "texte": "Toute Écriture est inspirée de Dieu, et utile pour enseigner, "
                            "pour convaincre, pour corriger, pour instruire dans la justice."
                    },
                    {
                        "ref": "Matthieu 4:4",
                        "texte": "Jésus répondit : Il est écrit : L'homme ne vivra pas de pain seulement, "
                            "mais de toute parole qui sort de la bouche de Dieu."
                    },
                    {
                        "ref": "Matthieu 5:18",
                        "texte": "Car, je vous le dis en vérité, tant que le ciel et la terre "
                            "subsisteront, il ne disparaîtra pas de la loi un seul iota ou un seul "
                            "trait de lettre, jusqu'à ce que tout soit arrivé."
                    },
                ],
            },
            {
                "titre": "Ce que Dieu dit à propos de Sa Parole",
                "contenu": "La Parole de Dieu est pure, préservée à jamais. "
                    "Elle est une lampe à nos pieds et une lumière sur notre sentier. "
                    "Dans un monde incertain, elle est notre sûreté absolue.",
                "versets": [
                    {
                        "ref": "Psaumes 119:105",
                        "texte": "Ta parole est une lampe à mes pieds, "
                            "et une lumière sur mon sentier."
                    },
                    {
                        "ref": "Psaumes 119:160",
                        "texte": "La somme de ta parole est la vérité, "
                            "et toutes tes lois éternelles sont justes."
                    },
                    {
                        "ref": "Psaumes 12:7",
                        "texte": "Toi, Éternel ! tu les garderas, tu nous préserveras de cette race, "
                            "à jamais."
                    },
                    {
                        "ref": "Ésaïe 33:5-6",
                        "texte": "L'Éternel est élevé, car il habite dans les hauteurs ; "
                            "il remplit Sion de droiture et de justice. "
                            "Il sera la sécurité de tes jours, "
                            "une riche source de salut, de sagesse et de connaissance."
                    },
                ],
            },
        ],
        "mnemo": "🔦 LAMPE pour les PIEDS = présent immédiat\n"
            "💡 LUMIÈRE sur le SENTIER = direction future\n"
            "Ps 119:105 → 119 = 1-1-9 → 'Une seule Parole, 9 fois confirmée !' \n"
            "📌 Parole = GPS + lampe torche + boussole + assurance vie !",
        "histoire": "Un explorateur part dans une grotte sombre avec deux gadgets : "
            "une lampe-frontale (Parole pour les pieds) et un phare géant (Parole pour le sentier). "
            "D'autres explorent sincèrement... mais dans le noir. "
            "Ils se cognent aux stalactites, tombent dans des trous, tournent en rond. "
            "Notre explorateur sort bronzé et chargé de trésors. "
            "Conclusion : la sincérité n'éclaire pas. La Parole, si.",
        "verite_cle": "La Parole de Dieu est la sûreté de nos jours. "
            "Elle ne change pas selon nos humeurs ou les circonstances — elle demeure éternellement.",
    },
    {
        "num": 4,
        "titre": "Le Sujet de Toute la Parole de Dieu",
        "couleur": "#8E44AD",
        "intro": (
            "Jésus Christ est le passe-partout à l'interprétation de toute la Parole. "
            "Il a lui-même divisé la Parole en trois catégories : "
            "**la Loi**, **les Prophètes** et **les Psaumes**. "
            "Toute l'Écriture parle de Lui."
        ),
        "sections": [
            {
                "titre": "Jésus Christ : Clé de Toute la Parole",
                "contenu": "De la Genèse à l'Apocalypse, tout parle de Jésus Christ. "
                    "C'est Lui le fil conducteur de toute l'Écriture. "
                    "Sans Lui, la Bible reste un livre fermé.",
                "versets": [
                    {
                        "ref": "Luc 24:44-45",
                        "texte": "Puis il leur dit : C'est là ce que je vous disais lorsque j'étais "
                            "encore avec vous, qu'il fallait que s'accomplît tout ce qui est écrit "
                            "de moi dans la loi de Moïse, dans les prophètes, et dans les psaumes. "
                            "Alors il leur ouvrit l'intelligence, pour qu'ils comprissent les Écritures."
                    },
                    {
                        "ref": "Jean 1:45",
                        "texte": "Philippe rencontra Nathanaël, et lui dit : Nous avons trouvé celui "
                            "dont Moïse a parlé dans la loi et dont les prophètes ont parlé, "
                            "Jésus de Nazareth, fils de Joseph."
                    },
                    {
                        "ref": "Colossiens 1:18-19",
                        "texte": "Il est la tête du corps de l'Église ; il est le commencement, "
                            "le premier-né d'entre les morts, afin d'être en tout le premier. "
                            "Car Dieu a voulu faire habiter toute la plénitude en lui."
                    },
                ],
            },
            {
                "titre": "Se Présenter comme un Ouvrier Approuvé",
                "contenu": "La plus grande des oeuvres de Dieu est Sa Parole. "
                    "Dieu a magnifié Sa Parole au-dessus de Son nom. "
                    "C'est à nous de la lire, l'écouter, l'étudier "
                    "et d'y mettre des efforts diligents.",
                "versets": [
                    {
                        "ref": "2 Timothée 2:15",
                        "texte": "Efforce-toi de te présenter devant Dieu comme un homme éprouvé, "
                            "un ouvrier qui n'a point à rougir, "
                            "qui dispense droitement la parole de la vérité."
                    },
                    {
                        "ref": "Psaumes 119:89",
                        "texte": "Éternel ! ta parole subsiste à jamais dans les cieux."
                    },
                    {
                        "ref": "Psaumes 138:2",
                        "texte": "Je me prosterne vers ton saint temple, et je célèbre ton nom "
                            "pour ta bonté et ta fidélité, parce que tu as fait passer ta parole "
                            "avant tout ce qui te fait glorifier."
                    },
                    {
                        "ref": "Actes 17:11",
                        "texte": "Ces Juifs avaient des sentiments plus nobles que ceux de Thessalonique ; "
                            "ils reçurent la parole avec beaucoup d'empressement, "
                            "et ils examinaient chaque jour les Écritures, pour voir si ce qu'on "
                            "leur disait était exact."
                    },
                ],
            },
            {
                "titre": "La Parole de Dieu est la Volonté de Dieu",
                "contenu": "Lire la Parole est la plus grande clé pour être un ouvrier de Dieu. "
                    "La Parole n'est pas une option — c'est notre pain quotidien spirituel.",
                "versets": [
                    {
                        "ref": "Ésaïe 55:8-11",
                        "texte": "Car mes pensées ne sont pas vos pensées, et vos voies ne sont pas "
                            "mes voies, dit l'Éternel. Autant les cieux sont élevés au-dessus de la "
                            "terre, autant mes voies sont élevées au-dessus de vos voies, et mes "
                            "pensées au-dessus de vos pensées. Comme la pluie et la neige descendent "
                            "des cieux... ainsi en est-il de ma parole : elle ne retourne point à moi "
                            "sans effet, sans avoir exécuté ma volonté."
                    },
                    {
                        "ref": "Néhémie 8:8",
                        "texte": "Ils lurent dans le livre de la loi de Dieu d'une manière distincte, "
                            "avec explication, et l'on faisait comprendre ce qu'on lisait."
                    },
                ],
            },
        ],
        "mnemo": "🔑 JÉSUS = CLÉ PASSE-PARTOUT\n"
            "Loi + Prophètes + Psaumes → tout parle de LUI\n"
            "2Tim 2:15 = '2 choses × 15 méthodes = ouvrier parfait'\n"
            "📌 Ouvrier = Effort + Droiture + Parole bien divisée",
        "histoire": "Un serrurier reçoit 1500 clés pour ouvrir la Bible. "
            "Il essaie clé par clé pendant 20 ans. "
            "Puis quelqu'un lui tend une clé dorée : 'Jésus-Christ'. "
            "Elle ouvre TOUT en une seconde. "
            "La Loi, les Prophètes, les Psaumes — tout s'illumine. "
            "Le serrurier jette les 1499 autres et devient le meilleur ouvrier du quartier.",
        "verite_cle": "Dieu a magnifié Sa Parole au-dessus de Son propre Nom (Ps 138:2). "
            "Rien n'est plus important que de connaître et de diviser droitement Sa Parole.",
    },
    {
        "num": 5,
        "titre": "Les Clés à l'Interprétation de la Parole",
        "couleur": "#2471A3",
        "intro": (
            "Toute Écriture s'interprète elle-même : dans le verset lui-même, "
            "ou dans le contexte utilisé auparavant. "
            "Il existe des vérités bibliques fondamentales auxquelles nous devons adhérer."
        ),
        "sections": [
            {
                "titre": "3 Vérités Fondamentales d'Interprétation",
                "contenu": "**1.** Il faut savoir la **période de temps** à laquelle une section est adressée.\n"
                    "**2.** Le **verset difficile** doit être compris à la lumière des versets clairs.\n"
                    "**3.** L'interprétation tient toujours compte de **à qui** c'est adressé.",
                "versets": [
                    {
                        "ref": "2 Pierre 1:20",
                        "texte": "Sachez d'abord vous-mêmes qu'aucune prophétie de l'Écriture "
                            "ne peut être un objet d'interprétation particulière."
                    },
                    {
                        "ref": "1 Timothée 3:16",
                        "texte": "Toute Écriture est inspirée de Dieu, et utile pour enseigner, "
                            "pour convaincre, pour corriger, pour instruire dans la justice."
                    },
                    {
                        "ref": "1 Corinthiens 10:31-32",
                        "texte": "Soit donc que vous mangiez, soit que vous buviez, "
                            "soit que vous fassiez quelque autre chose, faites tout pour la gloire de Dieu."
                    },
                ],
            },
            {
                "titre": "Toute la Parole est Utile — mais pas tout nous est directement adressé",
                "contenu": "Toute la Parole est utile pour enseigner, convaincre, corriger et instruire. "
                    "Cependant, toute la Parole ne nous est pas directement adressée aujourd'hui "
                    "dans cette administration, en tant que croyants nés de nouveau.",
                "versets": [
                    {
                        "ref": "Romains 15:4",
                        "texte": "Car tout ce qui a été écrit d'avance a été écrit pour notre instruction, "
                            "afin que, par la patience, et par la consolation que donnent les Écritures, "
                            "nous possédions l'espérance."
                    },
                    {
                        "ref": "Jacques 5:10",
                        "texte": "Frères, prenez pour modèles de souffrance et de patience "
                            "les prophètes qui ont parlé au nom du Seigneur."
                    },
                ],
            },
        ],
        "mnemo": "📖 3C d'interprétation :\n"
            "C1 = CONTEXTE (la Bible s'explique par elle-même)\n"
            "C2 = CLARTÉ (le flou cède au clair)\n"
            "C3 = CIBLE (à qui ? quelle époque ?)\n"
            "📌 Sans les 3C, tu risques d'interpréter à côté !",
        "histoire": "Un détective reçoit un message biblique crypté. "
            "Son assistant propose des experts extérieurs. "
            "Le détective refuse : 'La Bible se déchiffre elle-même.' "
            "Il compare verset à verset, période à période, destinataire à destinataire. "
            "Le message devient lumineux. "
            "Conclusion : pas d'interprétation solitaire. La Bible est son propre dictionnaire.",
        "verite_cle": "2 Pierre 1:20 est la règle d'or : aucune prophétie de l'Écriture "
            "ne peut être une affaire d'interprétation privée. "
            "La Bible s'explique elle-même.",
    },
    {
        "num": 6,
        "titre": "Au Commencement",
        "couleur": "#E67E22",
        "intro": (
            "La Parole de Dieu n'a jamais été écrite pour l'incrédule. "
            "Elle est écrite pour ceux qui veulent aimer Dieu, connaître la vérité, "
            "et qui sont prêts à être humbles et disciplinés selon la vérité. "
            "Au commencement, Jésus Christ était dans la présence de Dieu."
        ),
        "sections": [
            {
                "titre": "Dieu : Initiateur du Salut — Christ : Agent du Salut",
                "contenu": "Dieu est l'Auteur et l'Initiateur du salut. "
                    "Jésus Christ en est le Moyen et l'Agent. "
                    "Au commencement, la Parole était déjà là — elle était Dieu.",
                "versets": [
                    {
                        "ref": "Genèse 1:1",
                        "texte": "Au commencement, Dieu créa les cieux et la terre."
                    },
                    {
                        "ref": "Jean 1:1-4",
                        "texte": "Au commencement était la Parole, et la Parole était avec Dieu, "
                            "et la Parole était Dieu. Elle était au commencement avec Dieu. "
                            "Toutes choses ont été faites par elle, et rien de ce qui a été fait "
                            "n'a été fait sans elle. En elle était la vie, et la vie était la lumière "
                            "des hommes."
                    },
                    {
                        "ref": "Hébreux 11:3",
                        "texte": "C'est par la foi que nous reconnaissons que le monde a été formé "
                            "par la parole de Dieu, en sorte que ce qu'on voit n'a pas été fait "
                            "de choses visibles."
                    },
                ],
            },
            {
                "titre": "La Terre Devint Informe et Vide",
                "contenu": "La terre est devenue informe et vide à cause de l'adversaire. "
                    "Ce n'était pas son état original. "
                    "Dieu l'a créée bonne — c'est Satan qui l'a rendue chaotique.",
                "versets": [
                    {
                        "ref": "Genèse 1:2",
                        "texte": "La terre était informe et vide : il y avait des ténèbres "
                            "à la surface de l'abîme, et l'esprit de Dieu se mouvait "
                            "au-dessus des eaux."
                    },
                    {
                        "ref": "Ézéchiel 28:12-15",
                        "texte": "Tu étais le sceau de la perfection, plein de sagesse, "
                            "parfait en beauté. Tu étais en Éden, le jardin de Dieu... "
                            "Tu as été intègre dans tes voies, depuis le jour où tu fus créé "
                            "jusqu'à celui où l'iniquité a été trouvée en toi."
                    },
                    {
                        "ref": "Jérémie 4:23",
                        "texte": "Je regardai la terre, et voici, elle était informe et vide ; "
                            "les cieux, et ils n'avaient point de lumière."
                    },
                ],
            },
        ],
        "mnemo": "🌌 AU COMMENCEMENT = 3 réalités :\n"
            "1. PAROLE → était déjà là (Jean 1:1)\n"
            "2. CREATION → Dieu parle, tout existe\n"
            "3. CHAOS → l'adversaire sabote la terre\n"
            "📌 Avant le Big Bang : le BIG WORD !",
        "histoire": "Avant l'Univers, Jésus et Dieu prenaient le café dans l'éternité. "
            "Dieu dit : 'Et si on créait quelque chose ?' BOUM — galaxies, étoiles, planètes ! "
            "Mais Satan sabote la Terre et la laisse informe et vide. "
            "Dieu ne panique pas. Il reprend son projet et le reconstruit, encore meilleur. "
            "Morale : Dieu n'abandonne jamais ses projets.",
        "verite_cle": "Jean 1:1 révèle que Jésus-Christ (la Parole) existait avant toute création. "
            "Il n'est pas une créature — Il est le Créateur lui-même.",
    },
    {
        "num": 7,
        "titre": "La Surface de l'Abîme",
        "couleur": "#1ABC9C",
        "intro": (
            "Qu'est-ce que la surface de l'abîme et l'étendue ? "
            "Il existe trois cieux et trois terres dans la Parole de Dieu. "
            "La terre a changé au fil du temps selon le plan de Dieu."
        ),
        "sections": [
            {
                "titre": "Les Trois Cieux et les Trois Terres",
                "contenu": "**Terre 1** : Originelle (avant la chute de Satan — parfaite).\n"
                    "**Terre 2** : Actuelle (depuis la re-création de Genèse 1 — en cours).\n"
                    "**Terre 3** : Nouvelle (Apocalypse 21 — à venir — parfaite pour l'éternité).",
                "versets": [
                    {
                        "ref": "Genèse 1:1",
                        "texte": "Au commencement, Dieu créa les cieux et la terre."
                    },
                    {
                        "ref": "Apocalypse 21:1",
                        "texte": "Puis je vis un nouveau ciel et une nouvelle terre ; "
                            "car le premier ciel et la première terre avaient disparu, "
                            "et la mer n'était plus."
                    },
                    {
                        "ref": "2 Pierre 3:5-6",
                        "texte": "Ils oublient volontairement que des cieux existaient autrefois "
                            "et qu'il y avait une terre sortie de l'eau et subsistant au milieu de "
                            "l'eau, par la parole de Dieu, et que, par ces mêmes moyens, le monde "
                            "d'alors périt submergé par l'eau."
                    },
                    {
                        "ref": "1 Jean 1:5",
                        "texte": "La nouvelle que nous avons apprise de lui et que nous vous annonçons, "
                            "c'est que Dieu est lumière, et qu'il n'y a point en lui de ténèbres."
                    },
                ],
            },
            {
                "titre": "Dieu Prépare la Terre — La Terre a Changé",
                "contenu": "La seule masse de terre de Genèse 1:10 s'est divisée en plusieurs continents. "
                    "La terre était inondée au temps de Noé (une seule masse). "
                    "Les gens furent dispersés à Babel (toujours une masse). "
                    "Au temps de **Péleg**, la terre s'est divisée en continents.",
                "versets": [
                    {
                        "ref": "Genèse 1:9-10",
                        "texte": "Dieu dit : Que les eaux qui sont au-dessous du ciel se rassemblent "
                            "en un seul lieu, et que le sec paraisse. Et cela fut ainsi. "
                            "Dieu appela le sec terre, et il appela l'amas des eaux mers."
                    },
                    {
                        "ref": "Genèse 10:25",
                        "texte": "À Héber naquirent deux fils ; l'un s'appelait Péleg, "
                            "parce que de son temps la terre fut partagée."
                    },
                ],
            },
        ],
        "mnemo": "🌍 3T = 3 TERRES :\n"
            "T1 = Terre parfaite originelle\n"
            "T2 = Terre actuelle (Genèse 1 re-création)\n"
            "T3 = Terre nouvelle (Apocalypse 21)\n"
            "📌 PÉLEG = 'Division' → les continents sont nés de son vivant !",
        "histoire": "Imaginez un puzzle de 7 milliards de pièces toutes collées (Pangée biblique). "
            "Satan renverse tout. Dieu récupère les pièces et les recolle. "
            "Noé prend un bateau car la masse est encore unique. "
            "À Babel, les gens se dispersent (toujours une masse). "
            "Au temps de Péleg (son nom = division), les continents apparaissent. "
            "Afrique, Europe, Amérique — tous issus du même puzzle de Genèse 1.",
        "verite_cle": "Le nom de Péleg signifie 'division' (Genèse 10:25). "
            "La Parole confirme scientifiquement que les continents se sont séparés "
            "à une époque précise de l'histoire biblique.",
    },
    {
        "num": 8,
        "titre": "L'Idiome de Permission",
        "couleur": "#E74C3C",
        "intro": (
            "Un idiome est un usage de mots particulier à une langue ou une culture. "
            "En tant qu'idiome, les mots ne doivent pas être pris dans leur sens littéral. "
            "Reconnaître l'idiome hébreu de permission nous permet de ne **jamais** "
            "attribuer le mal à Dieu."
        ),
        "sections": [
            {
                "titre": "L'Idiome Hébreu de Permission",
                "contenu": "En hébreu, 'Dieu a fait X' peut souvent signifier "
                    "'Dieu a PERMIS que X arrive'. "
                    "Cette distinction est cruciale pour comprendre le caractère de Dieu "
                    "et ne pas Lui attribuer le mal.",
                "versets": [
                    {
                        "ref": "Exode 10:20",
                        "texte": "Mais l'Éternel endurcit le coeur de Pharaon, "
                            "et Pharaon ne laissa point aller les enfants d'Israël."
                    },
                    {
                        "ref": "Genèse 6:8-13",
                        "texte": "Mais Noé trouva grâce aux yeux de l'Éternel... "
                            "La terre était corrompue devant Dieu, la terre était pleine de violence. "
                            "Dieu regarda la terre, et voici, elle était corrompue ; "
                            "car toute chair avait corrompu sa voie sur la terre."
                    },
                ],
            },
            {
                "titre": "La Raison d'Être de l'Homme",
                "contenu": "La raison d'être de l'Univers est la Terre. "
                    "La raison d'être de la Terre est l'Homme. "
                    "La raison d'être de l'Homme est d'**aimer Dieu**, de l'adorer et de communier avec Lui.",
                "versets": [
                    {
                        "ref": "Matthieu 22:36-37",
                        "texte": "Maître, quel est le grand commandement de la loi ? "
                            "Jésus lui répondit : Tu aimeras le Seigneur, ton Dieu, "
                            "de tout ton coeur, de toute ton âme, et de toute ta pensée."
                    },
                    {
                        "ref": "Genèse 1:24-25",
                        "texte": "Dieu dit : Que la terre produise des animaux vivants selon leur espèce... "
                            "Et Dieu vit que cela était bon."
                    },
                ],
            },
        ],
        "mnemo": "🎭 IDIOME HÉBREU = PERMISSION\n"
            "'Dieu a fait X' → souvent 'Dieu a PERMIS X'\n"
            "Pharaon = il a durci son propre coeur, Dieu l'a permis\n"
            "📌 RÈGLE D'OR : Ne jamais attribuer le mal à Dieu !",
        "histoire": "Un journaliste titre : 'Dieu a durci le coeur de Pharaon !' "
            "Un expert hébreu corrige : 'En hébreu idiomatique, Dieu a permis que Pharaon "
            "fasse ses propres choix stupides.' "
            "Le journaliste relit ses archives — il avait accusé Dieu de 47 catastrophes ! "
            "L'expert résume : Univers = pour la Terre. Terre = pour l'Homme. "
            "Homme = pour aimer Dieu. Pharaon avait court-circuité tout ça.",
        "verite_cle": "Dieu ne fait jamais le mal. Jacques 1:13 confirme : "
            "'Dieu ne tente personne.' L'idiome de permission explique "
            "les passages qui semblent attribuer le mal à Dieu.",
    },
    {
        "num": 9,
        "titre": "Les Fondements de Toute Vie",
        "couleur": "#27AE60",
        "intro": (
            "Le but et la signification de la création sont établis en Genèse : "
            "les fondements de toute vie. "
            "L'homme est un être tripartite : Corps, Âme et Esprit. "
            "Comprendre cette trilogie est essentiel pour comprendre notre relation avec Dieu."
        ),
        "sections": [
            {
                "titre": "L'Homme : Corps, Âme et Esprit",
                "contenu": "🫀 **Corps** : Formé de la poussière du sol (Genèse 2:7)\n"
                    "💛 **Âme** : Faite — siège des émotions, de la volonté, de la personnalité\n"
                    "✨ **Esprit** : Créé — pour communier directement avec Dieu",
                "versets": [
                    {
                        "ref": "Genèse 2:7",
                        "texte": "L'Éternel Dieu forma l'homme de la poussière du sol, "
                            "il souffla dans ses narines un souffle de vie "
                            "et l'homme devint un être vivant."
                    },
                    {
                        "ref": "Lévitique 17:11",
                        "texte": "Car la vie de la chair est dans le sang. "
                            "Je vous l'ai donné sur l'autel pour faire l'expiation pour vos âmes."
                    },
                    {
                        "ref": "Jean 4:24",
                        "texte": "Dieu est Esprit, et il faut que ceux qui l'adorent "
                            "l'adorent en esprit et en vérité."
                    },
                ],
            },
            {
                "titre": "L'Homme Créé à l'Image de Dieu",
                "contenu": "L'homme a été créé à l'image et selon la ressemblance de Dieu. "
                    "Il était destiné à dominer sur toute la création. "
                    "C'est la plus haute dignité que Dieu puisse accorder.",
                "versets": [
                    {
                        "ref": "Genèse 1:26",
                        "texte": "Dieu dit : Faisons l'homme à notre image, selon notre ressemblance, "
                            "et qu'il domine sur les poissons de la mer, sur les oiseaux du ciel, "
                            "sur le bétail, sur toute la terre, "
                            "et sur tous les reptiles qui rampent sur la terre."
                    },
                    {
                        "ref": "Genèse 1:28",
                        "texte": "Dieu les bénit, et Dieu leur dit : Soyez féconds, multipliez, "
                            "remplissez la terre, et l'assujettissez ; et dominez sur les poissons "
                            "de la mer, sur les oiseaux du ciel, et sur tout animal qui se meut "
                            "sur la terre."
                    },
                ],
            },
        ],
        "mnemo": "🧬 C-A-E = Corps – Âme – Esprit\n"
            "Corps = FORMÉ (argile)\n"
            "Âme = FAITE (vie émotionnelle)\n"
            "Esprit = CRÉÉ (communion avec Dieu)\n"
            "📌 Dieu est Esprit → Il nous parle esprit à esprit !",
        "histoire": "Dieu fabrique l'homme comme un chef fait son plat signature. "
            "Il prend de la terre (corps), souffle dessus (esprit), "
            "et la créature devient une âme vivante. "
            "Le chef dit : 'Image de Moi !' "
            "L'homme se regarde dans le miroir et voit un être royal avec couronne et sceptre. "
            "La grenouille du jardin voisin est très impressionnée.",
        "verite_cle": "L'homme est la seule créature créée à l'image de Dieu. "
            "Il est le sommet de toute la création — pas un accident cosmique, "
            "mais le chef-d'oeuvre intentionnel du Créateur.",
    },
    {
        "num": 10,
        "titre": "La Connaissance du Bien et du Mal",
        "couleur": "#F39C12",
        "intro": (
            "La Parole de Dieu est une Parole de vie — pas simplement un livre de morale "
            "ou de philosophie. Dieu voulait que l'homme expérimente le bien et évite le mal. "
            "Les bénédictions de Dieu nous appartiennent quand nous choisissons la vie "
            "en obéissant à Sa Parole."
        ),
        "sections": [
            {
                "titre": "Le Souffle de Vie et le Jardin d'Éden",
                "contenu": "Dieu a tout préparé avant de créer l'homme. "
                    "Le jardin d'Éden était un lieu d'abondance totale, "
                    "de beauté parfaite et de communion directe avec Dieu.",
                "versets": [
                    {
                        "ref": "Genèse 2:8-9",
                        "texte": "L'Éternel Dieu planta un jardin en Éden, à l'orient, "
                            "et il y mit l'homme qu'il avait formé. "
                            "L'Éternel Dieu fit pousser du sol des arbres de toute espèce, "
                            "agréables à voir et bons à manger, et l'arbre de la vie au milieu "
                            "du jardin, et l'arbre de la connaissance du bien et du mal."
                    },
                    {
                        "ref": "Ésaïe 42:5",
                        "texte": "Ainsi parle le Dieu, l'Éternel, qui a créé les cieux et les a "
                            "déployés, qui a étendu la terre et ses productions, "
                            "qui a donné la respiration à ceux qui la peuplent, "
                            "et le souffle à ceux qui y marchent."
                    },
                ],
            },
            {
                "titre": "La Volonté de Dieu : Bien Expérimenter, Mal Éviter",
                "contenu": "Dieu avait clairement enseigné la différence entre le bien et le mal. "
                    "Il voulait que l'homme expérimente le bien et évite le mal. "
                    "L'arbre interdit n'était pas une punition — c'était une **protection**.",
                "versets": [
                    {
                        "ref": "Genèse 2:16-17",
                        "texte": "L'Éternel Dieu donna cet ordre à l'homme : "
                            "Tu pourras manger de tous les arbres du jardin ; "
                            "mais tu ne mangeras pas de l'arbre de la connaissance "
                            "du bien et du mal, car le jour où tu en mangeras, tu mourras."
                    },
                    {
                        "ref": "Genèse 2:18",
                        "texte": "L'Éternel Dieu dit : Il n'est pas bon que l'homme soit seul ; "
                            "je lui ferai une aide semblable à lui."
                    },
                    {
                        "ref": "Genèse 2:24",
                        "texte": "C'est pourquoi l'homme quittera son père et sa mère, "
                            "et s'attachera à sa femme, et ils deviendront une seule chair."
                    },
                ],
            },
        ],
        "mnemo": "🌳 JARDIN = LIBERTÉ TOTALE sauf 1 arbre\n"
            "✅ 9 999 arbres = OUI (abondance !)\n"
            "❌ 1 arbre = NON (protection !)\n"
            "Dieu = 99% OUI pour 1% NON\n"
            "📌 L'homme s'est fixé sur le 1%. Erreur fatale !",
        "histoire": "Dieu ouvre le plus grand buffet de l'histoire : 10 000 plats magnifiques. "
            "'Mangez tout !' dit-Il. 'Sauf ce plat au bout de la table — c'est du poison.' "
            "Adam et Ève ont 9 999 options délicieuses. "
            "Mais le 10 000ème les obsède. Ils le mangent quand même. "
            "Morale : Dieu donne l'abondance totale. "
            "Nous, on se fixe sur le seul interdit.",
        "verite_cle": "Le mariage est une institution divine créée avant la chute. "
            "Genèse 2:24 est la fondation biblique du mariage : "
            "un homme, une femme, une seule chair — pour la vie.",
    },
    {
        "num": 11,
        "titre": "Le Premier Péché de l'Humanité",
        "couleur": "#E94560",
        "intro": (
            "Dans la communication que Dieu a eue avec Adam, "
            "Dieu l'avait mis au courant des règles de la vie. "
            "Dieu a établi la vie aussi parfaitement que possible, "
            "donnant à l'homme et à la femme le choix selon le libre arbitre "
            "de la vivre abondamment."
        ),
        "sections": [
            {
                "titre": "Les 5 Tactiques de Satan pour Détruire la Parole",
                "contenu": "Satan utilise 5 tactiques précises pour faire tomber l'homme :\n\n"
                    "**1.** Met en question l'intégrité de la Parole\n"
                    "**2.** Pousse à répondre en considérant\n"
                    "**3.** Omet librement les conséquences\n"
                    "**4.** Ajoute à la Parole ('vous n'y toucherez point' — Ève ajoute !)\n"
                    "**5.** Change la Parole ('vous ne mourrez PAS')",
                "versets": [
                    {
                        "ref": "Genèse 3:1-4",
                        "texte": "Le serpent était le plus rusé de tous les animaux des champs, "
                            "que l'Éternel Dieu avait faits. Il dit à la femme : "
                            "Dieu a-t-il réellement dit : Vous ne mangerez pas de tous les arbres "
                            "du jardin ? La femme répondit au serpent : "
                            "Nous mangeons du fruit des arbres du jardin. "
                            "Mais quant au fruit de l'arbre qui est au milieu du jardin, "
                            "Dieu a dit : Vous n'en mangerez point et vous n'y toucherez point, "
                            "de peur que vous ne mouriez. "
                            "Le serpent dit à la femme : Vous ne mourrez point."
                    },
                ],
            },
            {
                "titre": "L'Homme a Perdu la Domination",
                "contenu": "Suite à la chute, l'homme a perdu la domination que Dieu lui avait donnée. "
                    "Satan est devenu 'le prince de ce monde'. "
                    "Mais Dieu avait déjà prévu la solution : **Jésus Christ**.",
                "versets": [
                    {
                        "ref": "Genèse 1:28",
                        "texte": "Dieu les bénit, et Dieu leur dit : Soyez féconds, multipliez, "
                            "remplissez la terre, et l'assujettissez."
                    },
                    {
                        "ref": "Jean 14:30",
                        "texte": "Je ne parlerai plus guère avec vous ; car le prince du monde vient. "
                            "Il n'a rien en moi."
                    },
                ],
            },
            {
                "titre": "Jésus Christ : Notre Semence Promise",
                "contenu": "Genèse 3:15 est la première prophétie messianique de la Bible. "
                    "Dès la chute, Dieu annonce la victoire finale de Christ. "
                    "Jésus est la semence promise qui écrase la tête de l'adversaire.",
                "versets": [
                    {
                        "ref": "Genèse 3:15",
                        "texte": "Je mettrai inimitié entre toi et la femme, "
                            "entre ta postérité et sa postérité : "
                            "celle-ci t'écrasera la tête, "
                            "et tu lui blesseras le talon."
                    },
                    {
                        "ref": "1 Jean 3:8",
                        "texte": "Le Fils de Dieu a paru afin de détruire les oeuvres du diable."
                    },
                ],
            },
        ],
        "mnemo": "🐍 SATAN = 5 tactiques (QOACE) :\n"
            "Q = Questionne ('A-t-il dit ?')\n"
            "O = Omet les conséquences\n"
            "A = Ajoute ('ni toucher' — Ève !)\n"
            "C = Change ('vous ne mourrez PAS')\n"
            "E = Engage à considérer l'interdit\n"
            "📌 Genèse 3:15 = 1ère prophétie de Christ !",
        "histoire": "Satan arrive avec micro, tableau et costume trois pièces. "
            "Étape 1 : 'Dieu a vraiment dit ÇA ?' (doute instillé). "
            "Étape 2 : 'Regarde comme c'est beau...' (tentation). "
            "Étape 3 : Il oublie de mentionner la mort (omission). "
            "Étape 4 : Ève ajoute 'ni toucher' (modification). "
            "Étape 5 : 'Vous ne mourrez PAS !' (mensonge pur). "
            "Résultat : chute. Mais Dieu répond au verset 15 : "
            "'La semence écrasera ta tête.' Satan perd avant de célébrer.",
        "verite_cle": "Genèse 3:15 est appelé le Protévangile — la première bonne nouvelle. "
            "Dès le début de la chute, Dieu annonce la victoire de Christ sur Satan.",
    },
    {
        "num": 12,
        "titre": "Le Plus Grand Principe : La Croyance",
        "couleur": "#8E44AD",
        "intro": (
            "Le plus grand principe dans toute la vie, c'est la **croyance**. "
            "Pour recevoir quoi que ce soit de Dieu, on doit d'abord savoir "
            "ce qui est disponible, comment le recevoir, et qu'en faire. "
            "La croyance provient du coeur."
        ),
        "sections": [
            {
                "titre": "Ce qui est Disponible en Dieu",
                "contenu": "Dieu veut bénir son peuple dans tous les domaines. "
                    "Avant de recevoir, il faut savoir ce qui est disponible. "
                    "L'ignorance empêche la réception.",
                "versets": [
                    {
                        "ref": "3 Jean 2",
                        "texte": "Bien-aimé, je souhaite que tu prospères à tous égards "
                            "et sois en bonne santé, comme prospère l'état de ton âme."
                    },
                    {
                        "ref": "2 Corinthiens 9:8",
                        "texte": "Et Dieu peut vous combler de toutes sortes de grâces, "
                            "afin que, ayant toujours en toutes choses de quoi satisfaire "
                            "à tous vos besoins, vous ayez encore en abondance pour "
                            "toute bonne oeuvre."
                    },
                    {
                        "ref": "Romains 8:37",
                        "texte": "Mais dans toutes ces choses nous sommes plus que vainqueurs "
                            "par celui qui nous a aimés."
                    },
                    {
                        "ref": "Éphésiens 3:16-19",
                        "texte": "Qu'il vous accorde, selon la richesse de sa gloire, d'être "
                            "puissamment fortifiés par son Esprit dans l'homme intérieur, "
                            "en sorte que Christ habite dans vos coeurs par la foi... "
                            "afin que vous soyez remplis jusqu'à toute la plénitude de Dieu."
                    },
                ],
            },
            {
                "titre": "La Loi de la Croyance — 3 Images",
                "contenu": "**Image 1 :** Précis et préoccupé — on garde nos pensées sur "
                    "la promesse de Dieu qui comble notre besoin.\n\n"
                    "**Image 2 :** On se l'imagine — c'est l'image de croyance dans l'intelligence.\n\n"
                    "**Image 3 :** On agit selon la promesse de Dieu, fidèlement.",
                "versets": [
                    {
                        "ref": "Romains 10:10",
                        "texte": "Car c'est en croyant du coeur qu'on parvient à la justice, "
                            "et c'est en confessant de la bouche qu'on parvient au salut."
                    },
                    {
                        "ref": "Proverbes 4:20-23",
                        "texte": "Mon fils, sois attentif à mes paroles, prête l'oreille à mes discours. "
                            "Qu'ils ne s'éloignent pas de tes yeux, garde-les au fond de ton coeur ; "
                            "car ils sont la vie pour ceux qui les trouvent... "
                            "Garde ton coeur plus que toute autre chose, "
                            "car c'est de lui que viennent les sources de la vie."
                    },
                    {
                        "ref": "Romains 4:20-21",
                        "texte": "Il ne chancela point par incrédulité au sujet de la promesse de Dieu ; "
                            "mais il fut fortifié par la foi, donnant gloire à Dieu, "
                            "et ayant la pleine certitude que ce que Dieu a promis, "
                            "il est puissant pour l'accomplir."
                    },
                    {
                        "ref": "Philippiens 4:19",
                        "texte": "Mon Dieu pourvoira à tous vos besoins selon sa richesse, "
                            "avec gloire, en Jésus Christ."
                    },
                ],
            },
            {
                "titre": "La Vie Synchronisée : Bouche + Coeur + Actions",
                "contenu": "Confesser signifie :\n"
                    "**1.** De notre BOUCHE\n"
                    "**2.** Dans notre COEUR\n"
                    "**3.** Avec nos ACTIONS\n\n"
                    "Lorsque nous croyons positivement, nous avons une vie dans l'abondance. "
                    "Voilà comment nous recevons l'abondance et la puissance de Dieu.",
                "versets": [
                    {
                        "ref": "Jacques 1:21",
                        "texte": "C'est pourquoi, rejetant toute souillure et tout débordement de "
                            "malice, recevez avec douceur la parole qui a été plantée en vous, "
                            "et qui peut sauver vos âmes."
                    },
                    {
                        "ref": "Hébreux 11:11",
                        "texte": "C'est aussi par la foi que Sara elle-même, malgré son âge avancé, "
                            "reçut la force d'être mère, parce qu'elle crut à la fidélité de celui "
                            "qui avait fait la promesse."
                    },
                    {
                        "ref": "Éphésiens 1:19",
                        "texte": "Et quelle est envers nous qui croyons l'infinie grandeur de "
                            "sa puissance, se manifestant avec efficacité par la vertu de sa force."
                    },
                ],
            },
        ],
        "mnemo": "🔑 3 ÉTAPES DE LA CROYANCE VICTORIEUSE :\n"
            "1️⃣ SAVOIR → Quelle promesse pour mon besoin ?\n"
            "2️⃣ IMAGINER → Mettre l'image de victoire dans mon esprit\n"
            "3️⃣ AGIR → Agir fidèlement selon la promesse\n"
            "📌 Bouche + Coeur + Actions = VIE SYNCHRONISÉE !",
        "histoire": "Un athlète veut gagner la course de sa vie. "
            "Étape 1 : il lit la promesse (Parole disponible). "
            "Étape 2 : il s'imagine franchir la ligne d'arrivée chaque matin (image de croyance). "
            "Étape 3 : il s'entraîne selon la promesse (action fidèle). "
            "Le jour J, la Parole de Dieu court avec lui. "
            "Il franchit la ligne avec une facilité déconcertante. "
            "Dans les gradins, trois anges prennent des notes : "
            "'Voilà comment fonctionne la croyance.'",
        "verite_cle": "Romains 4:20-21 (Abraham) = le modèle parfait de la croyance : "
            "ne pas chanceler, être fortifié par la foi, "
            "avoir la pleine certitude que Dieu accomplit ce qu'Il a promis.",
    },
]

ALL_BOOKS = [
    "Genèse","Exode","Lévitique","Nombres","Deutéronome",
    "Josué","Juges","Ruth","1 Samuel","2 Samuel",
    "1 Rois","2 Rois","1 Chroniques","2 Chroniques",
    "Esdras","Néhémie","Esther","Job","Psaumes","Proverbes",
    "Ecclésiaste","Cantique des Cantiques","Ésaïe","Jérémie",
    "Lamentations","Ézéchiel","Daniel","Osée","Joël","Amos",
    "Abdias","Jonas","Michée","Nahum","Habacuc","Sophonie",
    "Aggée","Zacharie","Malachie","Matthieu","Marc","Luc","Jean",
    "Actes des Apôtres","Romains","1 Corinthiens","2 Corinthiens",
    "Galates","Éphésiens","Philippiens","Colossiens",
    "1 Thessaloniciens","2 Thessaloniciens","1 Timothée","2 Timothée",
    "Tite","Philémon","Hébreux","Jacques","1 Pierre","2 Pierre",
    "1 Jean","2 Jean","3 Jean","Jude","Apocalypse"
]

GROUPES_BIBLE = [
    {"nom":"Pentateuque (5)","livres":["Genèse","Exode","Lévitique","Nombres","Deutéronome"],
     "acronyme":"GE-EX-LÉV-NOM-DEU",
     "mnemo":"GEorges EXplose LEVitant sur NOMbreux DEUtons !",
     "histoire":"GEorges, boucher géant, EXplore la ville en LÉVitant. Il compte un NOMbre de fois et le fait DEUx fois. Les voisins appellent la police."},
    {"nom":"Livres Historiques (12)","livres":["Josué","Juges","Ruth","1 Samuel","2 Samuel","1 Rois","2 Rois","1 Chroniques","2 Chroniques","Esdras","Néhémie","Esther"],
     "acronyme":"JO-JU-RU-SA-SA-R-R-CH-CH-ESD-NÉH-EST",
     "mnemo":"JOJo JUgeur sur RUche avec 2 SAmuels, 2 Rois, 2 CHroniques, ESDras, NÉHémie, ESTher !",
     "histoire":"JOJo le clown JUgeur atterrit sur une RUche. Deux SAuterelles en costume arrivent. Deux Rois se battent avec des CHronometeurs. Dragon ESDras souffle du feu sur NÉHumiste. ESTrade s'effondre."},
    {"nom":"Livres Poétiques (5)","livres":["Job","Psaumes","Proverbes","Ecclésiaste","Cantique des Cantiques"],
     "acronyme":"JOB-PS-PRO-ECC-CAN",
     "mnemo":"JOBert PSyché chante PROverbes ECCentriques sur son CANapé !",
     "histoire":"JOBert au chômage depuis 3 siècles. Son PSychologue dit : chante des PROverbes. Il le fait ECCentriquement sur son CANapé en pyjama de licorne. Sa voisine filme pour TikTok."},
    {"nom":"Grands Prophètes (5)","livres":["Ésaïe","Jérémie","Lamentations","Ézéchiel","Daniel"],
     "acronyme":"ÉS-JÉR-LAM-ÉZ-DAN",
     "mnemo":"ÉSpadon rencontre JÉRôme qui LAMente, ÉZéchias appelle DANiel !",
     "histoire":"Un ÉSpadon géant frappe chez JÉRôme qui se LAMente (moustache perdue). ÉZéchias arrive en robe de soirée et appelle DANiel, danseur de lion professionnel."},
    {"nom":"Petits Prophètes (12)","livres":["Osée","Joël","Amos","Abdias","Jonas","Michée","Nahum","Habacuc","Sophonie","Aggée","Zacharie","Malachie"],
     "acronyme":"OS-JO-AM-AB-JON-MI-NA-HA-SO-AG-ZA-MAL",
     "mnemo":"OS du JOuet de l'AMbassadeur sur ABricot, JONquille dans MIroir mange NAvet HAricot en SOurdine, note AG ZA MAL !",
     "histoire":"Diplomate perd l'OS de son jouet. Il atterrit sur un ABricot magique qui fait pousser une JONquille. La fleur mange NAvet et HAricot discrètement (SOurdine). Elle note dans AGenda : ZApper MALette. Police débarque."},
    {"nom":"Les 4 Évangiles","livres":["Matthieu","Marc","Luc","Jean"],
     "acronyme":"MAT-MAR-LU-JE",
     "mnemo":"MATelas dans MARmite de LUciole paie avec JEtons !",
     "histoire":"MAT le matelas bavard glisse dans la MARmite de LUciole chef cuisinière. Pour payer, il donne des JEtons de casino. Le commissaire arrive — c'est aussi un matelas."},
    {"nom":"Actes des Apôtres (1)","livres":["Actes des Apôtres"],
     "acronyme":"ACTES",
     "mnemo":"120 ACrobates à Pentecôte parlent en 17 langues !",
     "histoire":"120 ACrobates débarquent au Temple. Sauts périlleux en 17 langues simultanées. Pierre prend le micro : 'Il est 9h du matin, nous ne sommes pas ivres !' Applaudissements. L'Église est née."},
    {"nom":"Lettres de Paul (13)","livres":["Romains","1 Corinthiens","2 Corinthiens","Galates","Éphésiens","Philippiens","Colossiens","1 Thessaloniciens","2 Thessaloniciens","1 Timothée","2 Timothée","Tite","Philémon"],
     "acronyme":"RO-CO-CO-GA-ÉP-PH-CO-TH-TH-TI-TI-TIT-PHI",
     "mnemo":"ROmains, 2 COrinthiens, GAlates, ÉPhésiens, PHilippiens, COlossiens, 2 THessaloniciens, 2 TImothée, TIte, PHIlémon !",
     "histoire":"Paul-RObot mange 2 COraux et GAteau ÉPhémère. Suit un PHare jusqu'au COlosse géant. Boit 2 THéières, combat 2 TIgres en cravate. Vainqueur : TITon philosophe chauve. Paul écrit tout ça en prison."},
    {"nom":"Lettres Générales (8)","livres":["Hébreux","Jacques","1 Pierre","2 Pierre","1 Jean","2 Jean","3 Jean","Jude"],
     "acronyme":"HÉB-JAC-PI-PI-J-J-J-JU",
     "mnemo":"HÉBergeur, JACquot, 2 PIerres, 3 Jeans, JUde dans même couloir d'hôtel !",
     "histoire":"HÉBergeur gère le chaos : JACquot perroquet réserve 2 chambres pour frères PIerre (qui se disputent lequel est le vrai). 3 cousins prénommés JEAN avec même bagage. JUde arrive avec tambourin. Hôtel ferme."},
    {"nom":"Apocalypse (1)","livres":["Apocalypse"],
     "acronyme":"APOCALYPSE",
     "mnemo":"Grand Finale impossible à oublier : 7 sceaux, dragon, ville en or !",
     "histoire":"Jean exilé sur Patmos. Agneau ouvre 7 sceaux-enveloppes. 7 anges soufflent trompettes désaccordées. Dragon rouge danse la samba. Ville toute en or descend du ciel. Stylo de Jean explose. Rideau."},
]

# ══════════════════════════════════════════════════════════
# BASE DE DONNÉES (Notes personnelles)
# ══════════════════════════════════════════════════════════
DB = "notes.db"

def init_db():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seg_num INTEGER DEFAULT 0,
        titre TEXT, livre TEXT, ref TEXT,
        texte TEXT, note TEXT,
        date TEXT
    )""")
    c.commit(); c.close()

def add_note(sn, titre, livre, ref, texte, note):
    c = sqlite3.connect(DB)
    c.execute("INSERT INTO notes(seg_num,titre,livre,ref,texte,note,date) VALUES(?,?,?,?,?,?,?)",
        (sn, titre, livre, ref, texte, note, datetime.now().strftime("%Y-%m-%d %H:%M")))
    c.commit(); c.close()

def get_notes(seg=0):
    c = sqlite3.connect(DB)
    q = "SELECT * FROM notes"
    if seg > 0: q += f" WHERE seg_num={seg}"
    q += " ORDER BY date DESC"
    r = c.execute(q).fetchall(); c.close(); return r

def del_note(nid):
    c = sqlite3.connect(DB)
    c.execute("DELETE FROM notes WHERE id=?", (nid,))
    c.commit(); c.close()

def get_stats():
    c = sqlite3.connect(DB)
    r = c.execute("SELECT COUNT(*) FROM notes").fetchone()
    c.close(); return r[0]

# ══════════════════════════════════════════════════════════
# IA (optionnel)
# ══════════════════════════════════════════════════════════
def gen_ia(api_key, ref, texte):
    if not ANTHROPIC_OK:
        return None, "Module anthropic non disponible."
    try:
        client = anthropic.Anthropic(api_key=api_key)
        r = client.messages.create(
            model="claude-opus-4-5", max_tokens=700,
            messages=[{"role":"user","content":
                f"Expert mnémotechnique biblique francophone. Pour '{ref}' : '{texte}'\n"
                f"Crée: 1) Mnémotechnique original 2) Histoire loufoque (5 phrases)\n"
                f"JSON uniquement: {{\"mnemo\":\"...\",\"histoire\":\"...\"}}"}])
        import json
        raw = r.content[0].text.strip().replace("```json","").replace("```","")
        d = json.loads(raw)
        return d.get("mnemo",""), d.get("histoire","")
    except Exception as e:
        return None, str(e)

# ══════════════════════════════════════════════════════════
# SESSION
# ══════════════════════════════════════════════════════════
for k,v in [("page","accueil"),("api_key",""),("seg_idx",None)]:
    if k not in st.session_state: st.session_state[k] = v

init_db()

# ══════════════════════════════════════════════════════════
# EN-TÊTE
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
    <div class="app-title">✝️ Bible Memory</div>
    <div class="app-sub">LA VOIE DE L'ABONDANCE ET DE LA PUISSANCE</div>
</div>""", unsafe_allow_html=True)

# NAVIGATION
c1,c2,c3,c4 = st.columns(4)
with c1:
    if st.button("🏠\nAccueil"): st.session_state.page="accueil"
with c2:
    if st.button("📚\nCours"): st.session_state.page="cours"; st.session_state.seg_idx=None
with c3:
    if st.button("📝\nNotes"): st.session_state.page="notes"
with c4:
    if st.button("🗂️\n66 Livres"): st.session_state.page="livres"

st.markdown("<hr style='border-color:#252545;margin:.4rem 0 .8rem;'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE ACCUEIL
# ══════════════════════════════════════════════════════════
if st.session_state.page == "accueil":
    nb_notes = get_stats()
    a,b,c_ = st.columns(3)
    with a: st.markdown(f'<div class="stat-card"><p class="stat-num">12</p><p class="stat-lbl">Segments</p></div>', unsafe_allow_html=True)
    with b: st.markdown(f'<div class="stat-card"><p class="stat-num">66</p><p class="stat-lbl">Livres Bible</p></div>', unsafe_allow_html=True)
    with c_: st.markdown(f'<div class="stat-card"><p class="stat-num">{nb_notes}</p><p class="stat-lbl">Mes Notes</p></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-gold" style="margin-top:.8rem;">
        <div style="color:var(--gold);font-weight:800;font-size:1rem;margin-bottom:.5rem;">
            📖 À Propos de ce Cours
        </div>
        <p style="color:#ddd;font-size:.85rem;line-height:1.7;margin:0;">
        Ce cours biblique en <strong style="color:var(--gold)">12 segments</strong> explore
        la voie que Dieu a tracée pour son peuple :<br><br>
        ✅ <strong>L'Abondance</strong> — Dieu désire que tu prospères physiquement, mentalement et spirituellement.<br>
        ✅ <strong>La Puissance</strong> — La force de manifester la puissance de Dieu dans ta vie.<br>
        ✅ <strong>La Parole</strong> — Notre seule norme de croyance et d'action.<br><br>
        <em style="color:var(--gold);">Jean 14:6 — "Je suis le chemin, la vérité et la vie."</em>
        </p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-title">📚 Les 12 Segments</div>', unsafe_allow_html=True)

    for i in range(0, 12, 2):
        col_a, col_b = st.columns(2)
        for j, col in enumerate([col_a, col_b]):
            idx = i + j
            if idx < 12:
                seg = SEGMENTS[idx]
                with col:
                    st.markdown(f"""
                    <div class="card card-gold" style="padding:.65rem;min-height:75px;">
                        <div style="color:var(--gold);font-size:.68rem;font-weight:800;
                            margin-bottom:3px;">SEGMENT {seg['num']}</div>
                        <div style="color:#fff;font-size:.78rem;font-weight:700;
                            line-height:1.3;">{seg['titre']}</div>
                    </div>""", unsafe_allow_html=True)
                    if st.button("📖 Ouvrir", key=f"h_{idx}"):
                        st.session_state.page = "cours"
                        st.session_state.seg_idx = idx
                        st.rerun()

    st.markdown('<div class="sec-title">🔑 Clé API IA (optionnel)</div>', unsafe_allow_html=True)
    api = st.text_input("Clé Anthropic pour générer des mnémotechniques IA",
        value=st.session_state.api_key, type="password",
        placeholder="sk-ant-...", label_visibility="collapsed")
    if api:
        st.session_state.api_key = api
        st.success("✅ Clé enregistrée pour cette session !")
    st.caption("Sans clé, tous les contenus pré-construits sont disponibles.")

# ══════════════════════════════════════════════════════════
# PAGE COURS
# ══════════════════════════════════════════════════════════
elif st.session_state.page == "cours":

    if st.session_state.seg_idx is not None:
        idx = st.session_state.seg_idx
        seg = SEGMENTS[idx]

        if st.button("← Retour aux segments"):
            st.session_state.seg_idx = None; st.rerun()

        # En-tête du segment
        st.markdown(f"""
        <div class="seg-header">
            <div style="display:flex;align-items:flex-start;gap:.5rem;">
                <div class="seg-num-badge">{seg['num']}</div>
                <div>
                    <div style="color:var(--gold);font-weight:900;font-size:1rem;
                        line-height:1.3;margin-bottom:.4rem;">{seg['titre']}</div>
                    <p style="color:#ccc;font-size:.82rem;line-height:1.6;margin:0;">
                        {seg['intro']}
                    </p>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Vérité clé
        st.markdown(f"""
        <div class="key-truth">
            <span style="color:var(--gold);font-weight:800;">💡 Vérité Clé :</span><br>
            {seg['verite_cle']}
        </div>""", unsafe_allow_html=True)

        # Sections
        for section in seg["sections"]:
            st.markdown(f'<div class="sub-title">📌 {section["titre"]}</div>',
                unsafe_allow_html=True)

            # Contenu de la section
            if section["contenu"]:
                lines = section["contenu"].split('\n')
                content_html = "<br>".join(lines)
                st.markdown(f'<div class="card card-orange" style="font-size:.84rem;color:#ddd;line-height:1.7;">{content_html}</div>',
                    unsafe_allow_html=True)

            # Versets (Louis Segond)
            for v in section["versets"]:
                st.markdown(f"""
                <div class="verse-box">
                    <span class="ref-tag">📖 {v['ref']} — Louis Segond</span>
                    {v['texte']}
                </div>""", unsafe_allow_html=True)

        # Mnémotechnique
        st.markdown('<div class="sec-title">🧠 Mnémotechnique</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mnemo-box">{seg["mnemo"]}</div>', unsafe_allow_html=True)

        # Histoire loufoque
        st.markdown('<div class="sec-title">🎭 Histoire Loufoque</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="story-box">{seg["histoire"]}</div>', unsafe_allow_html=True)

        # Toutes les références du segment
        st.markdown('<div class="sec-title">📌 Toutes les Références</div>', unsafe_allow_html=True)
        all_refs = []
        for s in seg["sections"]:
            all_refs += [v["ref"] for v in s["versets"]]
        st.markdown('<div class="card">' +
            " ".join([f'<span class="ref-pill">{r}</span>' for r in all_refs]) +
            '</div>', unsafe_allow_html=True)

        # Navigation entre segments
        st.markdown("---")
        nav_a, nav_b = st.columns(2)
        with nav_a:
            if idx > 0 and st.button(f"← Segment {idx}"):
                st.session_state.seg_idx = idx - 1; st.rerun()
        with nav_b:
            if idx < 11 and st.button(f"Segment {idx+2} →"):
                st.session_state.seg_idx = idx + 1; st.rerun()

    else:
        st.markdown('<div class="sec-title">📚 Les 12 Segments du Cours</div>',
            unsafe_allow_html=True)
        st.markdown("""
        <div class="card card-green" style="margin-bottom:.8rem;">
            <p style="color:var(--green);font-size:.82rem;margin:0;">
            💡 Appuie sur 📖 pour étudier chaque segment avec ses versets (Louis Segond),
            ses sections détaillées, sa mnémotechnique et son histoire loufoque.
            </p>
        </div>""", unsafe_allow_html=True)

        for seg in SEGMENTS:
            col_info, col_btn = st.columns([5, 1])
            with col_info:
                nb_versets = sum(len(s["versets"]) for s in seg["sections"])
                st.markdown(f"""
                <div class="card card-gold">
                    <div style="display:flex;align-items:flex-start;gap:.5rem;">
                        <div class="seg-num-badge">{seg['num']}</div>
                        <div>
                            <div style="color:#fff;font-weight:700;font-size:.86rem;
                                line-height:1.3;">{seg['titre']}</div>
                            <div style="color:#888;font-size:.72rem;margin-top:3px;">
                                {len(seg['sections'])} sections · {nb_versets} versets Louis Segond
                            </div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if st.button("📖", key=f"s_{seg['num']}"):
                    st.session_state.seg_idx = seg['num'] - 1; st.rerun()

# ══════════════════════════════════════════════════════════
# PAGE NOTES
# ══════════════════════════════════════════════════════════
elif st.session_state.page == "notes":
    st.markdown('<div class="sec-title">📝 Mes Notes Personnelles</div>', unsafe_allow_html=True)

    # Filtre
    opts = ["Toutes"] + [f"Seg {s['num']} — {s['titre'][:30]}..." for s in SEGMENTS]
    sel = st.selectbox("Filtrer", opts, label_visibility="collapsed")
    seg_f = 0 if sel == "Toutes" else int(sel.split(" ")[1])
    notes = get_notes(seg_f)
    st.caption(f"{len(notes)} note(s)")

    if not notes:
        st.markdown("""
        <div class="card" style="text-align:center;padding:1.5rem;">
            <div style="font-size:2.5rem">📭</div>
            <p style="color:#888;margin:.5rem 0 0;">Aucune note. Ajoute-en une ci-dessous !</p>
        </div>""", unsafe_allow_html=True)

    for n in notes:
        nid,sn,titre,livre,ref,texte,note,date = n
        with st.expander(f"{'📌 Seg '+str(sn)+' — ' if sn else ''}{livre} {ref} · {date[:10]}"):
            if texte:
                st.markdown(f'<div class="verse-box"><span class="ref-tag">📖 {livre} {ref}</span>{texte}</div>',
                    unsafe_allow_html=True)
            if note:
                st.markdown(f'<div class="card card-blue" style="margin-top:.4rem;font-size:.84rem;color:#ddd;">'
                    f'<strong style="color:var(--blue)">📝 Ma Note</strong><br>{note}</div>',
                    unsafe_allow_html=True)
            if st.button("🗑️ Supprimer", key=f"dn_{nid}"):
                del_note(nid); st.rerun()

    # Ajouter une note
    st.markdown('<div class="sec-title">➕ Ajouter une Note</div>', unsafe_allow_html=True)
    with st.expander("📝 Nouvelle note"):
        seg_opts = [f"Seg {s['num']} — {s['titre'][:35]}" for s in SEGMENTS] + ["Hors cours"]
        seg_sel = st.selectbox("Segment", seg_opts, key="seg_note")
        sn_n = 0 if seg_sel == "Hors cours" else int(seg_sel.split(" ")[1])
        st_n = "" if sn_n == 0 else SEGMENTS[sn_n-1]["titre"]

        livre_n = st.selectbox("Livre", ALL_BOOKS, key="lv_note")
        ref_n = st.text_input("Référence", placeholder="ex: 14:6", key="ref_note")
        texte_n = st.text_area("Texte du verset", placeholder="Colle le texte ici...",
            height=80, key="tx_note")
        note_n = st.text_area("Ma note personnelle", placeholder="Ma réflexion, commentaire...",
            height=80, key="nt_note")

        gen_cb = st.checkbox("🤖 Générer mnémotechnique IA", key="gen_note",
            value=bool(st.session_state.api_key))

        if st.button("💾 Enregistrer", key="save_note"):
            if not ref_n.strip():
                st.error("❌ La référence est obligatoire !")
            else:
                note_finale = note_n.strip()
                if gen_cb and st.session_state.api_key and texte_n.strip():
                    with st.spinner("🧠 Génération IA..."):
                        m, h = gen_ia(st.session_state.api_key,
                            f"{livre_n} {ref_n}", texte_n)
                    if m:
                        note_finale += f"\n\n🧠 Mnémotechnique IA:\n{m}\n\n🎭 Histoire:\n{h}"
                    else:
                        st.warning(f"IA indisponible: {h}")
                add_note(sn_n, st_n, livre_n, ref_n.strip(),
                    texte_n.strip(), note_finale)
                st.success(f"✅ {livre_n} {ref_n} enregistré !"); st.rerun()

# ══════════════════════════════════════════════════════════
# PAGE 66 LIVRES
# ══════════════════════════════════════════════════════════
elif st.session_state.page == "livres":
    st.markdown('<div class="sec-title">🗂️ Les 66 Livres de la Bible</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-green">
        <p style="color:var(--green);font-weight:700;margin:0 0 .3rem;">🎯 Méthode Globale</p>
        <p style="color:#ddd;font-size:.82rem;margin:0;line-height:1.7;">
        <strong>AT (39)</strong> = 5+12+5+5+12 livres<br>
        <strong>NT (27)</strong> = 4+1+13+8+1 livres<br>
        <strong style="color:var(--gold);">📌 39+27=66 · 3×9=27 ✓</strong>
        </p>
    </div>""", unsafe_allow_html=True)

    with st.expander("🔢 Les 66 livres dans l'ordre"):
        for i, bk in enumerate(ALL_BOOKS):
            col = "#E94560" if i >= 39 else "var(--gold)"
            st.markdown(f"""
            <div style="display:flex;padding:3px 0;border-bottom:1px solid #1a1a35;">
                <span style="color:{col};font-weight:800;width:28px;font-size:.78rem;">{i+1}</span>
                <span style="color:#ddd;font-size:.83rem;">{bk}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a1a2e,#0a0a18);border-radius:12px;
        padding:.7rem;margin:1rem 0 .3rem;border:2px solid var(--gold);">
        <h3 style="color:var(--gold);margin:0;font-size:1.1rem;">✡️ Ancien Testament — 39 Livres</h3>
    </div>""", unsafe_allow_html=True)

    at_groups = GROUPES_BIBLE[:5]
    for g in at_groups:
        with st.expander(f"📂 {g['nom']}"):
            st.markdown(f"""
            <div class="card card-purple" style="margin-bottom:.4rem;">
                <strong style="color:var(--purple)">🔤 Acronyme</strong><br>
                <span style="color:var(--gold);font-size:.95rem;font-weight:800;
                    letter-spacing:2px;">{g['acronyme']}</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="mnemo-box"><strong>💡</strong> {g["mnemo"]}</div>',
                unsafe_allow_html=True)
            st.markdown(f'<div class="story-box" style="margin-top:.4rem;"><strong>🎭</strong> {g["histoire"]}</div>',
                unsafe_allow_html=True)
            first = g["livres"][0]
            start = ALL_BOOKS.index(first) + 1 if first in ALL_BOOKS else 1
            for i, bk in enumerate(g["livres"]):
                st.markdown(f"""
                <div style="display:flex;align-items:center;padding:3px 8px;
                    margin:2px 0;background:#1a1a35;border-radius:8px;">
                    <span style="color:var(--gold);font-weight:900;width:28px;
                        font-size:.78rem;">#{start+i}</span>
                    <span style="color:#fff;font-size:.85rem;font-weight:600;">{bk}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a0a1a,#0a0a18);border-radius:12px;
        padding:.7rem;margin:1rem 0 .3rem;border:2px solid var(--accent);">
        <h3 style="color:var(--accent);margin:0;font-size:1.1rem;">✝️ Nouveau Testament — 27 Livres</h3>
    </div>""", unsafe_allow_html=True)

    nt_groups = GROUPES_BIBLE[5:]
    for g in nt_groups:
        with st.expander(f"📂 {g['nom']}"):
            st.markdown(f"""
            <div class="card card-red" style="margin-bottom:.4rem;">
                <strong style="color:var(--accent)">🔤 Acronyme</strong><br>
                <span style="color:var(--gold);font-size:.95rem;font-weight:800;
                    letter-spacing:2px;">{g['acronyme']}</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="mnemo-box"><strong>💡</strong> {g["mnemo"]}</div>',
                unsafe_allow_html=True)
            st.markdown(f'<div class="story-box" style="margin-top:.4rem;"><strong>🎭</strong> {g["histoire"]}</div>',
                unsafe_allow_html=True)
            first = g["livres"][0]
            start = ALL_BOOKS.index(first) + 1 if first in ALL_BOOKS else 40
            for i, bk in enumerate(g["livres"]):
                st.markdown(f"""
                <div style="display:flex;align-items:center;padding:3px 8px;
                    margin:2px 0;background:#1a0a2a;border-radius:8px;">
                    <span style="color:var(--accent);font-weight:900;width:28px;
                        font-size:.78rem;">#{start+i}</span>
                    <span style="color:#fff;font-size:.85rem;font-weight:600;">{bk}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-gold" style="margin-top:.8rem;text-align:center;padding:1rem;">
        <div style="font-size:1.5rem">🏆</div>
        <p style="color:var(--gold);font-weight:800;margin:.2rem 0;">Grand Défi !</p>
        <p style="color:#ddd;font-size:.8rem;margin:0;line-height:1.8;">
        <strong style="color:var(--green)">1.</strong> 5 groupes AT<br>
        <strong style="color:var(--green)">2.</strong> 5 groupes NT<br>
        <strong style="color:var(--green)">3.</strong> Chaque acronyme<br>
        <strong style="color:var(--gold)">🎯 66 livres en 2 minutes !</strong>
        </p>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<hr style='border-color:#1a1a35;margin:.8rem 0 .3rem;'>
<div style='text-align:center;color:#333;font-size:.7rem;'>
    ✝️ Bible Memory · La Voie de l'Abondance et de la Puissance · Louis Segond
</div>""", unsafe_allow_html=True)
