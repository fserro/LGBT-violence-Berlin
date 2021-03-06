# LGBT-violence-Berlin
Mapping LGBT violence in Berlin

The goal of this project is to gather available data on the topic, map the incidents and to display it in an interactive interface with Streamlit. While the idea is to gather data from different sources, this first version works with only one: the Berliner Register website, which has been systematically tracking right-wing extremist and discriminatory incidents in Berlin  since 2014. 
The almost 22,000 recorded incidents extracted from the Berliner Register cover a period until 01.06.2021 and concern all kinds of public manifestations of hate and aggression in Berlin. There's racism, antisemitism, islamophobia, xenophobia... It also includes all types of violence: from stickers and graffiti promoting hate speech, to harassment and physical aggression. I used Regular Expressions to extract only the incidents concerning the LGBTQIA* community, which reduced the data points to just over 1000 incidents. After analyzing the data, I decided it made sense to classify them in the the following system:

- Attack (against individuals):
    - physical (or physical + verbal)
    - verbal
- Propaganda (against community):
    - stickers, graffiti, banners, etc.
    - speeches by individuals and politicians, incl. in the municipal assemblies (Bezirksverordnetenversammlung, or BVV)
    - public expressions (oral and written) in media and online
- Vandalism:
    - graffiti, damaging of LGBTQIA* symbols, memorials, plaques...
- Structural Discrimination:
   - in workplace or public/private institutions

The locations of the incidents were determined using SpaCy and the coordinates using GeoPy.

The categorization of the stories is still underway...

What to do Next:

- Finish labelling the data
- Figuring out a way to disambiguate locations
- Adding an input form so visitors can report new cases
- Find data from other sources
- Train an NLP model with the labeled data to automatically detect if new incidents are relevant for this project
- Make a pipeline so new incidents can be added automatically

![lgbt_preview](https://user-images.githubusercontent.com/77271778/132096390-209759bf-5fe2-4734-8457-10bdc188b626.gif)
