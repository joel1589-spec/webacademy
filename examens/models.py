from django.db import models

from comptes.models import Etudiant


class Sujet(models.Model):
    """Un sujet d'interrogation ou de devoir, créé par le formateur depuis l'admin."""

    titre = models.CharField("Titre", max_length=200)
    consignes = models.TextField(
        "Consignes", blank=True,
        help_text="Instructions générales affichées en haut du sujet (optionnel).",
    )
    duree_minutes = models.PositiveIntegerField(
        "Durée accordée (en minutes)",
        help_text="Temps laissé à l'apprenant à partir du moment où il ouvre le sujet.",
    )
    actif = models.BooleanField(
        "Visible par les apprenants", default=False,
        help_text="Décoche pour cacher le sujet pendant que tu le prépares.",
    )
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        verbose_name = "Sujet"
        verbose_name_plural = "Sujets"
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

    @property
    def note_totale(self):
        return sum(q.points for q in self.questions.all())

    @property
    def nombre_questions(self):
        return self.questions.count()


class Question(models.Model):
    QCM = 'qcm'
    VRAI_FAUX = 'vf'
    REPONSE_COURTE = 'courte'
    CHOIX_TYPE = [
        (QCM, "Choix multiples (QCM)"),
        (VRAI_FAUX, "Vrai / Faux"),
        (REPONSE_COURTE, "Réponse courte"),
    ]

    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='questions', verbose_name="Sujet")
    type_question = models.CharField("Type de question", max_length=10, choices=CHOIX_TYPE, default=QCM)
    enonce = models.TextField("Énoncé de la question")
    points = models.PositiveIntegerField("Points", default=1)
    ordre = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['ordre', 'id']

    def __str__(self):
        return f"{self.sujet.titre} — Q{self.ordre + 1}"


class Choix(models.Model):
    """Une option de réponse pour une question QCM ou Vrai/Faux."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choix_possibles', verbose_name="Question")
    texte = models.CharField("Texte de l'option", max_length=255)
    est_correct = models.BooleanField("C'est une bonne réponse", default=False)
    ordre = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Choix"
        verbose_name_plural = "Choix"
        ordering = ['ordre', 'id']

    def __str__(self):
        return f"{'✓' if self.est_correct else '✗'} {self.texte}"


class ReponseAcceptee(models.Model):
    """Pour une question à réponse courte : une formulation acceptée comme correcte."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses_acceptees', verbose_name="Question")
    texte = models.CharField(
        "Réponse acceptée", max_length=255,
        help_text="La comparaison ignore les majuscules/minuscules et les espaces en trop.",
    )

    class Meta:
        verbose_name = "Réponse acceptée"
        verbose_name_plural = "Réponses acceptées"

    def __str__(self):
        return self.texte


class Copie(models.Model):
    """La tentative d'un apprenant sur un sujet (une seule tentative autorisée par sujet)."""

    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='copies', verbose_name="Sujet")
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='copies', verbose_name="Apprenant")
    date_debut = models.DateTimeField("Commencé le", auto_now_add=True)
    date_soumission = models.DateTimeField("Soumis le", null=True, blank=True)
    terminee = models.BooleanField("Corrigée / terminée", default=False)
    note_obtenue = models.FloatField("Note obtenue", null=True, blank=True)

    class Meta:
        verbose_name = "Copie"
        verbose_name_plural = "Copies"
        unique_together = [('sujet', 'etudiant')]
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.etudiant} — {self.sujet.titre}"

    @property
    def note_sur(self):
        return self.sujet.note_totale


class ReponseEtudiant(models.Model):
    """La réponse d'un apprenant à une question donnée, au sein d'une copie."""

    copie = models.ForeignKey(Copie, on_delete=models.CASCADE, related_name='reponses', verbose_name="Copie")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses_etudiants', verbose_name="Question")
    choix_selectionnes = models.ManyToManyField(Choix, blank=True, verbose_name="Choix sélectionné(s)")
    texte_libre = models.TextField("Réponse libre", blank=True)
    points_obtenus = models.FloatField("Points obtenus", default=0)

    class Meta:
        verbose_name = "Réponse d'apprenant"
        verbose_name_plural = "Réponses d'apprenants"
        unique_together = [('copie', 'question')]

    def __str__(self):
        return f"Réponse de {self.copie.etudiant} à Q{self.question.ordre + 1}"
