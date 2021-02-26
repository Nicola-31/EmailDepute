#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Exemple pris depuis https://sametmax.com/creer-un-setup-py-et-mettre-sa-bibliotheque-python-en-ligne-sur-pypi/

from setuptools import setup, find_packages

import EmailDepute

setup(

    # le nom de votre biblioth�que, tel qu'il apparaitre sur pypi
    name='EmailDepute',

    # la version du code
    version=EmailDepute.__version__,

    # Liste les packages � ins�rer dans la distribution
    # plut�t que de le faire � la main, on utilise la foncton
    # find_packages() de setuptools qui va cherche tous les packages
    # python recursivement dans le dossier courant.
    # C'est pour cette raison que l'on a tout mis dans un seul dossier:
    # on peut ainsi utiliser cette fonction facilement
    packages=find_packages(),

    # votre pti nom
    author="Nicolas Jeudy",

    # Votre email, sachant qu'il sera publique visible, avec tous les risques
    # que �a implique.
    author_email="nicola.jeudy@gmail.com",

    # Une description courte
    description="R�cup�rer les adresses email des d�put�s de l'assembl�e nationale francaise",

    # Une description longue, sera affich�e pour pr�senter la lib
    # G�n�ralement on dump le README ici
    long_description=open('README.rst').read(),

    # Vous pouvez rajouter une liste de d�pendances pour votre lib
    # et m�me pr�ciser une version. A l'installation, Python essayera de
    # les t�l�charger et les installer.
    #
    # Ex: ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
    #
    # Dans notre cas on en a pas besoin, donc je le commente, mais je le
    # laisse pour que vous sachiez que �a existe car c'est tr�s utile.
    # install_requires= ,

    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,

    # Une url qui pointe vers la page officielle de votre lib
    url='https://github.com/Nicola-31/EmailDepute.git',

    # Il est d'usage de mettre quelques metadata � propos de sa lib
    # Pour que les robots puissent facilement la classer.
    # La liste des marqueurs autoris�es est longue:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    #
    # Il n'y a pas vraiment de r�gle pour le contenu. Chacun fait un peu
    # comme il le sent. Il y en a qui ne mettent rien.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Democracy",
    ],


    # C'est un syst�me de plugin, mais on s'en sert presque exclusivement
    # Pour cr�er des commandes, comme "django-admin".
    # Par exemple, si on veut cr�er la fabuleuse commande "proclame-sm", on
    # va faire pointer ce nom vers la fonction proclamer(). La commande sera
    # cr�� automatiquement.
    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    #entry_points = {
    #    'console_scripts': [
    #        'proclame-sm = sm_lib.core:proclamer',
    #    ],
    #},

    # A fournir uniquement si votre licence n'est pas list�e dans "classifiers"
    # ce qui est notre cas
    license="WTFPL",

    # Il y a encore une chi�e de param�tres possibles, mais avec �a vous
    # couvrez 90% des besoins

)
