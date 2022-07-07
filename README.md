# north-indian-dialect-modelling

This project consists of four stages:

## Data Collection for "dialects" in the North Indian "Hindi belt".

We crawl data from [Kavita Kosh](http://kavitakosh.org/) for 31 languages. We have been authorized to release only part of this data; however, our crawler is available to use in [here](crawlers/).

## Probing Data

We perform experiments over the collected data to test cross-lingual relationships in the continuum. See [here](stats/).

## Collecting Evaluation Data

We collect evaluation data for cognate induction in the form of bilingual lexicons for 19 of the languages under consideration with Hindi, from [Languages Home](http://languageshome.com/). We cannot make this data available due to copyright reasons; however, our processing pipeline is fully automatic and can be run by anyone on raw data that is manually downloaded from this website. See [here](https://github.com/niyatibafna/north-indian-dialect-modelling/tree/main/evaluation_languages_home) for more details.

## Cognate Induction

We explore methods of cognate induction for each of the languages against Hindi. We try four main approaches, using combinations of orthographic cues and semantic cues with bilingual embeddings. See ...
