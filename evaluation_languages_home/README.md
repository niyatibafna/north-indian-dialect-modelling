# Collecting Evaluation Data

We collect parallel sentences from [Languages Home](https://www.languageshome.com) and use an automatic pipeline to transliterate and re-align them, 
and then extract word alignments.

Unfortunately, we cannot release the resulting lexicons due to copyrights on the above website. 
However, we provide the pipeline here; it can be run using a single command on raw data downloaded from the website.


## Obtaining raw data

The pipeline expects the data in directory:

```eval_data/raw/```

The directory should contain a single file with raw data (for example) manually copied and pasted from the website. For example, ```awadhi.txt```, ```bundeli.txt```. 
(See table below for languages that we worked on.)

## Running the pipeline

### Requirements

The pipeline requires:

* [```fast_align```](https://github.com/clab/fast_align), should be cloned in ```../fast_align```. 
If required, the path to the clone can be set in ```processing_scripts/processing/read_alignments_all_hin.sh```,
by modifying the variable ```$FA_DIR```.

* [indictrans](https://github.com/libindic/indic-trans), cloned and installed.

### Running

Once the data are requirements are in place, the pipeline can be run like this:

```cd processing_scripts/processing/ ```

```bash processing_pipeline.sh```

### Resulting Lexicons

Here is a summary of the resulting lexicons:

| Language     | Total in test | Unique in test |
|--------------|---------------|----------------|
| brajbhasha   | 299           | 161            |
| angika       | 310           | 165            |
| maithili     | 273           | 147            |
| magahi       | 326           | 172            |
| awadhi       | 281           | 145            |
| rajasthani   | 312           | 161            |
| hariyanvi    | 298           | 156            |
| bhil         | 319           | 177            |
| chattisgarhi | 267           | 134            |
| nepali       | 203           | 118            |
| bajjika      | 317           | 149            |
| koraku       | 262           | 132            |
| malwi        | 325           | 163            |
| sindhi       | 250           | 141            |
| bhojpuri     | 303           | 146            |
| garwali      | 275           | 161            |
| marathi      | 230           | 130            |
| kumaoni      | 250           | 171            |
| bundeli      | 272           | 147            |

The last column records the number of unique Hindi source words that have an alignment in the respective target language. 
There are also other languages on the website than these; they can be processed in the same way.
