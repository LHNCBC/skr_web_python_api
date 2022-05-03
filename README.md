# Description

This Python-based API to the Indexing Initiative Scheduler facility
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

# Prerequisites

The SKR Web API requires at least Python 3.8 and two packages:
Requests and Requests-HTML to run.  It's possible that it will work
with earlier versions of Python 3 but that hasn't been tested.

Installing prequisites using pip:

    python3 -m pip install requests requests-html

# Building and Installing the API

Building the wheel package from sources:

    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    python3 -m build --no-isolation

Installing using wheel:

    python -m pip install dist/skr_web_api-0.1-py3-none-any.whl

# Usage

## A Simple Batch Example

A simple example of submitting file to generic batch with validation
to be processed by SemRep:

    >>> email = 'username@address'
    >>> apikey = somehexvalue
    >>> inputfilename = 'doc.txt'
    >>> inst = Submission(email, apikey)
    >>> inst.init_generic_batch("semrep", "-D")
    >>> inst.set_batch_file(inputfilename)
    >>> response = inst.submit()
    >>> print('response status: {}'.format(response.status_code))
    >>> print('content: {}'.format(response.content))

## Interactive Example

An example of processing a string using interactive MetaMap service:

    >>> email = 'username@address'
    >>> apikey = somehexvalue
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

The Python source file __generic_batch_file.py__ contains source for
example of submitting file to generic batch with validation.

Usage:

    usage: generic_batch_file.py [-h] [-e EMAIL] [-a APIKEY] inputfile


Example of use:

    python generic_batch_file.py --email user@host -a 5e53f \
    ~/queries/iiquery


### Interactive examples


MetaMap:

    python mm_interactive.py -e $EMAIL -a $UTS_API_KEY

MTI:

    python mti_interactive.py -e $EMAIL -a $UTS_API_KEY

SemRep:

    python sr_interactive.py -e $EMAIL -a $UTS_API_KEY
