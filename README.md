# Speech-to-maths

Speech-recognition for Latex generation project.

Second year project at [Ecole Polytechnique](https://www.polytechnique.edu/fr). This repo contains:

- A Django web-server with a working interface, including document, user management and audio communication

![User interface](https://lh3.googleusercontent.com/Zf4rV1Vzp_o6Tvx1rOqkw1Uo20FV0ppzOWunrNkNBRPlWz9qGNSPJzxrQDOCw390ZtSddcmePwEnvOdTIUwupx0JsTWjvXkIDx-kE-OkaMNUhF4zdvbBVKci5RIx3_AJ_IJ9HUnB)

- A speech recognition module using [CMUSphinx](https://cmusphinx.github.io/), with a custom grammar
- A custom implementation of the Myers algorithm for parsing mathematical formulae

![Example parse tree](https://lh6.googleusercontent.com/7rBHwPL0MU5rDrxCHdrMP_czrqxA_UbWV5_ac2VoAVrM6LW8qg4xHO0hkLBxR2C999B9MDxvOXvHRD4jBcL7-ZYRSQeJzHTiY_2z2c8z6bwH0gNsaju31EKCcR17Q7KJ5Ia4LcSl)

- ML wrapper for formula (tree) choice based on multiple heuristics
  - Combines global model and custom models _per document_ and _per user_

[Link to the final presentation](https://docs.google.com/presentation/d/e/2PACX-1vTiLNwtbUx39xA1unaswkmVvFD2bo6jYkQH8zcLtenalXyswm6lKN0qxGdOzfX24FhMZedREFTg3RXz/pub?start=false&loop=false&delayms=3000) (in French).

[Link to the final report](https://docs.google.com/document/d/e/2PACX-1vQHP_5PPMeASZCQMpPGnOkd9Ehy3QPG-Z25J2kN4DH0PpWaS7RoGe-IfMJroXc8PbtbvD6f4fdBJ9w7/pub) (in French).

Project by [Garance Cordonnier](https://www.linkedin.com/in/garance-cordonnier-22150a150/), [Loïs Faisant](https://www.linkedin.com/in/lo%C3%AFs-faisant-27bb82150/), [François Hublet](https://www.linkedin.com/in/fran%C3%A7ois-hublet-6500a2a2/), Baptiste Mourrain, [Haris Sahovic](https://github.com/hsahovic), [Fabrice Serret](https://www.linkedin.com/in/fserret/) and [Yolène Vanhaesbroucke](https://www.linkedin.com/in/yol%C3%A8ne-vanhaesbroucke-261006151/).
