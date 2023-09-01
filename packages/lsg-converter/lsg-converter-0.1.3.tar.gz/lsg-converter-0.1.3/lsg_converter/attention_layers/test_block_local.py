from block_local_self_attention import *
import torch 
"""
n, h, t, d = 2, 4, 58, 32
Q, K, V = torch.randn(n, h, t, d), torch.randn(n, h, t, d), torch.randn(n, h, t, d)
attention_mask = torch.zeros(n, 1, 1, t).float()

attn = BlockLocalSelfAttention(16)

outputs = attn(Q, K, V, attention_mask)
print(outputs.shape)

n, h, t, d = 2, 4, 58, 32
Q, K, V = torch.randn(n, h, t, d), torch.randn(n, h, t, d), torch.randn(n, h, t, d)
attention_mask = torch.zeros(n, 1, 1, t).float()

attn = BlockLocalSelfAttention(16, is_causal=True)

outputs = attn(Q, K, V, attention_mask=None)
print(outputs.shape)
"""

from transformers import AutoModelForTokenClassification, AutoModelForSequenceClassification, AutoTokenizer, pipeline

text = "George Washington est allé à washington." * 20
path = "Jean-Baptiste/camembert-ner"

text = """
Si vous cherchez du cinéma abrutissant à tous les étages,n'ayant aucune peur du cliché en castagnettes et moralement douteux,"From Paris with love" est fait pour vous.Toutes les productions Besson,via sa filière EuropaCorp ont de quoi faire naître la moquerie.Paris y est encore une fois montrée comme une capitale exotique,mais attention si l'on se dirige vers la banlieue,on y trouve tout plein d'intégristes musulmans prêts à faire sauter le caisson d'une ambassadrice américaine.Nauséeux.Alors on se dit qu'on va au moins pouvoir apprécier la déconnade d'un classique buddy-movie avec le jeune agent aux dents longues obligé de faire équipe avec un vieux lou complètement timbré.Mais d'un côté,on a un Jonathan Rhys-meyers fayot au possible,et de l'autre un John Travolta en total délire narcissico-badass,crâne rasé et bouc proéminent à l'appui.Sinon,il n'y a aucun scénario.Seulement,des poursuites débiles sur l'autoroute,Travolta qui étale 10 mecs à l'arme blanche en 8 mouvements(!!)ou laisse son associé se faire démolir la tronche pendant qu'il scrute à la jumelle.Ca pourrait être un plaisir coupable,tellement c'est "hénaurme",c'est juste de la daube dans la droite lignée d'un "Transporteur","Taken"ou "Banlieue 13."
"""
text = """
Non mais c'est une blague ? C'est quoi toutes ces critiques positives ??? "Premium rush" est carrément ridicule et est dénué de toute crédibilité. Un film pour adolescents avec un semblant de scénario qui demeure nullissime. Tout est mal emmené, les dialogues sont pauvres, on n'y croit pas une seconde, on assiste à une course poursuite de 90 minutes avec un suspens dont on se fout éperdument. Deux bons acteurs (Gordon-Levitt & Shannon) pour un long-métrage où l'arrivée du générique final se fait attendre au plus vite afin d'en terminer avec ce film qui ne cesse de tourner en rond.Entre Michel qui nous fait du trial avec ses côtes cassées, un vélo qui accélère plus vite qu'une belle bagnole luxueuse, une fin totalement ridicule avec un gang de bikers, et j'en passe...bref du cyclisme héroïque qui ne sert à rien."""

text = """
Derrière Le Miroir est un véritable chef-d’oeuvre des années 50 signé Nicholas Ray que j’ai découvert encore une fois grâce à Scorsese qui parle du film dans son voyage à travers le cinéma américain. Le titre original Bigger Than Life est plus explicite et nous montre déjà les ambitions exacerbés dont va souffrir notre personnage principal. Celui-ci est incarné par un James Mason magistral qui signe une des ses meilleurs performances en incarnant cet homme sombrant dans la folie. La réalisation est superbe, le travelling d’entrée de film donne le ton avec un cinemascope pourtant peu utilisé pour les drames psychologiques à l’époque, on retiendra également les plans du traitement à la cortisone à l’hopital et d’autres. La bande originale n’est pas mémorable mais souligne bien l’image grâce au travail de David Raksin. Certains regretteront peut-être une fin trop positive mais c’est un détail par rapport à la qualité du reste du film qu’il serait dommage de porter préjudice au film pour cela."""

path = "alosof/camembert-sentiment-allocine"

model = AutoModelForSequenceClassification.from_pretrained(path, from_tf=True)
tokenizer = AutoTokenizer.from_pretrained(path)
pipe = pipeline("text-classification", model=model, tokenizer=tokenizer)

outputs = pipe(text)
print(outputs)

from transformers.models.camembert import modeling_camembert

class NewCamembertSelfAttention(modeling_camembert.CamembertSelfAttention):

    def __init__(self, config, position_embedding_type=None):

        super().__init__(config, position_embedding_type=position_embedding_type)
        self.local_attn = BlockLocalSelfAttention(64)

    def forward(
        self,
        hidden_states,
        attention_mask = None,
        head_mask = None,
        encoder_hidden_states = None,
        encoder_attention_mask = None,
        past_key_value = None,
        output_attentions = False,
    ):
        mixed_query_layer = self.query(hidden_states)
        key_layer = self.transpose_for_scores(self.key(hidden_states))
        value_layer = self.transpose_for_scores(self.value(hidden_states))
        query_layer = self.transpose_for_scores(mixed_query_layer)

        
        context_layer = self.local_attn(query_layer, key_layer, value_layer, attention_mask)
        context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
        new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)
        context_layer = context_layer.view(new_context_layer_shape)
        outputs = (context_layer,)

        return outputs

modeling_camembert.CamembertSelfAttention = NewCamembertSelfAttention

from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

text = "George Washington est allé à washington." * 20
path = "Jean-Baptiste/camembert-ner"

text = """
Si vous cherchez du cinéma abrutissant à tous les étages,n'ayant aucune peur du cliché en castagnettes et moralement douteux,"From Paris with love" est fait pour vous.Toutes les productions Besson,via sa filière EuropaCorp ont de quoi faire naître la moquerie.Paris y est encore une fois montrée comme une capitale exotique,mais attention si l'on se dirige vers la banlieue,on y trouve tout plein d'intégristes musulmans prêts à faire sauter le caisson d'une ambassadrice américaine.Nauséeux.Alors on se dit qu'on va au moins pouvoir apprécier la déconnade d'un classique buddy-movie avec le jeune agent aux dents longues obligé de faire équipe avec un vieux lou complètement timbré.Mais d'un côté,on a un Jonathan Rhys-meyers fayot au possible,et de l'autre un John Travolta en total délire narcissico-badass,crâne rasé et bouc proéminent à l'appui.Sinon,il n'y a aucun scénario.Seulement,des poursuites débiles sur l'autoroute,Travolta qui étale 10 mecs à l'arme blanche en 8 mouvements(!!)ou laisse son associé se faire démolir la tronche pendant qu'il scrute à la jumelle.Ca pourrait être un plaisir coupable,tellement c'est "hénaurme",c'est juste de la daube dans la droite lignée d'un "Transporteur","Taken"ou "Banlieue 13."
"""
text = """
Non mais c'est une blague ? C'est quoi toutes ces critiques positives ??? "Premium rush" est carrément ridicule et est dénué de toute crédibilité. Un film pour adolescents avec un semblant de scénario qui demeure nullissime. Tout est mal emmené, les dialogues sont pauvres, on n'y croit pas une seconde, on assiste à une course poursuite de 90 minutes avec un suspens dont on se fout éperdument. Deux bons acteurs (Gordon-Levitt & Shannon) pour un long-métrage où l'arrivée du générique final se fait attendre au plus vite afin d'en terminer avec ce film qui ne cesse de tourner en rond.Entre Michel qui nous fait du trial avec ses côtes cassées, un vélo qui accélère plus vite qu'une belle bagnole luxueuse, une fin totalement ridicule avec un gang de bikers, et j'en passe...bref du cyclisme héroïque qui ne sert à rien."""
text = """
Derrière Le Miroir est un véritable chef-d’oeuvre des années 50 signé Nicholas Ray que j’ai découvert encore une fois grâce à Scorsese qui parle du film dans son voyage à travers le cinéma américain. Le titre original Bigger Than Life est plus explicite et nous montre déjà les ambitions exacerbés dont va souffrir notre personnage principal. Celui-ci est incarné par un James Mason magistral qui signe une des ses meilleurs performances en incarnant cet homme sombrant dans la folie. La réalisation est superbe, le travelling d’entrée de film donne le ton avec un cinemascope pourtant peu utilisé pour les drames psychologiques à l’époque, on retiendra également les plans du traitement à la cortisone à l’hopital et d’autres. La bande originale n’est pas mémorable mais souligne bien l’image grâce au travail de David Raksin. Certains regretteront peut-être une fin trop positive mais c’est un détail par rapport à la qualité du reste du film qu’il serait dommage de porter préjudice au film pour cela."""


path = "alosof/camembert-sentiment-allocine"

model = AutoModelForSequenceClassification.from_pretrained(path, from_tf=True)
tokenizer = AutoTokenizer.from_pretrained(path)
pipe = pipeline("text-classification", model=model, tokenizer=tokenizer)

outputs = pipe(text)
print(outputs)