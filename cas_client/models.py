from django.db import models
from django.contrib.auth.models import User

DEPARTMENT_CHOICES = (
    ('16',  'Aeronautics & Astronautics'),
    ('21A', 'Anthropology'),
    ('4',   'Architecture'),
    ('20',  'Biological Engineering'),
    ('7',   'Biology'),
    ('9',   'Brain and Cognitive Sciences'),
    ('15',  'Management'),
    ('10',  'Chemical Engineering'),
    ('5',   'Chemistry'),
    ('1',   'Civil and Environmental Engineering'),
    ('21W', 'Writing'),
    ('12',  'Earth, Atmospheric and Planetary Sciences'),
    ('14',  'Economics'),
    ('6',   'Electrical Engineering and Computer Science'),
    ('ESD', 'Engineering Systems Division'),
    ('21F', 'Foreign Languages and Literatures'),
    ('HST', 'Health Sciences and Technology'),
    ('21H', 'History'),
    ('24',  'Linguistics and Philosophy'),
    ('21L', 'Literature'),
    ('3',   'Materials Science and Engineering'),
    ('18',  'Mathematics'),
    ('2',   'Mechanical Engineering'),
    ('MAS', 'Media Arts and Sciences'),
    ('21M', 'Music and Theater Arts'),
    ('22',  'Nuclear Science and Engineering'),
    ('ORC', 'Operations Research Center'),
    ('8',   'Physics'),
    ('17',  'Political Science'),
    ('STS', 'Science, Technology, and Society'),
    ('11',  'Urban Studies and Planning'),     
    ('WGS', 'Women and Gender Studies'),     
)

DEPARTMENT_CHOICES_DICT = {
    '16':  'Aeronautics & Astronautics',
    '21A': 'Anthropology',
    '4':   'Architecture',
    '20':  'Biological Engineering',
    '7':   'Biology',
    '9':   'Brain and Cognitive Sciences',
    '15':  'Management',
    '10':  'Chemical Engineering',
    '5':   'Chemistry',
    '1':   'Civil and Environmental Engineering',
    '21W': 'Writing',
    '12':  'Earth, Atmospheric and Planetary Sciences',
    '14':  'Economics',
    '6':   'Electrical Engineering and Computer Science',
    'ESD': 'Engineering Systems Division',
    '21F': 'Foreign Languages and Literatures',
    'HST': 'Health Sciences and Technology',
    '21H': 'History',
    '24':  'Linguistics and Philosophy',
    '21L': 'Literature',
    '3':   'Materials Science and Engineering',
    '18':  'Mathematics',
    '2':   'Mechanical Engineering',
    'MAS': 'Media Arts and Sciences',
    '21M': 'Music and Theater Arts',
    '22':  'Nuclear Science and Engineering',
    'ORC': 'Operations Research Center',
    '8':   'Physics',
    '17':  'Political Science',
    'STS': 'Science, Technology, and Society',
    '11':  'Urban Studies and Planning',     
    'WGS': 'Women and Gender Studies',     
}

class Department(models.Model):

    name = models.CharField(max_length=3,
                            choices = DEPARTMENT_CHOICES,
                            blank=True,
                            null=True)
    def __unicode__(self):
        return str(self.name).ljust(5) + DEPARTMENT_CHOICES_DICT[self.name]

class Subject(models.Model):
    number        = models.CharField(max_length=10)
    name          = models.CharField(max_length=60)
    description   = models.CharField(max_length=1200, blank=True, null=True)
    creator       = models.ForeignKey(User, related_name='subjects_creator')
    instructors   = models.ManyToManyField(User, related_name='subjects_instructors', blank=True, null=True)
    TERM_CHOICES = (
        ('S', 'Spring'),
        ('F', 'Fall'),
        ('I', 'IAP'),
    )
    term          = models.CharField(max_length=1,
                                     choices = TERM_CHOICES,
                                     blank=True,
                                     null=True)
    YEAR_CHOICES = (
        ('2010', '2010'),
        ('2011', '2011'),
        ('2012', '2012'),
        ('2013', '2013'),
        ('2014', '2014'),
        ('2015', '2015'),
    )
    year          = models.CharField(max_length=4,
                                     choices = YEAR_CHOICES,
                                     blank=True,
                                     null=True)
    prerequisites = models.ManyToManyField('self', related_name='postrequisites', blank=True, null=True, symmetrical=False)
    def __unicode__(self):
        return str(self.number).ljust(7) + self.name



class Keyword(models.Model):
    name     = models.CharField(max_length=40)
    class Meta:
		ordering = ['name']
    def __unicode__(self):
        return self.name

class Module(models.Model):
    name          = models.CharField(max_length=60)
    description   = models.CharField(max_length=600, blank=True, null=True)
    creator       = models.ForeignKey(User, related_name='modules_creator')
    instructors   = models.ManyToManyField(User, related_name='modules_instructors', blank=True, null=True)
    subjects      = models.ManyToManyField(Subject, blank=True, null=True)
    def __unicode__(self):
        return self.name

class Outcome(models.Model):
    name          = models.CharField(max_length=40)
    description   = models.CharField(max_length=400)
    creator       = models.ForeignKey(User, related_name='outcomes_creator')
    instructors   = models.ManyToManyField(User, related_name='outcomes_intructors', blank=True, null=True)
    prerequisites = models.ManyToManyField('self', related_name='postrequisites', blank=True, null=True, symmetrical=False)
    modules       = models.ManyToManyField(Module, blank=True, null=True)
    subjects      = models.ManyToManyField(Subject, blank=True, null=True)
    departments   = models.ManyToManyField(Department, blank=True, null=True)
    keywords      = models.ManyToManyField(Keyword, blank=True, null=True)
    def __unicode__(self):
        return self.name
