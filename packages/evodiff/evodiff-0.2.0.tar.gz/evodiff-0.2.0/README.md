# EvoDiff

### Description
In this work, we exploit sequence as the universal design space for proteins to develop a general-purpose deep learning framework for controllable protein generation. We introduce a diffusion modeling framework, EvoDiff, that combines evolutionary-scale data with the distinct conditioning capabilities of diffusion models to achieve controllable protein design in sequence space alone. EvoDiff generates high-fidelity, diverse, and structurally-plausible proteins that fully cover natural sequence and functional space. By operating in the universal protein design space, EvoDiff can generate disordered regions and scaffold functional structural motifs without any explicit structural information. We envision that EvoDiff will expand capabilities in protein engineering beyond the structure-function paradigm towards programmable, sequence-first design.

----

# Table of contents

- [Evodiff](#EvoDiff)
  - [Description](#description)
- [Table of contents](#table-of-contents)
- [Installation](#installation)
    - [Data](#data)
    - [Loading pretrained models](#loading-pretrained-models)
- [Usage](#usage)
    - [Conditional sequence generation](#conditional-sequence-generation)
    - [Conditional MSA generation](#conditional-msa-generation)
    - [Unconditional sequence generation](#unconditional-sequence-generation)
    - [Unconditional MSA generation](#unconditional-msa-generation)
- [Analysis of generations](#analysis-of-generations)
- [Conclusion](#conclusion)
- [Contributing](#contributing)
- [Trademarks](#trademarks)

----

# Installation
To download our code, we recommend creating a clean conda environment with python ```v3.8.5```. You can do so by running ```conda create --name evodiff python=3.8.5```. In that new environment, to download our code, run:
```
pip install evodiff
pip install git+https://github.com/microsoft/evodiff.git # bleeding edge, current repo main branch
```

You will also need to install PyTorch (we tested our models on ` v2.0.1 `), PyTorch Geometric, and PyTorch Scatter.

Our downstream analysis scripts make use of a variety of tools we do not include in our package. To run the scripts, please download the following packages first:
* [TM score](https://zhanggroup.org/TM-score/)
* [Omegafold](https://github.com/HeliXonProtein/OmegaFold)
* [ProteinMPNN](https://github.com/dauparas/ProteinMPNN)
* [ESM-IF1](https://github.com/facebookresearch/esm/tree/main/esm/inverse_folding); see this [Jupyter notebook](https://colab.research.google.com/github/facebookresearch/esm/blob/main/examples/inverse_folding/notebook.ipynb) for setup details.
* [PGP](https://github.com/hefeda/PGP)
* [DISOPRED3](https://github.com/psipred/disopred)
* [DR-BERT](https://github.com/maslov-group/DR-BERT)

Please follow the setup instructions outlined by the authors of those tools.

## Data
We obtain sequences from the [Uniref50 dataset](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4375400/), which contains approximately 45 million protein sequences. The Multiple Sequence Alignments (MSAs) are from the [OpenFold dataset](https://www.biorxiv.org/content/10.1101/2022.11.20.517210v2), containing MSAs for 132,000 unique Protein Data Bank (PDB) chains.

To access the sequences described in table S1 of the paper, use the following code:

```
test_data = UniRefDataset('data/uniref50/', 'rtest', structure=False) # To access the test sequences
curl -O ...(TODO) # To access the generated sequences
```

For the scaffolding structural motifs task, we provide pdb files used for conditionally generating sequences in the [examples/scaffolding-pdbs](https://github.com/microsoft/evodiff/tree/main/examples/scaffolding-pdbs) folder. We also provide
We provide pdb files used for conditionally generating MSAs in the [examples/scaffolding-msas](https://github.com/microsoft/evodiff/tree/main/examples/scaffolding-msas) folder.


## Loading pretrained models
To load a model:
```
from evodiff.pretrained import OA_AR_38M

model, collater, tokenizer, scheme = OA_AR_38M()
```
Available models are:
* ``` D3PM_BLOSUM_640M() ```
* ``` D3PM_BLOSUM_38M() ```
* ``` D3PM_UNIFORM_640M() ```
* ``` D3PM_UNIFORM_38M() ```
* ``` OA_AR_640M() ```
* ``` OA_AR_38M() ```
* ``` LR_AR_640M() ```
* ``` LR_AR_38M() ```
* ``` MSA_D3PM_BLOSUM() ```
* ``` MSA_D3PM_UNIFORM() ```
* ``` MSA_D3PM_OA_AR_RANDSUB() ```
* ``` MSA_D3PM_OA_AR_MAXSUB() ```


----

# Usage
We combine evolutionary-scale datasets with denoising diffusion probabilistic models (DDPMs) to develop a powerful new generative modeling framework for controllable protein design from sequence data alone, which we term EvoDiff. We evaluate our sequence and MSA models – EvoDiff-Seq and EvoDiff-MSA, respectively – across a range of generation tasks to demonstrate their power for controllable protein design.

## Conditional sequence generation
There are two ways to conditionally generate an MSA. 

The first is to generate the alignment from the query. To do so run:

``` python generate-msa.py TODO: ADD MODEL TYPE --subsampling random --batch-size 1 --start-query ```

The second is to generate the query from the alignment. To do so run:

``` python generate-msa.py TODO: ADD MODEL TYPE --subsampling random --batch-size 1 --start-msa ```

Note that you can only start-query or start-msa, not both. To generate unconditionally, omit the flags (see the example in the above section).

To create the Potts model, which serves as a baseline, we use [CCMpredPy and CCMgen](https://github.com/soedinglab/CCMgen/wiki/Getting-Started-with-CCMgen-and-CCMpredPy).

<!-- Conditional is same idea but bc stuff uses databases that exist point them to write scripts for each section, refer scaffold flag vs idr to gen, what need to run is notebook -->
<!-- idr use dr bert -->

## Conditional MSA generation
<!-- Msa cond gen self cons analysis -->


## Unconditional sequence generation

<!-- TODO: INTRO from text -->

To unconditionally generate 100 sequences, run the following script:
``` python evodiff/generate.py --model-type oa_ar_38M --num-seqs 100 ```

The default model type is `oa_ar_640M` , and the other available model types are:
* ` oa_ar_38M `
* ` carp_38M `
* ` carp_640M `
* ` esm1b_640M `

An example of generating 1 sequence randomly sampled from the train distribution length can be found in [this notebook](https://github.com/microsoft/evodiff/tree/main/examples/evodiff.ipynb).

To evaluate the generated sequences, we implement our Omegafold-ESM-IF pipeline, as shown in [analysis/self_consistency_analysis.py](https://github.com/microsoft/evodiff/blob/main/analysis/self_consistency_analysis.py). To use this evaluation script, 

1-2 sentences explaining downstream evals. "To evaluate the generated sequences,  we implement our Omegafold-ESM-IF pipeline, as shown in analysis/self-consistency.py... To use this eval, must have X dependencies installed"

 

1-2 sentences adding how to download sequences and their metrics, curl -0 zenodo


For sequence generation run:
``` python evodiff/generate.py --model-type oa_ar_38M ```

See figure 2 in the paper for our results.

## Unconditional MSA generation

While we do not analyze the unconditional MSA generations in our paper, we provide the script as it may be applicable to users.

# Analysis of generations
To access the sequences described in table S1 of the paper, use the following code:

```
test_data = UniRefDataset('data/uniref50/', 'rtest', structure=False) # To access the test sequences
curl -O ...(TODO) # To access the generated sequences
```
To analyze the quality of the generations, we look at:
* amino acid KL divergence ([aa_reconstruction_parity_plot](https://github.com/microsoft/evodiff/blob/main/evodiff/plot.py))
* secondary structure KL divergence ([evodiff/analysis/calc_kl_ss.py](https://github.com/microsoft/evodiff/blob/main/analysis/calc_kl_ss.py))
* model perplexity for sequences ([evodiff/analysis/sequence_perp.py](https://github.com/microsoft/evodiff/blob/main/analysis/sequence_perp.py))
* model perplexity for MSAs ([evodiff/analysis/msa_perp.py](https://github.com/microsoft/evodiff/blob/main/analysis/msa_perp.py)
* Fréchet inception distance ([evodiff/analysis/calc_fid.py](https://github.com/microsoft/evodiff/blob/main/analysis/calc_fid.py))
* Hamming distance ([evodiff/analysis/calc_nearestseq_hamming.py](https://github.com/microsoft/evodiff/blob/main/analysis/calc_nearestseq_hamming.py))

We also compute the self-consistency perplexity to evaluate the foldability of generated sequences. To do so, we make use of various tools:
* [TM score](https://zhanggroup.org/TM-score/)
* [Omegafold](https://github.com/HeliXonProtein/OmegaFold)
* [ProteinMPNN](https://github.com/dauparas/ProteinMPNN)
* [ESM-IF1](https://github.com/facebookresearch/esm/tree/main/esm/inverse_folding); see this [Jupyter notebook](https://colab.research.google.com/github/facebookresearch/esm/blob/main/examples/inverse_folding/notebook.ipynb) for setup details.
* [PGP](https://github.com/hefeda/PGP)
* [DISOPRED3](https://github.com/psipred/disopred)
* [DR-BERT](https://github.com/maslov-group/DR-BERT)

Please follow the setup instructions outlined by the authors of those tools.

Our analysis scripts for iterating over these tools are in the [evodiff/analysis/downstream_bash_scripts](https://github.com/microsoft/evodiff/tree/main/analysis/downstream_bash_scripts) folder. Once we run the scripts in this folder, we analyze the results in [self_consistency_analysis.py](https://github.com/microsoft/evodiff/blob/main/analysis/self_consistency_analysis.py).

# Conclusions

TODO

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos are subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third party trademarks or logos is subject to those third-party's policies.
