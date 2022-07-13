# Indexing Initiative Web API: Python Implementation

This Python-based API for the Indexing Initiative Scheduler facility
was created to provide users with the ability to programmatically
submit jobs to the Scheduler Batch and Interactive facilities instead
of using the web-based interface.

Three programs are accessible via the Web API: MetaMap, the NLM
Medical Text Indexer (MTI), and SemRep. The functionality in these
programs includes: automatic indexing of MEDLINE citations,
concept-based query expansion, analysis of complex Metathesaurus
strings, accurate identification of the terminology and relationships
in anatomical documents, and the extraction of chemical binding
relations from biomedical text.

See Indexing Initiative's Web API page
(https://ii.nlm.nih.gov/Web_API/index.shtml) for more information.

# Prerequisites

+ To access either the the Interactive Mode or Batch Mode facilities,
  you must have accepted the terms of the
  [UMLS Metathesaurus License Agreement]
  (https://uts.nlm.nih.gov/license.html), which requires you to
  respect the copyrights of the constituent vocabularies and to file a
  brief annual report on your use of the UMLS. You also must have
  activated a [UMLS Terminology Services (UTS) account]
  (https://uts.nlm.nih.gov/home.html). See
  [UTS Account Information page]
  (http://skr.nlm.nih.gov/Help/umlsks.shtml) for information on how we
  use UTS authentication.

+ The SKR Web API requires at least Python 3.8 and two packages:
  Requests (https://docs.python-requests.org/en/latest/) and
  Requests-HTML (https://github.com/psf/requests-html) to run.  It's
  possible that it will work with earlier versions of Python 3 but
  that hasn't been tested.

# Building and Installing the API

Installing prerequisites using pip:

    python3 -m pip install requests requests-html
    python3 -m pip install wheel
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build

Building the wheel package from sources after cloning the repository:

	git clone https://github.com/lhncbc/skr_web_python_api.git
	cd skr_web_python_api
    python3 -m build

Installing the wheel package into your virtual environment:

    python3 -m pip install dist/skr_web_api-0.1-py3-none-any.whl

Note: If you don't have write access to the installed Python then you
may need to use virtual environment created using venv
(https://docs.python.org/3/library/venv.html) or Miniconda
(https://docs.conda.io/en/latest/miniconda.html).


# Usage

To run the examples, you'll need a UTS API key which available in your
UTS profile.

## A Simple Batch Example

A simple example of submitting file to generic batch with validation
to be processed by SemRep:

    >>> email = 'username@address'
    >>> apikey = '<UTS apikey>'
    >>> inputfilename = 'doc.txt'
    >>> inst = Submission(email, apikey)
    >>> inst.init_generic_batch("semrep", "-D")
    >>> inst.set_batch_file(inputfilename)
    >>> response = inst.submit()
    >>> print('response status: {}'.format(response.status_code))
    response status: 200
    >>> print('content: {}'.format(response.content))
	... output omitted ...

## Interactive Example

An example of processing a string using interactive MetaMap service:

    >>> email = 'username@address'
    >>> apikey = '<UTS apikey>'
    >>> inputfilename = 'doc.txt'
    >>> inst = Submission(email, apikey)
	>>> inputtext = "A spinal tap was performed and oligoclonal bands were \
    detected in the cerebrospinal fluid.\n"
    >>> inst.init_mm_interactive(inputtext)
    >>> response = inst.submit()
    >>> print('response status: {}'.format(response.status_code))
    response status: 200
    >>> print('content:\n {}'.format(response.content.decode()))
    content:
    /dmzfiler/II_Group/MetaMap2020/public_mm/bin/SKRrun.20 /dmzfiler/II_Group/MetaMap2020/public_mm/bin/metamap20.BINARY.Linux --lexicon db -Z 2020AB -N
    USER|MMI|5.18|Diagnostic lumbar puncture|C0553794|[diap]|["Spinal Tap"-tx-1-"spinal tap"-noun-0]|TX|2/10|
    USER|MMI|5.18|Oligoclonal Bands|C4048246|[lbtr]|["Oligoclonal Bands"-tx-1-"oligoclonal bands"-noun-0]|TX|31/17|
    USER|MMI|5.18|Oligoclonal Bands (protein)|C0069426|[aapp,imft]|["Oligoclonal Bands"-tx-1-"oligoclonal bands"-noun-0]|TX|31/17|
    USER|MMI|5.18|Oligoclonal protein measurement|C0202205|[lbpr]|["Oligoclonal Bands"-tx-1-"oligoclonal bands"-noun-0]|TX|31/17|
    USER|MMI|5.18|Performed|C0884358|[ftcn]|["PERFORMED"-tx-1-"performed"-verb-0]|TX|17/9|
    USER|MMI|5.18|Spinal Puncture|C0037943|[hlca]|["Spinal Tap"-tx-1-"spinal tap"-noun-0]|TX|2/10|
    USER|MMI|3.61|Cerebrospinal Fluid|C0007806|[bdsu]|["Spinal Fluid, Cerebro"-tx-1-"cerebrospinal fluid"-noun-0]|TX|70/19|
    USER|MMI|3.61|In Cerebrospinal Fluid|C0007807|[ftcn]|["cerebrospinal fluid"-tx-1-"cerebrospinal fluid"-noun-0]|TX|70/19|
    USER|MMI|3.56|Detected (finding)|C0442726|[fndg]|["Detected"-tx-1-"detected"-verb-0]|TX|54/8|
    USER|MMI|3.56|Detection|C1511790|[topp]|["Detected"-tx-1-"detected"-verb-0]|TX|54/8|
    >>>

## Example programs

### Generic Batch Example

The Python source file __generic_batch_file.py__, in the __examples__
directory, contains source for example of submitting file to generic
batch with validation.

Usage:

    usage: generic_batch_file.py [-h] [-e EMAIL] [-a APIKEY] inputfile


Example of use:

    python examples/generic_batch_file.py -e user@host -a 1234-5678-9ABC-DEF1 \
    ~/queries/iiquery


### Interactive example sources


The directory __examples__ also contains examples of using the
MetaMap, MTI, and SemRep interactive services.

MetaMap:

    python examples/mm_interactive.py -e $EMAIL -a $UTS_API_KEY

MTI:

    python examples/mti_interactive.py -e $EMAIL -a $UTS_API_KEY

SemRep:

    python examples/sr_interactive.py -e $EMAIL -a $UTS_API_KEY
